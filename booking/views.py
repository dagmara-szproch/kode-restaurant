from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib import messages
from .forms import BookingForm, EditBookingForm
from .models import Booking
from restaurant.models import Restaurant


# Create your views here.
def get_current_bookings(
        restaurant,
        booking_date,
        time_slot,
        exclude_booking=None
        ):
    """
    Helper function to calculate the total number of people already booked
    for a restaurant at a specific date and time slot.

    **Parameters:**

    - restaurant
        An instance of :model:`restaurant.Restaurant`.
    - booking_date
        The date to check bookings for.
    - time_slot
        The time slot to check bookings for.
    - exclude_booking (optional)
        An instance of :model:`booking.Booking` to exclude from the count
        (useful when editing an existing booking).

    **Returns:**

    Integer representing the total number of people already booked.
    """
    queryset = Booking.objects.filter(
        restaurant=restaurant,
        booking_date=booking_date,
        time_slot=time_slot,
        status=1
    )

    if exclude_booking:
        queryset = queryset.exclude(pk=exclude_booking.pk)

    return (
        queryset.aggregate(Sum('number_of_people'))['number_of_people__sum']
        or 0
    )


# Create booking
@login_required
def create_booking(request, slug):
    """
    Handle the creation of a new booking for a specific restaurant.

    **Context:**

    ``form``
        An instance of :form:`booking.BookingForm`.
    ``restaurant``
        An instance of :model:`restaurant.Restaurant`.

    **Behaviour:**

    - Validates against double-booking by the same user.
    - Ensures that the restaurant's online capacity is not exceeded.
    - On success, saves the booking and redirects to :view:`my_bookings`.

    **Template:**

    :template:`booking/create_booking.html`
    """
    restaurant = get_object_or_404(Restaurant, slug=slug)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant

            if Booking.objects.filter(
                user=request.user,
                restaurant=restaurant,
                booking_date=booking.booking_date,
                time_slot=booking.time_slot
            ).exclude(status=2).exists():
                form.add_error(
                    'time_slot',
                    "You already have a booking for this restaurant at the "
                    "selected date and time."
                )

            current_bookings = get_current_bookings(
                restaurant,
                booking.booking_date,
                booking.time_slot
            )

            if (current_bookings + booking.number_of_people
                    > restaurant.online_capacity):
                form.add_error(
                    'number_of_people',
                    "The restaurant cannot accommodate your "
                    "booking due to capacity limits. Please choose "
                    "a different time or reduce the number of people."
                )

            if not form.errors:
                booking.save()
                messages.success(request,
                                 "Your booking has been created successfully!"
                                 )
                return redirect('my_bookings')

    else:
        form = BookingForm()

    return render(
        request,
        'booking/create_booking.html',
        {
            'form': form,
            'restaurant': restaurant
        }
    )


# My bookings
@login_required
def my_bookings(request):
    """
    Display a list of bookings made by the logged-in user.

    **Context:**

    ``bookings``
        A queryset of :model:`booking.Booking` for the current user,
        ordered by booking date (newest first) and time slot.

    **Behaviour:**

    - Automatically marks past bookings as 'Completed'.

    **Template:**

    :template:`booking/my_bookings.html`
    """
    today = now().date()
    # Mark past bookings as 'Completed'
    Booking.objects.filter(user=request.user,
                           booking_date__lt=today).update(status=3)

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booking_date', 'time_slot')

    return render(
        request,
        'booking/my_bookings.html',
        {
            'bookings': bookings
        })


# Edit booking
@login_required
def edit_booking(request, pk):
    """
    Handle editing an existing booking.

    **Context:**

    ``form``
        An instance of :form:`booking.EditBookingForm`.
    ``booking``
        An instance of :model:`booking.Booking` being edited.

    **Behaviour:**

    - Allows updating the number of people for a booking.
    - Validates against the restaurant's capacity.
    - Displays success or error messages and redirects to :view:`my_bookings`.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_people = form.cleaned_data['number_of_people']

            current_bookings = get_current_bookings(booking.restaurant,
                                                    booking.booking_date,
                                                    booking.time_slot,
                                                    exclude_booking=booking
                                                    )

            remaining_spots = (
                booking.restaurant.online_capacity - current_bookings
            )

            if new_people > remaining_spots:
                messages.error(
                    request,
                    "Cannot update booking due to capacity limits. "
                    f"Only {remaining_spots} spots left for this time slot."
                )

            else:
                booking.number_of_people = new_people
                booking.save()
                messages.success(
                    request,
                    f"{booking.booking_date} at {booking.time_slot} "
                    "has been updated successfully to "
                    f"{booking.number_of_people} guests."
                )

        else:
            messages.error(request,
                           "There was an error updating your booking. "
                           "Please check the form and try again.")

        return redirect('my_bookings')


# Cancel booking
@login_required
def cancel_booking(request, pk):
    """
    Handle the cancellation of an existing booking.

    **Behaviour:**

    - Sets the booking status to 'Cancelled'.
    - Displays a success message and redirects to :view:`my_bookings`.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.status = 2
    booking.save()
    messages.success(request, "Your booking has been cancelled.")
    return redirect('my_bookings')
