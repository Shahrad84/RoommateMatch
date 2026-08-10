from django.urls import path
from . import views

urlpatterns = [
    path("complete/", views.profile_complete, name="profile complete")
]