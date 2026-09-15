from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("add/", views.Add.as_view(), name="add"),
    path("detail/<int:pk>/", views.Detail.as_view(), name="detail"),
    path("recent_posts/", views.RecentPosts.as_view(), name="recent_posts"),
    path("delete/<int:pk>/", views.Delete.as_view(), name="delete"),
    path("update/<int:pk>/", views.Update.as_view(), name="update"),
    path("favorites/", views.Favorites.as_view(), name="favorites"),
    path("my_posts/", views.MyPosts.as_view(), name="my_posts"),
]
