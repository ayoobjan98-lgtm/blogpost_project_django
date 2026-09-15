from django.urls import path

from .views import IsAdmin

urlpatterns = [
    path("", IsAdmin),
]
