from django.urls import path
from . import signup_views, login_views

urlpatterns = [

    path("signup/", signup_views.signup_page, name="signup"),
    path("login/", login_views.login_page, name="login"),

    # APIs
    path("api/signup/", signup_views.signup_api, name="signup-api"),
    path("api/login/", login_views.login_api, name="login-api"),
]