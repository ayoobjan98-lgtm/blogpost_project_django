from django.contrib import admin

from .models import BlogPost, Comment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "datetime_created",
        "datetime_modified",
        "author",
    ]
    list_display_links = [
        "title",
        "datetime_created",
        "datetime_modified",
        "author",
    ]
    filter_horizontal = ["likes"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "hide_name",
        "post",
        "state",
        "datetime_created",
        "datetime_modified",
    ]
    list_display_links = [
        "name",
        "hide_name",
        "post",
        "datetime_created",
        "datetime_modified",
    ]
    list_editable = [
        "state",
    ]
