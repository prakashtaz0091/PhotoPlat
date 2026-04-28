from background_task import background
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from bookings.models import Booking

@background(schedule=2)
def notify_booking_update_task(to_email, message=""):
    email = EmailMessage(
        subject="Booking Information",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email, # booking created ? -> photographer else client
    )
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    print("Notify booking update send sent ", to_email)
    
    
@background(schedule=5)
def auto_reject_old_bookings():
    print("Scanning old bookings ", timezone.now())
    now = timezone.now()
    rejected_count = Booking.objects.filter(
        created_at__lte=now - timedelta(seconds=settings.AUTO_REJECT_BOOKINGS_INTERVAL),
        status=Booking.STATUS_CHOICES.REQUESTED
        ).update(
            status=Booking.STATUS_CHOICES.REJECTED,
            rejection_reason="Booking request rejected due to photographer's inactivity"
            )
        
    print(f"Auto rejected {rejected_count} bookings due to photographers inactivity")