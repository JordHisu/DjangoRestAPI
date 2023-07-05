
from django.db import models
from django.contrib.auth.models import User

from . import City
from . import State


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, default='')
    birth_date = models.DateField(null=True)
    street = models.CharField(max_length=100, default='Lugar Nenhum')
    street_number = models.CharField(max_length=5, default=0)
    bairro = models.CharField(max_length=30, default='Bairro Nenhum')
    cep = models.CharField(max_length=8, default='00000000')
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} ({str(self.id)})"

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email



