from django.contrib import admin
from django.db.models import Sum
from .models import Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'booking_date', 'time_slot', 'number_of_people', 'get_status', 'spots_left')
    list_filter = ('restaurant', 'status', 'booking_date')
    search_fields = ('user__username', 'restaurant__name', 'special_requests')
    ordering = ('-booking_date', '-time_slot')

    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'Status'

    def spots_left(self, obj):
        if not obj.restaurant:
            return "N/A"

        current_bookings = Booking.objects.filter(
            restaurant=obj.restaurant,
            booking_date=obj.booking_date,
            time_slot=obj.time_slot,
            status=1, # Only count 'Confirmed' bookings
        ).aggregate(Sum('number_of_people'))['number_of_people__sum'] or 0

        return obj.restaurant.online_capacity - current_bookings
