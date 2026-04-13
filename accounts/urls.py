from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register_page"),
    path("login/", views.login_view, name="login_page"),
    path("logout/", views.logout_view, name="logout_page"),
]