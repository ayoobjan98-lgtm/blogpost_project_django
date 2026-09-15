from django.urls import path
from .views import BlogPostApiView, PostDetailAPIView


urlpatterns = [
    path("posts/", BlogPostApiView.as_view(), name="api-home"),
    path("post/<int:pk>/", PostDetailAPIView.as_view(), name="api-detail"),


]
