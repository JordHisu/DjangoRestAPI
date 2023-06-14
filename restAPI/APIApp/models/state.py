
from django.db import models


class State(models.Model):
    REGIONS = [
        ("N", "Norte"),
        ("NE", "Nordeste"),
        ("S", "Sul"),
        ("SE", "Sudeste"),
        ("CO", "Centro-Oeste"),
    ]

    name = models.CharField(max_length=30, unique=True)
    region = models.CharField(max_length=2, choices=REGIONS)
    capital = models.OneToOneField('restAPI.City', on_delete=models.SET_NULL, related_name='capital_state', default=None, null=True)
    abbreviation = models.CharField(max_length=2, null=True, unique=True)
    city_count = models.IntegerField(null=True)

    @classmethod
    def map_region(cls, value):
        for abbreviation, region in cls.REGIONS:
            if region in value:
                return abbreviation
        return value

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
