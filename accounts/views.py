import logging
from django.shortcuts import render, redirect, get_object_or_404
from .admin import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile, EmailVerifyOTP
from accounts.forms import ProfileForm
from django.http import JsonResponse
from django.templatetags.static import static
from django.core.mail import send_mail
from django.conf import settings
from accounts.services import send_welcome_email, send_otp_to_user
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .tasks import notify_for_kyc_submission, notify_otp_for_email_verification
from subscriptions.models import Subscription

logger = logging.getLogger(__name__)


@login_required
def verify_email_otp(request):
    if request.method == "POST":
        otp_from_form = request.POST.get("otp")
        try:
            otp_from_db = EmailVerifyOTP.objects.get(user=request.user, otp=otp_from_form)
        except EmailVerifyOTP.DoesNotExist:
            messages.error(request, "OTP check failed, please request new otp and continue")
        else:
            if otp_from_db.is_expired:
                messages.error(request, "OTP is expired. Please follow the process again.")
            else:
                Profile.objects.filter(user=request.user).update(
                    email_verified=Profile.EMAIL_STATUS.VERIFIED
                    )
                otp_from_db.delete()
                messages.success(request, "Email verified successfully.")
        
        return redirect("profile_page")
            
    return render(request, "accounts/verify-email-otp.html")

@login_required
def verify_email_form(request):
    
    if request.method == "POST":
        # otp generate and send
        otp_verify_url = request.build_absolute_uri(reverse("verify_email_otp_page"))
        notify_otp_for_email_verification(user_email=request.user.email, verify_url=otp_verify_url)
        return redirect("verify_email_otp_page")
    
    return render(request, "accounts/verify-email.html")

@login_required
def photographer_profile(request, profile_id):
    # Fetch profile based on profile id
    profile = get_object_or_404(Profile, pk=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/public-profile.html', context)

@login_required
def remove_profile_photo(request):
    try:
        profile = request.user.profile
        profile.profile_photo = None
        profile.save()
    except Exception:
        return JsonResponse({
            "message": "Failed to remove profile photo",
        })
    else:
        return JsonResponse({
            "message": "Successfully removed profile photo",
            "default_url": static("accounts/images/default-profile-pic.png")
        })
    
@login_required
def upload_profile_photo(request):
    if request.method == "POST":
        if len(request.FILES) != 1:
            messages.error(request, "Please submit exactly 1 image file")
            return redirect("profile_page")
        
        image = request.FILES["file"]
        if not image.content_type.startswith('image/'):
            return JsonResponse({
                "message": "Failed to upload profile photo"
            })
        
        profile = request.user.profile
        profile.profile_photo = image
        profile.save()
        return JsonResponse({
            "message": "Profile photo uploaded successfully"
        })

@login_required
def submit_kyc(request):
    if request.method == "POST":
        submitted_form = ProfileForm(request.POST, request.FILES, request=request)
        if submitted_form.is_valid():
            submitted_form.save()
            notify_for_kyc_submission(user_email=request.user.email) # saves tasks metadata in task table in db
            return redirect("profile_page")
        else:
            context = {
                "profile_form": submitted_form
            }
            return render(request, "accounts/profile.html", context)
        

@login_required
def profile_view(request):
    if request.user.profile is not None:
        logger.debug("user.profile: %s", request.user.profile)
        form = ProfileForm(instance=request.user.profile, request=request)
        logger.debug("user_form: %s", form)
        user_subscription = request.user.subscriptions.filter(active=1).first()
        logger.debug("user_subs: %s", user_subscription)
        free_trial = Subscription.objects.get(type__icontains="free")
        logger.debug("free_trial: %s", free_trial)
        free_trial_done = request.user.subscriptions.filter(subscription=free_trial)
        logger.debug("free_trial_done: %s", free_trial_done)
        subscription_plans = Subscription.objects.all()
        logger.debug("subscription_plans: %s", subscription_plans)
        if free_trial_done:
            subscription_plans = subscription_plans.exclude(id=free_trial.id)
        context = {
            "profile_form": form,
            "user_subscription": user_subscription,
            "subscription_plans": subscription_plans,
        }
    else:
        logger.warning("User %s has no profile", request.user)
        form = ProfileForm(request=request)
        context = {
            "profile_form": form,
        }
    return render(request, "accounts/profile.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("login_page")

def login_view(request):
    
    if request.method == "POST":
        print(request.POST)
        user = authenticate(request,
                            email=request.POST.get("email"),
                            password=request.POST.get("password")
                            )
        if user is not None:
            # actual user handling
            login(request, user)
            
            if not request.POST.get("remember"):
                request.session.set_expiry(0)
                
            messages.success(request, "Login successful.")
            return redirect("profile_page")
        else:
            # user doesn't exist handling
            messages.error(request, "User with these credentials doesn't exist")
            return redirect("login_page")
    
    return render(request, "accounts/login.html")
    
def register(request):
    # If post request, post request in this view means, user is trying to submit registeration form
    if request.method == "POST":
        print("this is post request", request.POST)
        submitted_form = UserCreationForm(request.POST)
        
        if submitted_form.is_valid():
            registered_user = submitted_form.save()
            Profile.objects.create(
                user = registered_user
            )
            messages.success(request, "Registration successful. Please login and complete the verification process")
            
            # send notification mail to user
            send_welcome_email(
                [registered_user.email], 
                profile_url=request.build_absolute_uri(reverse("profile_page"))
                )
            
            return redirect("login_page")
        else:
            print("-----------No it's not valid")
            
        return redirect("home_page")
    
    # If get request, give the registration page
    return render(request, "accounts/register.html")