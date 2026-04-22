from django.shortcuts import render, redirect
from bookings.forms import BookingForm
from main.models import Package
from bookings.models import Booking
from django.db.models import Q
from datetime import timedelta

def create_booking(request, package_id):
    package = Package.objects.get(id=package_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # attach package
            booking.package = package

            # calculate end_date BEFORE checking availability
            booking.duration = package.duration
            booking.end_date = booking.start_date + timedelta(days=int(package.duration) - 1)

            # availability check
            conflict_exists = Booking.objects.filter(
                package=package,
                status__in=["accepted"]  # active bookings only
            ).filter(
                Q(start_date__lte=booking.end_date) &
                Q(end_date__gte=booking.start_date)
            ).exists()

            if conflict_exists:
                form.add_error("start_date", "This date is already booked for this package.")
            else:
                # snapshot fields
                booking.name = package.name
                booking.no_of_cameras = package.no_of_cameras
                booking.no_of_staffs = package.no_of_staffs
                booking.drone_included = package.drone_included
                booking.free_accessories = package.free_accessories
                booking.delivery_time = package.delivery_time
                booking.final_price = package.final_price

                booking.status = "requested"
                booking.author = "customer"

                booking.save()
                return redirect("home_page")

    else:
        form = BookingForm()

    return render(request, "bookings/booking-create.html", {
        "form": form,
        "package": package
    })