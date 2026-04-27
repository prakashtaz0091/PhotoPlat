from django.db.models.signals import post_save
from django.dispatch import receiver
from bookings.models import Booking
from django.core.mail import EmailMessage
from django.conf import settings
from main.middlewares import get_current_request
from django.urls import reverse


BOOKING_REQUEST_TEMPLATE = """
    <!DOCTYPE html>

    <html>
    <head>
    <meta charset="UTF-8">
    <title>New Booking Request</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f4f4f7;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .header {
            background-color: #2563eb;
            color: #ffffff;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 30px;
            color: #333333;
            line-height: 1.6;
        }
        .highlight-box {
            margin: 20px 0;
            padding: 15px;
            background: #f3f4f6;
            border-radius: 6px;
        }
        .button {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 22px;
            background-color: #2563eb;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .footer {
            padding: 20px;
            font-size: 12px;
            color: #888888;
            text-align: center;
            background-color: #f9f9fb;
        }
    </style>
    </head>

    <body>
    <div class="container">

        <div class="header">
            <h1>New Booking Request</h1>
        </div>

        <div class="content">
            <p>Hello,</p>

            <p>
                You have received a new photography package booking request.
            </p>

            <div class="highlight-box">
                <p><strong>Package:</strong> %s</p>
                <p><strong>Name:</strong> %s</p>
                <p><strong>Email:</strong> %s</p>
                <p><strong>Requested Date:</strong> %s</p>
                <p><strong>Till Date:</strong> %s</p>
            </div>

            <p>
                The client has requested to book one of your photography packages.
                Please review the request and take appropriate action.
            </p>

            <p style="text-align: center;">
                <a href="%s" class="button">View Booking Request</a>
            </p>

            <p style="margin-top: 25px;">
                If you were not expecting this request, you can safely ignore this email.
            </p>

            <p>Best regards,<br>PhotoPlat Team</p>
        </div>

        <div class="footer">
            <p>© 2026 PhotoPlat. All rights reserved.</p>
        </div>

    </div>
    </body>
    </html>
    """
BOOKING_UPDATE_TEMPLATE = """
    <!DOCTYPE html>

    <html>
    <head>
    <meta charset="UTF-8">
    <title>Booking Request Status</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f4f4f7;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .header {
            background-color: #2563eb;
            color: #ffffff;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 30px;
            color: #333333;
            line-height: 1.6;
        }
        .highlight-box {
            margin: 20px 0;
            padding: 15px;
            background: #f3f4f6;
            border-radius: 6px;
        }
        .button {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 22px;
            background-color: #2563eb;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .footer {
            padding: 20px;
            font-size: 12px;
            color: #888888;
            text-align: center;
            background-color: #f9f9fb;
        }
    </style>
    </head>

    <body>
    <div class="container">

        <div class="header">
            <h1>Booking request status</h1>
        </div>

        <div class="content">
            <p>Hello,</p>

            <p>
                %s
            </p>

            <div class="highlight-box">
                <p><strong>Package:</strong> %s</p>
                <p><strong>Current Status</strong> %s</p>
            </div>

            <p>Best regards,<br>PhotoPlat Team</p>
        </div>

        <div class="footer">
            <p>© 2026 PhotoPlat. All rights reserved.</p>
        </div>

    </div>
    </body>
    </html>
    """


@receiver(post_save, sender=Booking)
def notify_booking_update(sender, instance, created, **kwargs):
    
    if created:
        request = get_current_request()
        booking_management_uri = request.build_absolute_uri(reverse("list_booking_page"))
        message = BOOKING_REQUEST_TEMPLATE % (
            instance.name,
            instance.fullname,
            instance.email,
            instance.start_date,
            instance.end_date,
            booking_management_uri
            )
        to = [instance.package.photographer.user.email]
    else:
        message_text = ""
        if instance.status == Booking.STATUS_CHOICES.REJECTED:
            message_text = "Your booking request has been rejected by photographer."
        elif instance.status == Booking.STATUS_CHOICES.ACCEPTED:
            message_text = "Your booking request has been accepted. Please contact photographer for any further discussions of the event."
        elif instance.status == Booking.STATUS_CHOICES.DELIVERED:
            message_text = "Your event final result is set to delivered. But if you haven't got your results yet, please contact to the support (XXXXXXXX) PhotoPlat"
        message = BOOKING_UPDATE_TEMPLATE % (
            message_text,
            instance.name,
            instance.get_status_display()
            ) 
        to = [instance.email]
        
    email = EmailMessage(
        subject="Booking Information",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to, # booking created ? -> photographer else client
    )
    email.content_subtype = "html"  # Main content is now text/html
    email.send()