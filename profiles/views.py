from django.shortcuts import render, redirect
from .models import Profile, LifestyleProfile, Preference


def profile_complete(request):

    if request.method == "POST":

        print("========== POST RECEIVED ==========")
        print(request.POST)

        account = request.user

        Profile.objects.create(
            account=account,
            birthdate=request.POST.get("birthdate"),
            job=request.POST.get("job"),
            bio=request.POST.get("bio"),
        )

        LifestyleProfile.objects.create(
            account=account,
            cleaning_frequency=request.POST.get("cleaning_frequency"),
            noise_generating_level=request.POST.get("noise_generating_level"),
            noise_tolerance=request.POST.get("noise_tolerance"),
            social_level=request.POST.get("social_level"),
            smoking=request.POST.get("smoking") == "true",
            has_pets=request.POST.get("has_pets") == "true",
            cooking=request.POST.get("cooking"),
            eating_at_home=request.POST.get("eating_at_home"),
            wake_up=request.POST.get("wake_up"),
            sleep=request.POST.get("sleep"),
            guests=request.POST.get("guests"),
            overnight_guests=request.POST.get("overnight_guests"),
        )

        Preference.objects.create(
            account=account,
            cleanliness_weight=request.POST.get("cleanliness_weight"),
            noise_weight=request.POST.get("noise_weight"),
            social_weight=request.POST.get("social_weight"),
            pets_weight=request.POST.get("pets_weight"),
            cooking_weight=request.POST.get("cooking_weight"),
            guests_weight=request.POST.get("guests_weight"),
            sleep_schedule_weight=request.POST.get("sleep_schedule_weight"),
            accepts_smokers=request.POST.get("accepts_smokers") == "true",
            accepts_pets=request.POST.get("accepts_pets") == "true",
        )

        return redirect("/dashboard/")

    return render(request, "templates/profile_complete.html")