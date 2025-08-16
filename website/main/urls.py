from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home),
    path("home/", views.home),
    path("create-post/", views.create_post, name="create-post"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("ban-user/<int:pk>", views.ban_user, name="ban-user"),
]
