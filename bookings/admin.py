from django.contrib import admin
from bookings.models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["name", "fullname","phone_number", "email", "final_price", "status"]
    search_fields = ["name", "fullname", "phone_number"]
    list_filter = ["email"]
