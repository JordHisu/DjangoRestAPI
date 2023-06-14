from django.db import models
from . import Player


class GameScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

