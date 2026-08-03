from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="profile",
        verbose_name="account"   
    )

    bitrhdate = models.TimeField()
    job = models.CharField(max_length=20)
    bio = models.CharField(max_length=200, blank=True, null=True)


class LifestyleProfile(models.Model):
        
    NOISE_TOLERANCE_CHOICES = (
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high"),
    )


    TIME_FREQUENCY_CHOICES = (
        ("never", "never"),
        ("sometimes", "sometimes"),
        ("often", "often"),
        ("usually", "usually"),
        ("always", "always")
    )


    cleaning_frequency = models.CharField(max_length=30, choices=TIME_FREQUENCY_CHOICES)

    noise_generating_level = models.CharField(max_length=30, choices=NOISE_TOLERANCE_CHOICES)
    noise_tolerance = models.CharField(max_length=30, choices=NOISE_TOLERANCE_CHOICES)

    social_level = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    smoking = models.BooleanField()

    has_pets = models.BooleanField()

    cooking = models.CharField(max_length=30, choices=TIME_FREQUENCY_CHOICES)
    eating_at_home = models.CharField(max_length=30, choices=TIME_FREQUENCY_CHOICES)

    wake_up = models.TimeField()
    sleep = models.TimeField()

    guests = models.CharField(TIME_FREQUENCY_CHOICES)
    overnight_guests = models.CharField(max_length=40, choices=TIME_FREQUENCY_CHOICES)



class Preference(models.Model):

    cleanliness_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    noise_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    social_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    pets_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    cooking_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    guests_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    sleep_schedule_weight = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    accepts_smokers = models.BooleanField()
    accepts_pets = models.BooleanField()