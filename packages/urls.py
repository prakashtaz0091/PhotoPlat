from django.urls import path
from packages import views

urlpatterns = [
    path("", views.packages, name="packages_page"),
    path("create/", views.packages_create, name="packages_create_page"),
]