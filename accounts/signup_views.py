import json

from django.contrib.auth import get_user_model, login as auth_login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


def build_form_context(values, errors):
    """Builds a plain dict shaped so the existing template's
    {{ form.username.value }} / {% for error in form.username.errors %}
    syntax keeps working (Django templates do dict-key lookup on dots
    too), without needing a Form class.
    """

    values = values or {}
    errors = errors or {}

    field_names = [
        "username", "email", "password", "confirmPassword",
        "fullName", "age", "gender", "city", "bio"
    ]

    form = {}

    for field_name in field_names:
        field_value = values.get(field_name, "")
        field_error = errors.get(field_name)
        form[field_name] = {
            "value": field_value,
            "errors": [field_error] if field_error else []
        }

    form["non_field_errors"] = (
        [errors["__all__"]] if "__all__" in errors else []
    )

    return form


def signup_page(request):

    if request.user.is_authenticated:
        return redirect("/dashboard/")

    errors = {}
    form_values = {}

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password", "")
        password2 = request.POST.get("confirmPassword", "")
        full_name = request.POST.get("fullName", "").strip()
        age = request.POST.get("age", "")
        gender = request.POST.get("gender", "")
        city = request.POST.get("city", "") or None
        bio = request.POST.get("bio", "").strip()

        # Keep whatever the user typed so the form doesn't clear on error
        # (password fields intentionally excluded — never re-fill those)
        form_values = {
            "username": username,
            "email": email,
            "fullName": full_name,
            "age": age,
            "gender": gender,
            "city": city,
            "bio": bio,
        }

        errors = get_signup_errors(
            username=username,
            email=email,
            password1=password1,
            password2=password2,
            full_name=full_name,
            age=age,
            gender=gender
        )

        if not errors:

            try:
                age_int = int(age)

                new_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    name=full_name,
                    age=age_int,
                    gender=gender
                )

            except Exception:
                errors["__all__"] = "Error creating account. Please try again."

            else:
                auth_login(request, new_user)
                return redirect("/dashboard/")

    form = build_form_context(form_values, errors)

    return render(request, "templates/signup.html", {"form": form})


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
        errors["confirmPassword"] = "Passwords must be the same"


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