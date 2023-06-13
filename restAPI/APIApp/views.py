from django.contrib.auth.models import User, Group
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework import permissions
from restAPI.APIApp.serializers import UserSerializer, GroupSerializer, CitySerializer, StateSerializer
from .models import City
from .models import State
from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    # permission_classes = [permissions.IsAuthenticated]


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    # permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
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

    return Response(status=status.HTTP_200_OK)

