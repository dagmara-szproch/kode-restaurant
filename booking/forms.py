from django import forms
from datetime import date, timedelta
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form for creating a new :model:`booking.Booking`.

    **Fields:**

    - booking_date
        Date of the booking; uses a flatpickr date picker.
    - time_slot
        Selected time slot for the booking.
    - number_of_people
        Number of people for the booking; selectable from 1 to 6.
    - special_requests
        Optional text area for any special requests.

    **Validates:**

    - `booking_date` cannot be today or a past date,
      and cannot be more than 180 days in advance.
    - `number_of_people` is chosen by the user
      (further capacity checks are handled in views).

    **Widgets:**

    - booking_date: :class:`django.forms.TextInput` with flatpickr styling.
    - number_of_people: :class:`django.forms.Select`.
    - special_requests: :class:`django.forms.Textarea`.
    """
    class Meta:
        model = Booking
        fields = ('booking_date',
                  'time_slot',
                  'number_of_people',
                  'special_requests',)

        widgets = {
            'booking_date': forms.TextInput(attrs={
                'class': 'flatpickr',
                'placeholder': 'Select Date'
            }),
            'number_of_people': forms.Select(
                choices=[(i, i) for i in range(1, 7)]
            ),
            'special_requests': forms.Textarea(attrs={
                'rows': 3, 'placeholder': 'Any special requests?'
            }),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        today = date.today()
        max_date = today + timedelta(days=180)

        if booking_date <= today:
            raise forms.ValidationError(
                "You cannot book for today or a past date."
            )
        if booking_date >= max_date:
            raise forms.ValidationError(
                "You cannot book more than 180 days in advance."
            )

        return booking_date


class EditBookingForm(forms.ModelForm):
    """
    Form for editing an existing :model:`booking.Booking`.

    **Fields:**

    - number_of_people
        Allows updating the number of people for the booking;
        selectable from 1 to 6.

    **Widgets:**

    - number_of_people: :class:`django.forms.Select`.
    """
    class Meta:
        model = Booking
        fields = ('number_of_people',)
        widgets = {
            'number_of_people': forms.Select(
                choices=[(i, i) for i in range(1, 7)]
            ),
        }
