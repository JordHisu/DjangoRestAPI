
from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return f"{self.name} ({str(self.id)})"


