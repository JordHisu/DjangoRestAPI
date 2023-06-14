from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class Player(models.Model):
    user = models.OneToOneField(User, related_name='player', on_delete=models.CASCADE, null=True, )

    def __str__(self):
        return self.nickname

    @property
    def nickname(self):
        return self.user.username

    @property
    def name(self):
        return self.user.first_name

    def get_fields(self):
        return [f.name for f in self._meta.get_fields()]


@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()
