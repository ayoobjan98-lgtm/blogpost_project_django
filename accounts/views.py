from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .forms import ChangeUserForm


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        password = make_password(password1)
        get_user_model().objects.create_user(
            username=username,
            # password=password,
            password=password1,
        )
    return render(request, "registration/signup.html")


def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {"form": form}
    return render(request, "registration/signup.html", context)


def change_user_info(request):
    user = request.user
    form = ChangeUserForm(instance=user)
    if request.method == "POST":
        form = ChangeUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "registration/change_user_info.html", context)
