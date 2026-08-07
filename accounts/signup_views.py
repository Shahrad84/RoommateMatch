import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


def signup_page(request):

    if request.user.is_authenticated:
        return redirect("/dashboard/")

    return render(request, "templates/signup.html")


@csrf_exempt
def signup_api(request):

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
    email = data.get("email")
    password1 = data.get("password")
    password2 = data.get("password2")
    full_name = data.get("fullName")
    age = data.get("age")
    gender = data.get("gender")
    city = data.get("city")
    bio = data.get("bio")


    errors = get_signup_errors(
        username=username,
        email=email,
        password1=password1,
        password2=password2,
        full_name=full_name,
        age=age,
        gender=gender
    )


    if errors:
        return JsonResponse({
            "success": False,
            "message": "Validation error",
            "errors": errors
        }, status=400)



    try:
        age = int(age)

    except (TypeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Age must be a number",
            "errors": {
                "age": "Age must be a number"
            }
        }, status=400)


    try:

        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            name=full_name,
            age=age,
            gender=gender
        )

    except Exception:
        return JsonResponse({
            "success": False,
            "message": "Error creating account"
        }, status=500)


    refresh = RefreshToken.for_user(new_user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)


    redirect_url = "/dashboard/"


    return JsonResponse({

        "success": True,

        "message": "Account created successfully!",

        "data": {
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "name": new_user.name,
            "access": access_token,
            "refresh": refresh_token
        },

        "redirect": redirect_url

    }, status=201)




def get_signup_errors(
    username,
    email,
    password1,
    password2,
    full_name,
    age,
    gender
):

    errors = {}


    # Username
    if not username:
        errors["username"] = "Username is required"

    elif len(username) < 3:
        errors["username"] = (
            "Username must include at least 3 characters"
        )

    elif User.objects.filter(username=username).exists():
        errors["username"] = "Username already taken"


    # Email
    if not email:
        errors["email"] = "Email is required"

    elif User.objects.filter(email=email).exists():
        errors["email"] = "Email already taken"


    # Password
    if not password1:
        errors["password"] = "Password is required"

    elif len(password1) < 6:
        errors["password"] = (
            "Password must include at least 6 characters"
        )

    elif password1 != password2:
        errors["password2"] = "Passwords must be the same"


    # Full name
    if not full_name:
        errors["fullName"] = "Full name is required"


    # Age
    if not age:
        errors["age"] = "Age is required"

    else:

        try:

            age_int = int(age)

            if age_int < 18:
                errors["age"] = (
                    "You must be at least 18 years old"
                )

            elif age_int > 99:
                errors["age"] = (
                    "Age must be less than 100"
                )

        except (TypeError, ValueError):

            errors["age"] = "Age must be a number"


    # Gender
    if not gender:
        errors["gender"] = "Gender is required"

    elif gender not in ["male", "female", "other"]:
        errors["gender"] = "Invalid gender option"


    return errors