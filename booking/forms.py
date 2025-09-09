from django import forms
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
            'booking_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'Select Date'}),
            'number_of_people': forms.Select(choices=[(i, i) for i in range(1, 7)]),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder':'Any special requests?'}),
        }


class EditBookingForm(forms.ModelForm):
    """
    Form for editing an existing :model:`booking.Booking`.

    **Fields:**

    - number_of_people
        Allows updating the number of people for the booking; selectable from 1 to 6.

    **Widgets:**

    - number_of_people: :class:`django.forms.Select`.
    """
    class Meta:
        model = Booking
        fields = ('number_of_people',)
        widgets = {
            'number_of_people': forms.Select(choices=[(i, i) for i in range(1, 7)]),
        }
