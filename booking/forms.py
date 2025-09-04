from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('booking_date', 'time_slot', 'number_of_people', 'special_requests',)

        widgets = {
            'booking_date': forms.TextInput(attrs={'class': 'flatpickr', 'placeholder': 'Select Date'}),
            'number_of_people': forms.Select(choices=[(i, i) for i in range(1, 7)]), # Allow selection from 1 to 6 people
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests?'}),
        }