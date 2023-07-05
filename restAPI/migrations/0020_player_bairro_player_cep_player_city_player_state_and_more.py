# Generated by Django 4.2.2 on 2023-07-05 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0019_player_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bairro',
            field=models.CharField(default='Bairro Nenhum', max_length=30),
        ),
        migrations.AddField(
            model_name='player',
            name='cep',
            field=models.IntegerField(default='00000000', max_length=8),
        ),
        migrations.AddField(
            model_name='player',
            name='city',
            field=models.ForeignKey(default=10584, on_delete=django.db.models.deletion.DO_NOTHING, to='restAPI.city'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='state',
            field=models.ForeignKey(default=428, on_delete=django.db.models.deletion.DO_NOTHING, to='restAPI.state'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='street',
            field=models.CharField(default='Lugar Nenhum', max_length=100),
        ),
        migrations.AddField(
            model_name='player',
            name='street_number',
            field=models.CharField(default=0, max_length=5),
        ),
    ]