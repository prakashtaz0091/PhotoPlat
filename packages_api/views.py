from rest_framework.generics import ListAPIView, CreateAPIView
from main.models import Package
from .serializers import PackageSerializer, BookingSerializer
from main.auth import APIKeyAuthentication
from rest_framework.response import Response
from datetime import timedelta
from bookings.models import Booking
from django.db.models import Q
from rest_framework import status


class PackageListView(ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    authentication_classes = [APIKeyAuthentication]
    
    
class BookingCreateView(CreateAPIView):
    authentication_classes = [APIKeyAuthentication]
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data to compute derived fields before saving
        package = serializer.validated_data.get("package")
        start_date = serializer.validated_data.get("start_date")

        # Calculate end_date before availability check
        duration = package.duration
        end_date = start_date + timedelta(days=int(duration) - 1)

        # Availability check — active bookings only
        conflict_exists = Booking.objects.filter(
            package=package,
            status__in=["accepted"]
        ).filter(
            Q(start_date__lte=end_date) &
            Q(end_date__gte=start_date)
        ).exists()

        if conflict_exists:
            return Response(
                {"start_date": ["This date is already booked for this package."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save with all snapshot + derived fields
        booking = serializer.save(
            package=package,
            duration=duration,
            end_date=end_date,
            # snapshot fields
            name=package.name,
            no_of_cameras=package.no_of_cameras,
            no_of_staffs=package.no_of_staffs,
            drone_included=package.drone_included,
            free_accessories=package.free_accessories,
            delivery_time=package.delivery_time,
            final_price=package.final_price,
            # status fields
            status="requested",
            author="customer",
        )

        return Response({"message": "Booking created"}, status=status.HTTP_201_CREATED)