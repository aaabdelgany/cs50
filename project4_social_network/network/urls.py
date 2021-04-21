
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new",views.new,name="new"),
    path("user/<str:username>",views.user, name="user"),
    path("follow",views.follow,name="follow"),
    path("following",views.following,name="following"),
    path("like",views.like,name="like"),
    path("user_like",views.user_like,name="user_like")
]
