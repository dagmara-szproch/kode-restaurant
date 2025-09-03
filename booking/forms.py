from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('booking_date', 'time_slot', 'number_of_people', 'special_requests',)