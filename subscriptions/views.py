import requests
import json
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .models import UserSubscriptionBooking, Subscription, UserSubscription
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from django.conf import settings


@login_required
def subs_booking_initiate(request, subs_id):
    subs = get_object_or_404(Subscription, id=subs_id)
    
    # in case of free trial
    if subs.price == Decimal("0.0"): 
        UserSubscription.objects.get_or_create(
            user=request.user,
            subscription=subs
        )
        messages.success(request, "Free trial has been activated")
        return redirect("profile_page")
    
    
    subs_booking, created = UserSubscriptionBooking.objects.get_or_create(
        user=request.user,
        subscription=subs,
        status=UserSubscriptionBooking.STATUS.PENDING,
        defaults={
            "s_type":subs.type,
            "s_valid_no_of_days":subs.valid_no_of_days,
            "s_price":subs.price,
            "s_currency":subs.currency
        }
    )
    
    return_url = request.build_absolute_uri(reverse("khalti_return"))
    website_url = request.build_absolute_uri(reverse("home_page"))
    amount_in_paisa_str = str(subs_booking.s_price*100)
    purchase_order_id = str(subs_booking.id)
    purchase_order_name = subs.type
    fullname = request.user.profile.fullname
    email = request.user.email
    
    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount_in_paisa_str,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": purchase_order_name,
        "customer_info": {
                "name": fullname,
                "email": email,
            }
    })
    
    headers = {
        'Authorization': f"key {settings.KHALTI_API_SECRET}",
        'Content-Type': 'application/json',
    }
    
    response = requests.request("POST", settings.KHALTI_INITIATE_URL, headers=headers, data=payload)
    
    if response.status_code != 200:
        messages.error(request, "Something went wrong !!!")
        return redirect("profile_page")
    
    response_data = response.json()
    pidx = response_data.get("pidx")
    subs_booking.pidx = pidx
    subs_booking.save()
    
    payment_url = response_data.get('payment_url')
    
    return redirect(payment_url)


@login_required
def khalti_return(request):
    pidx = request.GET.get("pidx")
    
    try:
        subs_booking = UserSubscriptionBooking.objects.get(pidx=pidx)
    except UserSubscriptionBooking.DoesNotExist:
        messages.error(request, "Such booking information doesn't exist")
        return redirect("profile_page")

    payload = json.dumps({
        "pidx":pidx
    })
    
    headers = {
        'Authorization': 'key 95f43b44bec34bf1be5f5e4f4adbfdbc',
        'Content-Type': 'application/json',
    }
    
    response = requests.request("POST", settings.KHALTI_LOOKUP_URL, headers=headers, data=payload)
    
    response_data = response.json()
    if response_data.get('status') == "Completed":
        total_amount = Decimal(response_data.get('total_amount'))/100 # convert to ruppees
        if total_amount != subs_booking.s_price:
            messages.error(request, "Payment amount mis-match. Please contact adminstrator")
            return redirect("profile_page")
        
        UserSubscription.objects.create(
            user=request.user,
            subscription=subs_booking.subscription
        )
        subs_booking.status = UserSubscriptionBooking.STATUS.COMPLETED
        messages.success(request, "Subscription purchased successfully")
    elif response_data.get('status') == "Pending":
        messages.error(request, "Something went wrong during payment completion. Please contact administrator to investigate the issue")
    else:
        messages.error(request, "Payment not completed. Please try again")
        subs_booking.status = UserSubscriptionBooking.STATUS.TERMINATED

    subs_booking.khalti_status = response_data.get('status')
    subs_booking.save()
    
    return redirect("profile_page")
        
    
    
    
    
    
    
    