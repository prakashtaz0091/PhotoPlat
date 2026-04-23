from django.urls import path
from bookings import views

urlpatterns = [
    path("<package_id>/", views.create_booking, name="create_booking"),
    path("", views.list_booking, name="list_booking_page"),
    path("detail/<booking_id>/", views.detail_booking, name="detail_booking_page"),
    path("accept/<booking_id>/", views.accept_booking, name="accept_booking_page"),
    path("reject/<booking_id>/", views.reject_booking, name="reject_booking_page"),
    path("accept/<booking_id>/confirm/", views.confirm_accept_booking, name="confirm_accept_booking_page"),
]