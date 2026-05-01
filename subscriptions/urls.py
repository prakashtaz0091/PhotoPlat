from django.urls import path
from . import views

urlpatterns = [
    path("initate/<subs_id>/", views.subs_booking_initiate, name="subs_booking_initiate")
]