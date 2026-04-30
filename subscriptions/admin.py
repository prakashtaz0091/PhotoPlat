from django.contrib import admin
from subscriptions.models import Subscription, UserSubscription, UserSubscriptionBooking

@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ["type", "price"]
    
    
@admin.register(UserSubscription)
class UserSubscriptionsAdmin(admin.ModelAdmin):
    list_display = ["user", "subscription", "active"]
    
    
@admin.register(UserSubscriptionBooking)
class UserSubscriptionBookingAdmin(admin.ModelAdmin):
    list_display = ["user", "subscription", "status", "khalti_status"]