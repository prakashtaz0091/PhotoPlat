from django import forms
from bookings.models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "fullname",
            "email",
            "phone_number",
            "start_date",
        ]

        widgets = {
            "fullname": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Your full name (as per citizenship)"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "you@example.com"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "98XXXXXXXX",
                "maxlength": "10"
            }),
            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-input"
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter valid 10 digit phone number.")
        
        if not phone.startswith(("98", "97")):
            raise forms.ValidationError("Phone number format is invalid according to Ncell or NTC")

        return phone