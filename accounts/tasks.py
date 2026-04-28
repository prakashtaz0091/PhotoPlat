from background_task import background
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from .services import generate_otp
from .models import EmailVerifyOTP, MyUser


@background(schedule=3)
def notify_for_kyc_submission(user_email):
    # send notification mail to user
    subject = "KYC submission"
    message = "We have successfully received KYC verification request. Please wait 1-2 business days to get verified or any response."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
    print("[EMAIL]: kyc submission notification sent to ", user_email)
    
    
@background(schedule=3)
def notify_otp_for_email_verification(user_email, verify_url=""):
    otp = generate_otp()
    print("OTP generated: ", otp)
    message = """
        <!DOCTYPE html>

        <html>
        <head>
        <meta charset="UTF-8">
        <title>OTP Verification</title>
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
            background-color: #16a34a;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            }
            .content {
            padding: 30px;
            color: #333333;
            line-height: 1.6;
            text-align: center;
            }
            .otp-box {
            display: inline-block;
            margin: 20px 0;
            padding: 15px 25px;
            font-size: 24px;
            letter-spacing: 4px;
            font-weight: bold;
            background: #f3f4f6;
            border-radius: 6px;
            }
            .button {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 22px;
            background-color: #16a34a;
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
        <h1>Verify Your Account</h1>
        </div>

        <div class="content">
        <h2>Hello %s,</h2>
        
        <p>
            Use the One-Time Password (OTP) below to verify your account.  
            This code is valid for the next <strong>10 minutes</strong>.
        </p>
        
        <div class="otp-box">
            %s
        </div>
        
        <p>Or simply click the button below to verify instantly:</p>
        
        <a href="%s" class="button">Verify Here</a>
        
        <p style="margin-top: 25px;">
            If you didn’t request this, you can safely ignore this email.
        </p>
        
        <p>Thanks,<br>Your Team</p>
        </div>

        <div class="footer">
        <p>© 2026 PhotoPlat. All rights reserved.</p>
        </div>

        </div>
        </body>
        </html>
    """ % (user_email, otp, verify_url)
    email = EmailMessage(
        subject="Email Verification",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    print("OTP is sent to ", user_email)
    user = MyUser.objects.get(email=user_email)
    EmailVerifyOTP.objects.update_or_create(
        user=user,
        defaults={
            "otp": otp
        }
    )
    print("OTP updated in database")