from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from locations.models import City 

class Account(models.Model):

    GENDER_CHOICES = (
        ("male", "male"),
        ("female", "female"),
    )

    user_id = models.AutoField(primary_key=True)


    # base infos
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user', 
        verbose_name="city"
    )