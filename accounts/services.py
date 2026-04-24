import random
from django.core.mail import EmailMessage
from django.conf import settings
from accounts.models import EmailVerifyOTP

def generate_otp(length=6):
    chars = "0123456789QWERTYUIOPLKJHGFDSAZXCVBNM"
    otp = "".join([chars[random.randint(0, len(chars)-1)] for _ in range(length)])
    return otp


def send_otp_to_user(user, verify_url=None):
    otp = generate_otp()
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
    """ % (user.email, otp, verify_url)
    email = EmailMessage(
        subject="Email Verification",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    EmailVerifyOTP.objects.update_or_create(
        user=user,
        defaults={
            "otp": otp
        }
    )


def send_welcome_email(recipient_list, profile_url):
    email = EmailMessage(
        subject='Welcome to our platform',
        body="""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <title>Welcome Email</title>
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
                background-color: #4f46e5;
                color: #ffffff;
                padding: 20px;
                text-align: center;
                }
                .content {
                padding: 30px;
                color: #333333;
                line-height: 1.6;
                }
                .button {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 20px;
                background-color: #4f46e5;
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
                <h1>Welcome!</h1>
                </div>
                
                <div class="content">
                <h2>Hello %s,</h2>
                <p>
                    We're excited to have you on board! 🎉  
                    Thanks for joining us — you're now part of something great.
                </p>
                
                <p>
                    Get started by exploring your profile and verifying your email and KYC.
                </p>
                
                <a href="%s" class="button">Get Started</a>
                
                <p style="margin-top: 30px;">
                    If you have any questions, just reply to this email—we're happy to help.
                </p>
                </div>
                
                <div class="footer">
                <p>© 2026 PhotoPlat. All rights reserved.</p>
                </div>
                
            </div>
            </body>
            </html>
        """ % (recipient_list[0], profile_url),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    

if __name__ == "__main__":
    print("-----running services file manually----")
    print(generate_otp(length=8))