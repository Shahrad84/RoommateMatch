from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.models import Profile, LifestyleProfile, Preference

@login_required(login_url='/accounts/login/')
def main_page(request):
    return render(request, "templates/main.html")

@login_required(login_url='/accounts/login/')
def dashboard_page(request):
    account = request.user  # NOT request.UserWarning

    profile_complete = (
        Profile.objects.filter(account=account).exists() and
        LifestyleProfile.objects.filter(account=account).exists() and
        Preference.objects.filter(account=account).exists()
    )

    return render(request, "templates/dashboard.html", {
        "profile_complete": profile_complete
    })