from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class City(models.Model):

    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="city",
        verbose_name="country"
    )