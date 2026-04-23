from django.db import models
from datetime import date, timedelta


class Booking(models.Model):
    
    class STATUS_CHOICES(models.TextChoices):
        REQUESTED = ('requested', 'Requested')
        ACCEPTED = ('accepted', 'Accepted')
        REJECTED = ('rejected', 'Rejected')
        DELIVERED = ('delivered', 'Delivered')
        
    class AUTHOR_CHOICES(models.TextChoices):
        PHOTGRAPHER = ('photographer', 'Photographer')
        CUSTOMER = ('customer', 'Customer')
    
    # booking specific fields
    email = models.EmailField(help_text="Enter email to verify yourself as interested customer")
    phone_number = models.CharField(help_text="Eg. 98********, phone number for verbal communication with photograher", max_length=10)
    fullname = models.CharField(max_length=60, help_text="Your fullname matching citizenship name")
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES.REQUESTED)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(help_text="Booking date", null=True)
    end_date = models.DateField(editable=False, null=True)

    
    # booked package specific snapshot fields
    package = models.ForeignKey("main.Package", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    duration = models.CharField(help_text="Enter duration in days. Eg. 5", default=1)
    no_of_cameras = models.PositiveIntegerField(help_text="No of cameras included in the package", null=True, blank=True)
    no_of_staffs = models.PositiveIntegerField(help_text="No of staffs required for the package", null=True, blank=True)
    drone_included = models.BooleanField(default=False)
    free_accessories = models.TextField(help_text="Eg. Free 32GB pendrive, Free medium size photo album etc.", null=True, blank=True)
    delivery_time = models.PositiveIntegerField(help_text="Enter duration in days when final results will be delivered. Eg. 5 days")
    
    # meta
    author = models.CharField(choices=AUTHOR_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    @property
    def free_accessories_list(self):
        return self.free_accessories.split(sep=",")
    
    @property
    def is_shooting_completed(self):
        return date.today() > self.end_date    
    
    def __str__(self):
        return f"{self.name} Booking"
    
    def save(self, *args, **kwargs):
        if self.start_date and self.duration:
            self.end_date = self.start_date + timedelta(days=int(self.duration) - 1)
        super().save(*args, **kwargs)