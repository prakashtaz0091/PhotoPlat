from django.contrib import admin
from main import models
# Register your models here.

admin.site.register(models.Package)

@admin.register(models.APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "value", "active"]