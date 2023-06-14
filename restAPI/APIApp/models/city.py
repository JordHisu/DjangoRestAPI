
from django.db import models
from .state import State


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=15)
    population = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.state.name})"

