from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib import messages
from .forms import BookingForm, EditBookingForm
from .models import Booking
from restaurant.models import Restaurant

# Create your views here.
def get_current_bookings(restaurant, booking_date, time_slot, exclude_booking=None):
    """
    Helper function to return total number of people already booked for a restaurant at a specific date and time.
    Optionally exlude a specific booking (useful when editing an existing booking)."""

    queryset = Booking.objects.filter(
        restaurant=restaurant,
        booking_date=booking_date,
        time_slot=time_slot,
    )
 
    if exclude_booking:
        queryset = queryset.exclude(pk=exclude_booking.pk)

    return queryset.aggregate(Sum('number_of_people'))['number_of_people__sum'] or 0

# Create booking

@login_required
def create_booking(request, slug):
    """
    Handle the creation of a new booking for a specific restaurant.
    Validates against double-booking and restaurant capacity.
    Each booking is linked to the logged-in user and the selected restaurant.
    """
    restaurant = get_object_or_404(Restaurant, slug=slug)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant # Link booking to the selected restaurant

            # check unique booking constraint (User cannot have multiple bookings for the same restaurant at the same date and time)
            if Booking.objects.filter(
                user=request.user, 
                restaurant=restaurant, 
                booking_date=booking.booking_date, 
                time_slot=booking.time_slot
            ).exists():
                form.add_error(
                    None,
                    "You already have a booking for this restaurant at the selected date and time."
                )
         
            # check restaurant capacity (sum of all bookings for the restaurant at the same date and time should not exceed online_capacity)
            current_bookings = get_current_bookings(restaurant, booking.booking_date, booking.time_slot)
            if current_bookings + booking.number_of_people > restaurant.online_capacity:
                form.add_error(
                    'number_of_people', 
                    "The restaurant cannot accommodate your booking due to capacity limits. Please choose a different time or reduce the number of people."
                )

            if not form.errors:
                booking.save()
                messages.success(request, "Your booking has been created successfully!")
                return redirect('my_bookings') # Redirect to a page showing user's bookings

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
    
    The view retrieves all bookings associated with the current user,
    ordered by booking date (newest first) and time slot.

    """
    today = now().date()
    # Mark past bookings as 'Completed'
    Booking.objects.filter(user=request.user, booking_date__lt=today).update(status=3)

    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date', 'time_slot')
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
    Handle the editing of an existing booking via inline JS form.
    Allows updating the number of people for the booking, while ensuring
    that the restaurant's capacity is not exceeded.
    
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = EditBookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_people = form.cleaned_data['number_of_people']

         # check restaurant capacity
            current_bookings = get_current_bookings(booking.restaurant, booking.booking_date, booking.time_slot, exclude_booking=booking)
             # Calculate the difference in number of people

            if current_bookings + new_people > booking.restaurant.online_capacity:
                form.add_error(
                    'number_of_people', 
                    f"Cannot update booking due to capacity limits. "
                    f"Only {booking.restaurant.online_capacity - current_bookings} spots left for this time slot."
                )
            else:
                booking.number_of_people = new_people
                booking.save()
                messages.success(request, f"Your booking for {booking.booking_date} at {booking.time_slot} "
                                          f"has been updated successfully to {booking.number_of_people} guests."
                )

        else: # Form is not valid
            messages.error(request, "There was an error updating your booking. Please check the form and try again.")
        return redirect('my_bookings')


# Cancel booking
@login_required
def cancel_booking(request, pk):
    """
    Handle the cancellation of an existing booking.
    Sets the booking status to 'Cancelled'.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.status = 2  # Set status to 'Cancelled'
    booking.save()
    messages.success(request, "Your booking has been cancelled.")
    return redirect('my_bookings')
