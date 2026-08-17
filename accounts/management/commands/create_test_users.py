from django.core.management.base import BaseCommand
from accounts.models import Account
from locations.models import City, Country
from profiles.models import Profile, LifestyleProfile, Preference
import random
from datetime import time, date


class Command(BaseCommand):
    help = 'Creates 30 test users in Berlin'

    def handle(self, *args, **options):
        # Create Germany
        germany, created = Country.objects.get_or_create(name="Germany")
        self.stdout.write(f"Germany ready (created: {created})")
        
        # Create Berlin
        berlin, created = City.objects.get_or_create(name="Berlin", country=germany)
        self.stdout.write(f"Berlin ready (created: {created})")
        
        # Set existing users to Berlin
        for username in ['ShahradLF', 'Arad1321']:
            try:
                user = Account.objects.get(username=username)
                user.city = berlin
                user.save()
                self.stdout.write(f"Set {username} to Berlin")
            except Account.DoesNotExist:
                self.stdout.write(f"User {username} not found")
        
        jobs = ['Engineer', 'Doctor', 'Teacher', 'Designer', 'Student', 'Chef', 'Artist', 'Developer']
        bios = ['Love cooking and hiking', 'Quiet and tidy person', 'Music lover', 'Gym enthusiast', 'Book worm', 'Movie buff']
        genders = ['male', 'female', 'other']
        names = ['Alex', 'Sarah', 'Mike', 'Emma', 'John', 'Lisa', 'David', 'Anna', 
                 'Chris', 'Julia', 'Tom', 'Maria', 'James', 'Sofia', 'Daniel', 'Laura',
                 'Max', 'Nina', 'Paul', 'Elena', 'Sam', 'Katie', 'Ryan', 'Maya',
                 'Kevin', 'Lena', 'Mark', 'Tina', 'Ben', 'Zoe']
        
        created_count = 0
        
        for i in range(1, 31):
            username = f"testuser{i}"
            
            # Skip if already exists
            if Account.objects.filter(username=username).exists():
                self.stdout.write(f"Skipping {username} (already exists)")
                continue
            
            email = f"test{i}@gmail.com"
            password = "Test12345"
            name = random.choice(names)
            age = random.randint(18, 35)
            gender = random.choice(genders)
            
            account = Account.objects.create_user(
                username=username,
                email=email,
                password=password,
                city=berlin,
                name=name,
                age=age,
                gender=gender
            )
            
            Profile.objects.create(
                account=account,
                birthdate=date(random.randint(1995, 2005), random.randint(1, 12), random.randint(1, 28)),
                job=random.choice(jobs),
                bio=random.choice(bios)
            )
            
            LifestyleProfile.objects.create(
                account=account,
                smoking=random.choice([True, False]),
                cleanliness=random.randint(1, 10),
                noise_generating=random.randint(1, 10),
                social_activity=random.randint(1, 10),
                wake_up=time(random.randint(5, 9), random.choice([0, 30])),
                sleep=time(random.randint(22, 23), random.choice([0, 30])),
                has_pets=random.choice([True, False]),
                guests_frequency=random.choice(['never', 'sometimes', 'often', 'usually', 'always']),
                cooking=random.choice(['never', 'sometimes', 'often', 'usually', 'always'])
            )
            
            Preference.objects.create(
                account=account,
                cleanliness_importance=random.randint(1, 10),
                noise_importance=random.randint(1, 10),
                max_noise=random.randint(1, 10),
                social_importance=random.randint(1, 10),
                preferred_social_activity=random.randint(1, 10),
                sleep_schedule_importance=random.randint(1, 10),
                guests_importance=random.randint(1, 10),
                max_guests_frequency=random.randint(1, 10),
                cooking_importance=random.randint(1, 10),
                accepts_pets=random.choice([True, False]),
                accepts_smoking=random.choice([True, False])
            )
            
            created_count += 1
            self.stdout.write(f"Created: {username}")
        
        self.stdout.write(self.style.SUCCESS(f"Done! Created {created_count} test users."))