from django.shortcuts import render
from django.contrib import admin


def IsAdmin(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return render(request, "403.html", status=403)

    return admin.site.urls(request)