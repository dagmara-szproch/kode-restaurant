from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Restaurant

CHOICES = (
    (0, 'Pending'),
    (1, 'Confirmed'),
    (2, 'Cancelled'),
    (3, 'Completed'),
)

TIME_SLOTS = (
    ('12:00 PM - 1:30 PM', '12:00 PM - 1:30 PM'),
    ('1.30 PM - 3:00 PM', '1:30 PM - 3:00 PM'),
    ('3:00 PM - 4:30 PM', '3:00 PM - 4:30 PM'),
    ('6:00 PM - 7:30 PM', '6:00 PM - 7:30 PM'),
    ('7:30 PM - 9:00 PM', '7:30 PM - 9:00 PM'),
    ('9:00 PM - 10:30 PM', '9:00 PM - 10:30 PM'),   
)

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_made')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookings_received')
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default='12:00 PM - 1:30 PM')
    number_of_people = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    status = models.IntegerField(choices=CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Booking for {self.user.username} on {self.booking_date} at {self.time_slot} for {self.number_of_people} people."