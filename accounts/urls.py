from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("change_user_info/", views.change_user_info, name="change_user_info"),
]
