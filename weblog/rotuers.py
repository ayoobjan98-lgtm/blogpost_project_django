from rest_framework.routers import DefaultRouter

from project.myapi.viewsets import BlogPostViewSet


rotuer = DefaultRouter()

rotuer.register(r"", BlogPostViewSet, basename="blogpost")

urlpatterns = rotuer.urls