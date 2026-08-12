from django.urls import path
from . import signup_views, login_views, general_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("overview/", general_views.account_page, name="account-overview"),
    path("signup/", signup_views.signup_page, name="signup"),
    path("login/", login_views.login_page, name="login"),
    path('accounts/logout/', general_views.logout_handle, name='logout'),
    # APIs
    path("api/signup/", signup_views.signup_api, name="signup-api"),
    path("api/login/", login_views.login_api, name="login-api"),
]