# Generated by Django 4.2.2 on 2023-06-13 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0004_city_population_alter_city_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='size',
            field=models.CharField(max_length=15),
        ),
    ]
