from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
class Profile(models.Model):
    
    class EMAIL_STATUS(models.TextChoices):
        PENDING = ("pending", "Pending")
        VERIFIED = ("verified", "Verified")
        
    class KYC_STATUS(models.TextChoices):
        NOT_SUBMITTED = ("not_submitted", "Not Submitted")
        IN_REVIEW = ("in_review", "In Review")
        REJECTED = ("rejected", "Rejected")
        VERIFIED = ("verified", "Verified")
    
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=60, null=True)
    date_of_birth = models.DateField(null=True)
    citizenship_no = models.CharField(max_length=20, null=True) # xx-xx-xx-xxxxx
    issued_district = models.CharField(max_length=30, null=True)
    permanent_address = models.CharField(max_length=100, null=True)
    speciality = models.CharField(max_length=100, null=True)
    
    # documents
    profile_photo = models.ImageField(upload_to="profile_photos", null=True, blank=True)
    citizenship_front = models.ImageField(upload_to="citizenships", null=True, blank=True)
    citizenship_back = models.ImageField(upload_to="citizenships", null=True, blank=True)
    
    # verification
    email_verified = models.CharField(choices=EMAIL_STATUS, default=EMAIL_STATUS.PENDING)
    kyc_verified = models.CharField(choices=KYC_STATUS, default=KYC_STATUS.NOT_SUBMITTED)
    
    # rejection reason
    rejection_reason = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.user.email}'s profile"
    