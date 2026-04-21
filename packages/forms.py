from django import forms
from main.models import Package


class PackageForm(forms.ModelForm):
    """
    Form for creating and editing photographer packages.
    All fields are styled with PhotoPlat's warm earthy design system.
    Widget attrs inject Tailwind + custom CSS classes defined in package-form.html.
    """

    class Meta:
        model = Package
        exclude = ["photographer"]  # Set in view via form.instance.photographer = request.user.profile
        widgets = {
            # ── Core Info ──────────────────────────────────────────────
            "name": forms.TextInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. Premium Wedding Coverage",
                "autocomplete": "off",
            }),
            "active": forms.CheckboxInput(attrs={
                "class": "pp-checkbox",
            }),
            "duration": forms.NumberInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. 3",
                "min": "1",
            }),

            # ── Team & Equipment ───────────────────────────────────────
            "no_of_cameras": forms.NumberInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. 2",
                "min": "1",
            }),
            "no_of_staffs": forms.NumberInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. 4",
                "min": "1",
            }),
            "drone_included": forms.CheckboxInput(attrs={
                "class": "pp-checkbox",
            }),

            # ── Deliverables ───────────────────────────────────────────
            "free_accessories": forms.Textarea(attrs={
                "class": "pp-input pp-textarea",
                "placeholder": "e.g. Free 64GB Pendrive, Large photo album (50 pages), 2 framed 16×20 prints",
                "rows": "4",
            }),
            "delivery_time": forms.NumberInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. 14",
                "min": "1",
            }),

            # ── Pricing ────────────────────────────────────────────────
            "price": forms.NumberInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. 95000.00",
                "step": "0.01",
                "min": "0",
            }),
            "discount": forms.NumberInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. 5000.00  (0 if no discount)",
                "step": "0.01",
                "min": "0",
            }),
            "discount_text": forms.TextInput(attrs={
                "class": "pp-input",
                "placeholder": "e.g. Wedding Season Offer",
                "autocomplete": "off",
            }),
            "discount_end_date": forms.DateInput(attrs={
                "class": "pp-input",
                "type": "date",
            }),
        }

        labels = {
            "name": "Package Name",
            "active": "Package is Active",
            "duration": "Duration (days)",
            "no_of_cameras": "Number of Cameras",
            "no_of_staffs": "Number of Staff",
            "drone_included": "Drone Included",
            "free_accessories": "Free Accessories",
            "delivery_time": "Delivery Time (days)",
            "price": "Package Price (NPR)",
            "discount": "Discount Amount (NPR)",
            "discount_text": "Discount Label",
            "discount_end_date": "Offer End Date",
        }

        help_texts = {
            "name": "A clear, marketable name clients will see on your profile.",
            "duration": "How many days the shoot spans.",
            "no_of_cameras": "Total cameras your team will bring.",
            "no_of_staffs": "Total crew members, including yourself.",
            "free_accessories": "List each item on a new line or separated by commas.",
            "delivery_time": "Business days until the client receives final files.",
            "price": "Your full package rate before any discount.",
            "discount": "Enter 0 if there is no discount.",
            "discount_text": "Short label shown on your listing, e.g. 'Wedding Season'.",
            "discount_end_date": "The date your promotional offer expires.",
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        discount = cleaned_data.get("discount")
        discount_text = cleaned_data.get("discount_text")
        discount_end_date = cleaned_data.get("discount_end_date")

        # Discount must not exceed price
        if price is not None and discount is not None:
            if discount >= price:
                self.add_error(
                    "discount",
                    "Discount must be less than the package price."
                )

        # If a discount amount is given, label and end date become required
        if discount and discount > 0:
            if not discount_text:
                self.add_error(
                    "discount_text",
                    "Please provide a short label for this discount offer."
                )
            if not discount_end_date:
                self.add_error(
                    "discount_end_date",
                    "Please set an end date for the discount."
                )

        return cleaned_data