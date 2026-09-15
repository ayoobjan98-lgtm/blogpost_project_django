from rest_framework import viewsets

from project.blogpost.models import BlogPost
from project.myapi.permissions import IsAuthenticated
from project.myapi.serializers import BlogPostSerializer



class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [IsAuthenticated]
        return super().get_permissions()
