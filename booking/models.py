from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from restaurant.models import Restaurant


CHOICES = (
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
    """
    Stores information about a restaurant booking.

    Each booking is linked to a :model:`auth.User`
    and a :model:`restaurant.Restaurant`.

    **Fields:**

    - user
        The user who made the booking.
    - restaurant
        The restaurant that the booking is for.
    - booking_date
        Date of the booking.
    - time_slot
        Time slot for the booking; choices are defined in :const:`TIME_SLOTS`.
    - number_of_people
        Number of people for the booking.
    - special_requests
        Optional special requests from the user.
    - status
        Current status of the booking; choices are :const:`CHOICES`.
        Defaults to 'Confirmed'.
    - created_at
        Timestamp when the booking was created.
    - updated_at
        Timestamp when the booking was last updated.

    **Meta:**

    - Bookings are ordered by `-booking_date` then `time_slot`.
    - Unique constraint prevents a user from double-booking the same restaurant
      at the same date and time slot (applies only to
      Confirmed and Completed bookings).
    - Allows cancelled bookings to be replaced with
      a new booking for the same slot.

    **String representation:**

    Returns a readable description including user, date, time slot,
    and number of people.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='bookings_made')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='bookings_received')
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS,
                                 default='12:00 PM - 1:30 PM')
    number_of_people = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    status = models.IntegerField(choices=CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date', 'time_slot']
        constraints = [
            models.UniqueConstraint(
                fields=["user",
                        "restaurant",
                        "booking_date",
                        "time_slot"],
                condition=Q(status__in=[1, 3]),
                name="unique_booking"
            )
        ]

    def __str__(self):
        return (
            f"Booking for {self.user.username} on {self.booking_date} "
            f"at {self.time_slot} for {self.number_of_people} people."
        )
