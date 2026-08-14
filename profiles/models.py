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

    smoking = models.BooleanField(
        null=True
    )

    cleanliness = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    noise_generating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    social_activity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )


    wake_up = models.TimeField()

    sleep = models.TimeField()


    has_pets = models.BooleanField(
        null=True
    )

    guests_frequency = models.CharField(
        max_length=12,
        choices=TIME_FREQUENCY_CHOICES
    )
    
    cooking = models.CharField(
        max_length=30,
        choices=TIME_FREQUENCY_CHOICES
    )

    def is_complete(self):
        required_fields = [
            self.smoking,
            self.cleanliness,
            self.noise_generating,
            self.social_activity,
            self.wake_up,
            self.sleep,
            self.has_pets,
            self.guests_frequency,
            self.cooking
,

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

    cleanliness_importance = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    noise_importance = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    max_noise = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    social_importance = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    preferred_social_activity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    sleep_schedule_importance = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    guests_importance = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    max_guests_frequency = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    cooking_importance = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )    

    accepts_pets = models.BooleanField(
        null=True
    )

    accepts_smoking = models.BooleanField(
        null=True
    )

    def is_complete(self):
        required_fields = [
            self.cleanliness_importance,
            self.noise_importance,
            self.max_noise,
            self.social_importance,
            self.preferred_social_activity,
            self.sleep_schedule_importance,
            self.guests_importance,
            self.max_guests_frequency,
            self.max_guests_frequency,
            self.cooking_importance,
            self.accepts_pets,
            self.accepts_smoking,
        ]

        for f in required_fields:
            if f is None:
                return False

        return True


    def __str__(self):
        return f"{self.account.username}'s Preferences"