from django.urls import path
from . import views


urlpatterns = [
    path('packages/', views.PackageListView.as_view(), name="packages_list_api"),
    path('bookings/', views.BookingCreateView.as_view(), name="booking_create_view")
]