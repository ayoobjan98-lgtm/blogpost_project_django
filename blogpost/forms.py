from django import forms
from .models import Comment


class BlogPostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "name",
            "email",
            "address",
            "city",
            "province",
            "zip_code",
            "hide_name",
            "comment",
        ]
