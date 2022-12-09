from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pricing", views.pricing, name="pricing"),
    path("login", views.login_view, name="login_view"),
    path("app", views.app, name="app"),
    path("logout", views.logout_view, name="logout_view"),
    path("outline", views.app_next, name="app_next"),
    path("finish", views.finish, name="finish"),
    path("usage", views.usage, name="usage")
]