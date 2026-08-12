from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile, LifestyleProfile, Preference
from django.contrib.auth import logout

@login_required(login_url='/accounts/login/')
def account_page(request):
    account = request.user
    
    # Check if profile is complete
    profile_complete = (
        Profile.objects.filter(account=account).exists() and
        LifestyleProfile.objects.filter(account=account).exists() and
        Preference.objects.filter(account=account).exists()
    )
    
    # Get profile data
    profile = None
    if Profile.objects.filter(account=account).exists():
        profile = Profile.objects.get(account=account)
    
    return render(request, "templates/account_overview.html", {
        'profile_complete': profile_complete,
        'profile': profile,
    })


@login_required
def logout_handle(request):
    logout(request)
    return redirect("/accounts/login/")