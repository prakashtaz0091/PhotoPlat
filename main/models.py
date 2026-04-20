from django.db import models


class Package(models.Model):
    active = models.BooleanField(default=True)
    photographer = models.ForeignKey("accounts.Profile", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    duration = models.CharField(help_text="Enter duration in days. Eg. 5", default=1)
    no_of_cameras = models.PositiveIntegerField(help_text="No of cameras included in the package", null=True, blank=True)
    no_of_staffs = models.PositiveIntegerField(help_text="No of staffs required for the package", null=True, blank=True)
    drone_included = models.BooleanField(default=False)
    free_accessories = models.TextField(help_text="Eg. Free 32GB pendrive, Free medium size photo album etc.", null=True, blank=True)
    delivery_time = models.PositiveIntegerField(help_text="Enter duration in days when final results will be delivered. Eg. 5 days")
    price = models.DecimalField(decimal_places=2, max_digits=10, help_text="Price of package") #12345678.90
    discount = models.DecimalField(decimal_places=2, max_digits=10, help_text="Discount amount") #12345678.90
    discount_text = models.CharField(max_length=50, help_text="Eg. Wedding season", null=True, blank=True)
    discount_end_date = models.DateField(help_text="Its offer ending date")

    
    class Meta:
        unique_together = ("photographer", "name")
        
        # p1 -> pre-wedding-shoot # right
        # p2 -> pre-wedding-shoot # right
        # p1 -> pre-wedding-shoot # wrong -> duplicate
    
    def __str__(self):
        return self.name    