
from django.db import models
from .state import State


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=15)
    population = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']
        unique_together = [('state', 'name')]

