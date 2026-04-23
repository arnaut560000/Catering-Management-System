from django import forms
from django.utils import timezone

from .models import Booking, Feedback


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = css_class
            field.widget.attrs.setdefault("placeholder", field.label)
        self.fields["special_request"].widget.attrs["placeholder"] = "Dietary preferences, theme, setup notes"
        self.fields["selected_drinks"].widget.attrs["placeholder"] = "Iced tea, lemonade, coffee station"

    def clean_booking_date(self):
        booking_date = self.cleaned_data["booking_date"]
        if booking_date < timezone.localdate():
            raise forms.ValidationError("Please choose today or a future date.")
        return booking_date

    class Meta:
        model = Booking
        fields = [
            "customer_name",
            "email",
            "contact_number",
            "booking_date",
            "event_time",
            "number_of_persons",
            "selected_drinks",
            "venue",
            "special_request",
        ]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "event_time": forms.TimeInput(attrs={"type": "time"}),
            "special_request": forms.Textarea(attrs={"rows": 4}),
        }


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = css_class
            field.widget.attrs.setdefault("placeholder", field.label)
        self.fields["comment"].widget.attrs["placeholder"] = "Share what went well and what could be improved."

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    class Meta:
        model = Feedback
        fields = ["customer_name", "booking", "rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 5}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }
