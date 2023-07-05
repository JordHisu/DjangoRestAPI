import json
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group
from django.db.models import QuerySet
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView

from restAPI.APIApp.serializers import UserSerializer, CitySerializer, StateSerializer, PlayerSerializer, ScoreSerializer
from .models import City
from .models import State
from .models import Player
from .models import GameScore
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
import csv
from django.contrib.auth import authenticate
from django.http import HttpResponse


@csrf_exempt
def login(request):
    try:
        body = json.loads(request.body)
        user = User.objects.get(username=body['username'])
        correct_password = body['password'] == user.password
        if correct_password:
            player = Player.objects.get(user_id=user.id)
            return JsonResponse({
                'status': 'SUCCESS',
                'player': {
                    'username': user.username,
                    'superuser': user.is_superuser,
                    'name': player.name,
                    'email': player.email,
                    'cep': player.cep,
                    'city': player.city_id,
                    'state': player.state_id,
                    'bairro': player.bairro,
                    'birth_date': player.birth_date,
                    'street': player.street,
                    'street_number': player.street_number,
                    'id': player.pk,
                }
            })
        else:
            return JsonResponse({'status': 'FAILED', 'reason': 'User not found or password incorrect'})
    except Exception as e:
        return JsonResponse({'status': 'ERROR', 'reason': f"{type(e)} - {e}"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        player_data = request.data.copy()
        player_serializer = PlayerSerializer(data=player_data)
        player_serializer.is_valid(raise_exception=True)
        player = player_serializer.save()

        user_data = request.data.copy()
        user_data['player'] = player.id  # reverse('player-detail', args=[player.id])
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            player.delete()
            return Response({'status': 'FAILED', 'reason': user_serializer.errors})
        user = user_serializer.save()
        user.password = user_data['password']
        user.save()
        player.user = user
        player.save()
        return Response({'status': 'SUCCESS', 'player_id': player.id})


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        player = self.get_object()
        data_copy = request.data.copy()
        player_serializer = self.get_serializer(player, data=request.data, partial=True)
        player_serializer.is_valid(raise_exception=True)
        user_serializer = self.get_serializer(player.user, data=data_copy, partial=True)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(player_serializer)
        self.perform_update(user_serializer)
        if 'password' in data_copy.keys():
            player.user.password = data_copy['password']
            player.user.save()
        return Response({'status': 'SUCCESS'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user is not None:
            self.perform_destroy(instance.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     # permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        state_filter = self.request.query_params.get('state')
        if state_filter:
            queryset = queryset.filter(state=state_filter)
        return queryset


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    pagination_class = None
    # permission_classes = [permissions.IsAuthenticated]


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = GameScore.objects.all().order_by('-score')
    serializer_class = ScoreSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        queryset = self.queryset
        queryset = self.filter_player(queryset)
        queryset = self.filter_score(queryset)
        return queryset

    def filter_player(self, queryset):
        player_filter = self.request.query_params.get('player')
        if player_filter:
            queryset = queryset.filter(player=player_filter)
        return queryset

    def filter_score(self, queryset):
        score_filter = self.request.query_params.get('score')
        if score_filter:
            queryset = queryset.filter(score=score_filter)
        return queryset

    @action(detail=False, methods=['delete'])
    def delete_filtered(self, request):
        player_id = self.request.query_params.get('player')
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            player = None

        if player_id is None or player is None:
            return Response({'status': 'FAILED', 'reason': "You need to specify a valid player."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_player(self.get_queryset())
        queryset = self.filter_score(queryset)
        count, _ = queryset.delete()
        return Response({'status': 'SUCCESS', 'count': count, 'player': int(player_id)}, status=status.HTTP_204_NO_CONTENT)


@api_view()
def populate_database(request):
    State.objects.all().delete()
    City.objects.all().delete()

    states_to_save = []
    with open('estados.csv', encoding='utf-8') as state_csv:
        state_list = csv.DictReader(state_csv, delimiter=';')
        for state in state_list:
            states_to_save.append(
                State(name=state['Estado'], region=State.map_region(state['Região']),
                      abbreviation=state['UF'], city_count=state['Qtd Mun'])
            )
    State.objects.bulk_create(states_to_save)
    all_states = dict([(state.abbreviation, state) for state in State.objects.all()])

    cities_to_save = []
    states_to_update = []
    with open('cidades.csv', encoding='utf-8') as city_csv:
        city_list = csv.DictReader(city_csv, delimiter=';')
        for city in city_list:
            state = all_states[city['UF']]
            try:
                population = int(city['População 2010'])
            except ValueError:
                population = 0

            new_city = City(name=city['Município'], state=state, size=city['Porte'], population=population)

            if city['Capital'] != '':
                state.capital = new_city
                states_to_update.append(state)
            cities_to_save.append(new_city)

    City.objects.bulk_create(cities_to_save)
    State.objects.bulk_update(states_to_update, fields=['capital'])
    response_body = {'status': 'SUCCESS'}
    return Response(data=response_body, status=status.HTTP_200_OK)

