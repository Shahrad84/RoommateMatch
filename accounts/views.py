from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@csrf_exempt
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "GET":
        return render(request, "templates/signup.html")

    elif request.method == "POST":
        if request.content_type == "application/json":
            return signup_api(request)
        else:
            return signup_submit(request)



def signup_submit(request):

    username = request.POST.get("username")
    email = request.POST.get("email")
    password1 = request.POST.get("password")
    password2 = request.POST.get("password2")
    full_name = request.POST.get('fullName')
    age = request.POST.get('age')
    gender = request.POST.get('gender')


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
        return render(request, "templates/signup.html", {
            "errors": errors,
            "old_data": {
                "username": username,
                "email": email,
                "full_name": full_name,
                "age": age,
                "gender": gender,
            }
        })

    try:
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            name=full_name,
            age=int(age),
            gender=gender
        )
    except Exception as e:
        return render(request, "templates/signup.html", {
            "errors": {"form": f"Error creating account: {str(e)}"}
        })

    return redirect('/accounts/login/')


def get_signup_errors(username, email, password1, password2, full_name, age, gender):

    errors = {}

    # username validation
    if not username:
        errors["username"] = "Username is required"

    elif len(username) < 3:
        errors["username"] = "Username must include at least 3 characters"

    elif User.objects.filter(username=username).exists():
        errors["username"] = "Username already taken"


    # email vaidation
    if not email:
        errors["email"] = "Email is required"
    elif User.objects.filter(email=email).exists():
        errors["email"] = "Email already taken"


    # password validation
    if not password1:
        errors["password1"] = "Password is required"
    elif len(password1) < 6:
        errors["password1"] = "Password must include at least 6 characters"
    elif password1 != password2:
        errors["password2"] = "Passwords must be the same"


    # fullname validation
    if not full_name:
        errors['fullName'] = 'Full name is required'


    # age validation
    if not age:
        errors['age'] = 'Age is required'
    else:
        try:
            age_int = int(age)
            if age_int < 18:
                errors['age'] = 'You must be at least 18 years old'
            elif age_int > 99:
                errors['age'] = 'Age must be less than 100'
        except ValueError:
            errors['age'] = 'Age must be a number'


    # gender validation
    if not gender:
        errors['gender'] = 'Gender is required'
    elif gender not in ['male', 'female', 'other']:
        errors['gender'] = 'Invalid gender option'


    return errors



@csrf_exempt
def signup_api(request):

    data = json.loads(request.body)

    # dig out datas from json
    username = data.get('username')
    email = data.get('email')
    password1 = data.get('password')
    password2 = data.get('password2')
    full_name = data.get('fullName')
    age = data.get('age')
    gender = data.get('gender')


    # valiidate and find errors
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
            'success': False,
            'message': 'Validation error',
            'errors': errors 
        }
        , status=400
        )


    # make new user
    try:
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            name=full_name,
            age=age,
            gender=gender
        )

    except Exception as e:
        return JsonResponse({
            "success" : False,
            "message" : f"error creating account {str(e)}"
        }, status=500)



    # generating jwt
    refresh = RefreshToken.for_user(new_user)

    return JsonResponse({
        'success': True,
        'message': 'Account created successfully!',
        'data': {
            'user_id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    }, status=201)
