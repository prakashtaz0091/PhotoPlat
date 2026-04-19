from django import forms
from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("email_verified", "kyc_verified", "rejection_reason", "user", "profile_photo")
        widgets = {
            "fullname": forms.TextInput(attrs={
                "class": "form-input mb-5",
                "placeholder": "Full name",
            }),
            "date_of_birth": forms.DateInput(attrs={
                "class": "form-input mb-5",
                "type": "date",
            }),
            "citizenship_no": forms.TextInput(attrs={
                "class": "form-input mb-5",
                "placeholder": "e.g. 23-01-75-12345",
            }),
            "issued_district": forms.TextInput(attrs={
                "class": "form-input mb-5",
                "placeholder": "e.g. Kathmandu",
            }),
            "permanent_address": forms.TextInput(attrs={
                "class": "form-input mb-5",
                "placeholder": "Ward No., VDC/Municipality, District, Province",
            }),
            "speciality": forms.TextInput(attrs={
                "class": "form-input mb-5",
                "placeholder": "eg. Wedding photoshoot",
            }),
            "citizenship_front": forms.FileInput(attrs={
                "class": "form-input mb-5",
                "accept": "image/*,.pdf",
            }),
            "citizenship_back": forms.FileInput(attrs={
                "class": "form-input mb-5",
                "accept": "image/*,.pdf",
            }),
            "currency": forms.Select(attrs={
                "class": "form-input mb-5"}),
            "per_day_fee": forms.TextInput(attrs={
                "class": "form-input mb-5",
                "placeholder": "Eg. 15000"
                }),
            "specialities": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "mb-5"
                }
            )
        }

    def __init__(self, *args, request=None, **kwargs):
        if request is not None:
            self.request = request
        else:
            raise forms.ValidationError("User not available for KYC, user must be logged in.")
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        cleaned_data = self.cleaned_data.copy()

        # remove many-to-many field before using defaults
        specialities = cleaned_data.pop("specialities", None)

        profile, created = Profile.objects.get_or_create(
            user=self.request.user,
            defaults=cleaned_data
        )

        if not created:
            for key, value in cleaned_data.items():
                if value is not None:
                    setattr(profile, key, value)

        if commit:
            profile.kyc_verified = Profile.KYC_STATUS.IN_REVIEW
            profile.save(*args, **kwargs)

            # handle many-to-many AFTER save
            if specialities is not None:
                profile.specialities.set(specialities)

        return profile
        