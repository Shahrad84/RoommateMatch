from django.shortcuts import render, redirect
from .models import Profile, LifestyleProfile, Preference
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birthdate', 'job', 'bio']

class LifestyleProfileForm(forms.ModelForm):
    class Meta:
        model = LifestyleProfile
        fields = ['cleaning_frequency', 'noise_generating_level', 'noise_tolerance', 
                 'social_level', 'smoking', 'has_pets', 'cooking', 'eating_at_home',
                 'wake_up', 'sleep', 'guests', 'overnight_guests']

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['cleanliness_weight', 'noise_weight', 'social_weight', 
                 'pets_weight', 'cooking_weight', 'guests_weight', 
                 'sleep_schedule_weight', 'accepts_smokers', 'accepts_pets']


def profile_complete(request):

    if request.method == "POST":

        print("========== POST RECEIVED ==========")
        print(request.POST)

        account = request.user

        try:
            profile = Profile.objects.get(account=account)
        except Profile.DoesNotExist:
            profile = None

        try:
            lifestyle = LifestyleProfile.objects.get(account=account)
        except LifestyleProfile.DoesNotExist:
            lifestyle = None

        try:
            preference = Preference.objects.get(account=account)
        except Preference.DoesNotExist:
            preference = None

        profile_form = ProfileForm(request.POST, instance=profile)
        lifestyle_form = LifestyleProfileForm(request.POST, instance=lifestyle)
        preference_form = PreferenceForm(request.POST, instance=preference)

        if profile_form.is_valid() and lifestyle_form.is_valid() and preference_form.is_valid():
            profile_form.save()
            lifestyle_form.save()
            preference_form.save()
            return redirect("/dashboard/")

    else:
        try:
            profile = Profile.objects.get(account=request.user)
        except Profile.DoesNotExist:
            profile = None

        try:
            lifestyle = LifestyleProfile.objects.get(account=request.user)
        except LifestyleProfile.DoesNotExist:
            lifestyle = None

        try:
            preference = Preference.objects.get(account=request.user)
        except Preference.DoesNotExist:
            preference = None

        profile_form = ProfileForm(instance=profile)
        lifestyle_form = LifestyleProfileForm(instance=lifestyle)
        preference_form = PreferenceForm(instance=preference)

    return render(request, "templates/profile_complete.html", {
        'profile_form': profile_form,
        'lifestyle_form': lifestyle_form,
        'preference_form': preference_form,
    })