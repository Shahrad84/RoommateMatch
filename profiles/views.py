from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Profile, LifestyleProfile, Preference


@login_required(login_url='/accounts/login/')
def profile_complete(request):
  
    account = request.user
    
    # Try to get existing records
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
    
    if request.method == 'POST':
        
        print("========== POST RECEIVED ==========")
        print(request.POST)

        # Create forms using modelform_factory
        ProfileForm = forms.modelform_factory(Profile, fields=['birthdate', 'job', 'bio'])
        LifestyleForm = forms.modelform_factory(LifestyleProfile, fields=[
            'cleaning_frequency', 'noise_generating_level', 'noise_tolerance', 
            'social_level', 'smoking', 'has_pets', 'cooking', 'eating_at_home',
            'wake_up', 'sleep', 'guests', 'overnight_guests'
        ])
        PreferenceForm = forms.modelform_factory(Preference, fields=[
            'cleanliness_weight', 'noise_weight', 'social_weight', 
            'pets_weight', 'cooking_weight', 'guests_weight', 
            'sleep_schedule_weight', 'accepts_smokers', 'accepts_pets'
        ])

        profile_form = ProfileForm(request.POST, instance=profile)
        lifestyle_form = LifestyleForm(request.POST, instance=lifestyle)
        preference_form = PreferenceForm(request.POST, instance=preference)
        
        # Validate all forms
        if profile_form.is_valid() and lifestyle_form.is_valid() and preference_form.is_valid():
            profile_form.save()
            lifestyle_form.save()
            preference_form.save()
            messages.success(request, 'Profile saved successfully!')            
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Please fix the errors below.')
    
    else:
        # Create forms using modelform_factory
        ProfileForm = forms.modelform_factory(Profile, fields=['birthdate', 'job', 'bio'])
        LifestyleForm = forms.modelform_factory(LifestyleProfile, fields=[
            'cleaning_frequency', 'noise_generating_level', 'noise_tolerance', 
            'social_level', 'smoking', 'has_pets', 'cooking', 'eating_at_home',
            'wake_up', 'sleep', 'guests', 'overnight_guests'
        ])
        PreferenceForm = forms.modelform_factory(Preference, fields=[
            'cleanliness_weight', 'noise_weight', 'social_weight', 
            'pets_weight', 'cooking_weight', 'guests_weight', 
            'sleep_schedule_weight', 'accepts_smokers', 'accepts_pets'
        ])

        profile_form = ProfileForm(instance=profile)
        lifestyle_form = LifestyleForm(instance=lifestyle)
        preference_form = PreferenceForm(instance=preference)
    
    return render(request, "templates/profile_complete.html", {
        'profile_form': profile_form,
        'lifestyle_form': lifestyle_form,
        'preference_form': preference_form,
    })


