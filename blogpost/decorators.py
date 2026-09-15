from functools import wraps
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from .models import BlogPost


def post_owner_required(view_func):
    """
    Decorator that checks if the user is the owner of the blog post.
    Expects 'pk' in view kwargs.
    """

    @wraps(view_func)
    def _wrapper_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        pk = kwargs.get("pk")
        if not pk:
            raise ValueError(
                "post_owner_required decorator requires 'pk' in URL kwargs"
            )
        post = get_object_or_404(BlogPost, pk=pk)
        if request.user != post.author:
            raise PermissionDenied("You don't have permission to access this post")
        return view_func(request, *args, **kwargs)

    return _wrapper_view
