import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken



def login_page(request):

    if request.user.is_authenticated:
        return redirect("/dashboard/")

    return render(request, "templates/login.html")



@csrf_exempt
def login_api(request):


    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Method not allowed"
        }, status=405)


    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:

        return JsonResponse({
            "success": False,
            "message": "Invalid JSON"
        }, status=400)


    username = data.get("username")
    password = data.get("password")



    errors = {}
    if not username:
        errors["username"] = "Username is required"

    if not password:
        errors["password"] = "Password is required"


    if errors:
        return JsonResponse({
            "success": False,
            "message": "Validation error",
            "errors": errors
        }, status=400)


    user = authenticate(request, username=username, password=password)


    if user is None:
        return JsonResponse({
            "success": False,
            "message": "Invalid username or password"
        }, status=401)

    login(request, user)


    # Generate JWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)


    redirect_url = "/dashboard/"

    return JsonResponse({
        "success": True,
        "message": "Login successful",
        "data": {
            "user_id": user.id,
            "username": user.username,
            "access": access_token,
            "refresh": refresh_token
        },
        "redirect": redirect_url
    }, status=200)