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
            'smoking', 'cleanliness', 'noise_generating', 
            'social_activity', 'wake_up', 'sleep', 'has_pets',
            'guests_frequency', 'cooking'
        ])
        
        PreferenceForm = forms.modelform_factory(Preference, fields=[
            'cleanliness_importance', 'noise_importance', 'max_noise', 
            'social_importance', 'preferred_social_activity', 
            'sleep_schedule_importance', 'guests_importance', 
            'max_guests_frequency', 'cooking_importance', 
            'accepts_pets', 'accepts_smoking'
        ])

        profile_form = ProfileForm(request.POST, instance=profile)
        lifestyle_form = LifestyleForm(request.POST, instance=lifestyle)
        preference_form = PreferenceForm(request.POST, instance=preference)
        
        # Validate all forms
        if profile_form.is_valid() and lifestyle_form.is_valid() and preference_form.is_valid():
            
            # Set account before saving
            profile_obj = profile_form.save(commit=False)
            profile_obj.account = account
            profile_obj.save()
            
            lifestyle_obj = lifestyle_form.save(commit=False)
            lifestyle_obj.account = account
            lifestyle_obj.save()
            
            preference_obj = preference_form.save(commit=False)
            preference_obj.account = account
            preference_obj.save()
            
            messages.success(request, 'Profile saved successfully!')            
            return redirect('/dashboard/')
        else:
            print("Profile Form Errors:", profile_form.errors)
            print("Lifestyle Form Errors:", lifestyle_form.errors)
            print("Preference Form Errors:", preference_form.errors)
            messages.error(request, 'Please fix the errors below.')
    
    else:
        # Create forms using modelform_factory
        ProfileForm = forms.modelform_factory(Profile, fields=['birthdate', 'job', 'bio'])
        
        LifestyleForm = forms.modelform_factory(LifestyleProfile, fields=[
            'smoking', 'cleanliness', 'noise_generating', 
            'social_activity', 'wake_up', 'sleep', 'has_pets',
            'guests_frequency', 'cooking'
        ])
        
        PreferenceForm = forms.modelform_factory(Preference, fields=[
            'cleanliness_importance', 'noise_importance', 'max_noise', 
            'social_importance', 'preferred_social_activity', 
            'sleep_schedule_importance', 'guests_importance', 
            'max_guests_frequency', 'cooking_importance', 
            'accepts_pets', 'accepts_smoking'
        ])

        profile_form = ProfileForm(instance=profile)
        lifestyle_form = LifestyleForm(instance=lifestyle)
        preference_form = PreferenceForm(instance=preference)
    
    return render(request, "templates/profile_complete.html", {
        'profile_form': profile_form,
        'lifestyle_form': lifestyle_form,
        'preference_form': preference_form,
    })