from rest_framework import viewsets

from ..blogpost.models import BlogPost
from myapi.permissions import IsAuthenticated
from myapi.serializers import BlogPostSerializer



class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [IsAuthenticated]
        return super().get_permissions()
