# Generated by Django 4.2.2 on 2023-07-05 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0017_player_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='username',
        ),
    ]
