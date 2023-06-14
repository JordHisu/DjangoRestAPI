from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import City
from .models import State
from .models import Player
from .models import GameScore


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'email', 'groups', 'player']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['url', 'name', 'nickname', 'user']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScore
        fields = '__all__'

