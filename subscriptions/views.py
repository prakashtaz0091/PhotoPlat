from django.shortcuts import redirect, get_object_or_404
from .models import UserSubscriptionBooking, Subscription, UserSubscription
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages


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
    
    
    
    
    
    
    