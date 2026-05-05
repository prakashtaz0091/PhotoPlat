from rest_framework import serializers
from main.models import Package
from bookings.models import Booking

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["package", "email", "phone_number", "fullname", "start_date"]