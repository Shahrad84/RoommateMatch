from django.db import models
from django.contrib.auth.models import AbstractUser
from locations.models import City 


class Account(AbstractUser):

    GENDER_CHOICES = (
        ("male", "male"),
        ("female", "female"),
        ("other", "other"),
    )


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


    def __str__(self):
        return self.username