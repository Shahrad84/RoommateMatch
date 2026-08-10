from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator


# ====================== Profile ===================== 

class Profile(models.Model):

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    birthdate = models.DateField()
    job = models.CharField(max_length=50)
    bio = models.TextField(
        max_length=200,
        blank=True
    )

    def is_complete(self):
        required_fields = [
            self.birthdate,
            self.job,
        ]

        for f in required_fields:
            if f is None:
                return False

        return True
    

    def __str__(self):
        return f"{self.account.username}'s Profile"



#============================= Lifestle ============================

class LifestyleProfile(models.Model):

    NOISE_TOLERANCE_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    TIME_FREQUENCY_CHOICES = (
        ("never", "Never"),
        ("sometimes", "Sometimes"),
        ("often", "Often"),
        ("usually", "Usually"),
        ("always", "Always"),
    )

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="lifestyle"
    )

    cleaning_frequency = models.CharField(
        max_length=30,
        choices=TIME_FREQUENCY_CHOICES
    )

    noise_generating_level = models.CharField(
        max_length=30,
        choices=NOISE_TOLERANCE_CHOICES
    )

    noise_tolerance = models.CharField(
        max_length=30,
        choices=NOISE_TOLERANCE_CHOICES
    )

    social_level = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    smoking = models.BooleanField(
        null=True
    )

    has_pets = models.BooleanField(
        null=True
    )

    cooking = models.CharField(
        max_length=30,
        choices=TIME_FREQUENCY_CHOICES
    )

    eating_at_home = models.CharField(
        max_length=30,
        choices=TIME_FREQUENCY_CHOICES
    )

    wake_up = models.TimeField()

    sleep = models.TimeField()

    guests = models.CharField(
        max_length=12,
        choices=TIME_FREQUENCY_CHOICES
    )

    overnight_guests = models.CharField(
        max_length=12,
        choices=TIME_FREQUENCY_CHOICES
    )

    def is_complete(self):
        required_fields = [
            self.birthdate,
            self.job,
        ]

        for f in required_fields:
            if f is None:
                return False

        return True


    def __str__(self):
        return f"{self.account.username}'s Lifestyle"



# ============================ Prefrence ==============================

class Preference(models.Model):

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="preference"
    )

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

    accepts_smokers = models.BooleanField(
        null=True
    )

    accepts_pets = models.BooleanField(
        null=True
    )

    def is_complete(self):
        required_fields = [
            self.birthdate,
            self.job,
        ]

        for f in required_fields:
            if f is None:
                return False

        return True


    def __str__(self):
        return f"{self.account.username}'s Preferences"