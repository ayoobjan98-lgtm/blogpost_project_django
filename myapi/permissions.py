from rest_framework.permissions import BasePermission

from django.shortcuts import render

from django.contrib.auth import get_user_model


User = get_user_model()

class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
    
