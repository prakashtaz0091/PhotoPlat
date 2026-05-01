from django.db import models
from datetime import timedelta
from django.utils import timezone
import uuid


class Subscription(models.Model):
    
    class CURRENCY_CHOICES(models.TextChoices):
        NPR = ('npr', 'रु')
        INR = ('inr', '₹')
        USD = ('usd', '$')
    
    type = models.CharField(max_length=50)
    valid_no_of_days = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES.NPR)
    
    def __str__(self):
        return self.type
    

class UserSubscription(models.Model):
    user = models.ForeignKey("accounts.MyUser", on_delete=models.CASCADE, related_name="subscriptions")
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    active = models.BooleanField(default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    @property
    def expires_on(self):
        return self.created_at + timedelta(days=self.subscription.valid_no_of_days)
    
    @property
    def is_expired(self):
        today = timezone.now().date()
        if today - self.created_at > timedelta(days=self.subscription.valid_no_of_days):
            return True
        
    
    def __str__(self):
        return self.user.email
    
    
class UserSubscriptionBooking(models.Model):
    
    class STATUS(models.TextChoices):
        PENDING = ("pending", "Pending")
        TERMINATED = ("terminated", "Terminated")
        COMPLETED = ("completed", "Completed")
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.MyUser", on_delete=models.CASCADE, related_name="subs_booking")
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    s_type = models.CharField(max_length=50)
    s_valid_no_of_days = models.PositiveIntegerField(null=True)
    s_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    s_currency = models.CharField(default=Subscription.CURRENCY_CHOICES.NPR)
    status = models.CharField(choices=STATUS, default=STATUS.PENDING)
    khalti_status = models.CharField(max_length=50, null=True, help_text="Exact status from khalti")
    pidx = models.CharField(max_length=50, null=True, help_text="Initial payment request id from khalti")
    
    def __str__(self):
        return self.user.email