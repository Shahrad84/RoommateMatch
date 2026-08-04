from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def main_page(request):
    return render(request, "templates/main.html")