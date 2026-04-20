from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group, PermissionsMixin
from main.validators import validate_file_size
from django.utils.text import slugify


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True  # Required for PermissionsMixin
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # Removed manual groups field — PermissionsMixin already provides
    # groups and user_permissions with correct setup

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_admin:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_admin:
            return True
        return super().has_module_perms(app_label)


class Speciality(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        verbose_name_plural = "Specialities"
    
    # wedding.profiles.count()
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        
class Profile(models.Model):
    
    class EMAIL_STATUS(models.TextChoices):
        PENDING = ("pending", "Pending")
        VERIFIED = ("verified", "Verified")
        
    class KYC_STATUS(models.TextChoices):
        NOT_SUBMITTED = ("not_submitted", "Not Submitted")
        IN_REVIEW = ("in_review", "In Review")
        REJECTED = ("rejected", "Rejected")
        VERIFIED = ("verified", "Verified")
    
    
    class CURRENCY_CHOICES(models.TextChoices):
        NPR = ('npr', 'रु')
        INR = ('inr', '₹')
        USD = ('usd', '$')
    

    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=60, null=True)
    date_of_birth = models.DateField(null=True)
    citizenship_no = models.CharField(max_length=20, null=True) # xx-xx-xx-xxxxx
    issued_district = models.CharField(max_length=30, null=True)
    permanent_address = models.CharField(max_length=100, null=True)
    specialities = models.ManyToManyField(Speciality, related_name="profiles")
    
    # documents
    profile_photo = models.ImageField(upload_to="profile_photos", null=True, blank=True, validators=[validate_file_size])
    citizenship_front = models.ImageField(upload_to="citizenships", null=True, blank=True, validators=[validate_file_size])
    citizenship_back = models.ImageField(upload_to="citizenships", null=True, blank=True, validators=[validate_file_size])
    
    # verification
    email_verified = models.CharField(choices=EMAIL_STATUS, default=EMAIL_STATUS.PENDING)
    kyc_verified = models.CharField(choices=KYC_STATUS, default=KYC_STATUS.NOT_SUBMITTED)
    
    # rejection reason
    rejection_reason = models.TextField(null=True, blank=True)
    
    # pricing
    currency = models.CharField(choices=CURRENCY_CHOICES, default="npr")
    per_day_fee = models.PositiveIntegerField(default=0) 
    
    def __str__(self):
        return f"{self.user.email}'s profile"
    