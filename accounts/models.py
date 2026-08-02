from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from locations.models import City 

class account(models.Model):

    GENDER_CHOICES = (
        ("male", "male"),
        ("female", "female"),
    )

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

    PREFER_CHOICES = (
        ("always together", "always together"),
        ("sometimes hang out", "sometimes hang out"),
        ("personal space", "personal space")
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

    job = models.CharField(max_length=20)
    bio = models.CharField(max_length=200, blank=True, null=True)


    # sleep
    wake_up = models.TimeField()
    sleep = models.TimeField()


    # cleaning
    cleanliness = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    cleaning_frequency = models.CharField(max_length=30, choices=TIME_FREQUENCY_CHOICES)


    # voice
    noise_tolerance = models.CharField(max_length=30, choices=NOISE_TOLERANCE_CHOICES)


    # smoking
    smoking = models.BooleanField()


    # pets
    has_pets = models.BooleanField()
    accept_pets = models.BooleanField()


    # food
    cooking = models.CharField(max_length=30, choices=TIME_FREQUENCY_CHOICES)
    eating_at_home = models.CharField(max_length=30, choices=TIME_FREQUENCY_CHOICES)


    # guests
    guests = models.CharField(TIME_FREQUENCY_CHOICES)
    overnight_guests = models.CharField(max_length=40, choices=TIME_FREQUENCY_CHOICES)


    # social style
    social_level = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    prefer = models.CharField(max_length=30, choices=PREFER_CHOICES)