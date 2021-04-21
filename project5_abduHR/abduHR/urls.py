from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register",views.register,name="register"),
    #path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("landing",views.landing,name="landing"),
    path("export",views.export,name="export"),
    path("edit/<str:empid>",views.edit,name="edit"),
    path("test",views.test,name="test"),
    path("new",views.new,name="new"),
    path("inactive",views.inactive,name="inactive"),
    path("impemp",views.impemp,name="impemp"),
    path("update",views.update,name="update"),
    path("search",views.search,name="search")
]