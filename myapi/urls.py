from django.urls import path
from .views import BlogPostAPIView, BlogPostDetailAPIView,  LoginAPIView, RegisterAPIView, UserInfoLogin

urlpatterns = [
    path("blogpost/", BlogPostAPIView.as_view()),
    path("blogpost/<int:pk>/", BlogPostDetailAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view(), name="api-login"),
    path("auth/register/", RegisterAPIView.as_view(), name="api-register"),
    path("auth/me/", UserInfoLogin.as_view(), name="api-user-info"),

]
