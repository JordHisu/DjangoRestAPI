from django.db import models


class GameScore(models.Model):
    player = models.ForeignKey(Player, on_delete=DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=DO_NOTHING)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)