from django.urls import path
from bookings import views

urlpatterns = [
    path("<package_id>/", views.create_booking, name="create_booking")
]