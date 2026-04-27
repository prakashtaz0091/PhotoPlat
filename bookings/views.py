from django.shortcuts import render, redirect, get_object_or_404
from bookings.forms import BookingForm
from main.models import Package
from bookings.models import Booking
from django.db.models import Q
from datetime import timedelta
from django.contrib import messages
from . import signals


def confirm_accept_booking(request, booking_id):
    return render(request, "bookings/booking-accept-confirm.html",{
        'booking_id': booking_id
    })

def detail_booking(request, booking_id):
    
    pass

def reject_booking(request, booking_id):
    """
    only allow to reject those bookings whose status is requested
    """
    # print("booking id -------", booking_id)
    booking = get_object_or_404(Booking, id=booking_id, status=Booking.STATUS_CHOICES.REQUESTED)
    booking.status = Booking.STATUS_CHOICES.REJECTED
    booking.save()
    
    return redirect("list_booking_page")

def accept_booking(request, booking_id):
    """
    only allow to accept those bookings whose status is requested
    """
    # print("booking id -------", booking_id)
    booking = get_object_or_404(Booking, id=booking_id, status=Booking.STATUS_CHOICES.REQUESTED)
    
    conflict_exists = Booking.objects.filter(
        package=booking.package,
        status__in=["accepted"]  # active bookings only
    ).filter(
        Q(start_date__lte=booking.end_date) &
        Q(end_date__gte=booking.start_date)
    ).exists()
    
    if conflict_exists:
        messages.error(request, "You are already occupied for this booking date.")
    else:    
        booking.status = Booking.STATUS_CHOICES.ACCEPTED
        booking.save()
        messages.success(request, "Booking accepted successfully. Customer will be notified in few minutes.")
    
    return redirect("list_booking_page")

def list_booking(request):
    
    bookings = Booking.objects.filter(package__photographer__user=request.user)
    return render(request, "bookings/bookings-list.html", {
        'bookings': bookings,
        'requested_count': bookings.filter(status='requested').count(),
        'accepted_count':  bookings.filter(status='accepted').count(),
        'delivered_count': bookings.filter(status='delivered').count(),
    })

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
                messages.success(request, "Package booking requested successfully. Please wait for response")
                return redirect("home_page")

    else:
        form = BookingForm()

    return render(request, "bookings/booking-create.html", {
        "form": form,
        "package": package
    })