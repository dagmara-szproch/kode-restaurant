from django.contrib import admin
from .models import Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'booking_date', 'time_slot', 'number_of_people', 'status')