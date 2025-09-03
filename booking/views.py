from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking
from restaurant.models import Restaurant

# Create your views here.
@login_required
def create_booking(request, slug):
    """
    Handle the creation of a new booking for a specific restaurant.
    
    The view retrieves the restaurant based on the provided slug.
    If the request method is POST, it processes the submitted booking form.
    If valid, it saves the booking and redirects to a confirmation page.
    If the request method is GET, it displays an empty booking form.
    """
    restaurant = get_object_or_404(Restaurant, slug=slug)
  
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant # Link booking to the selected restaurant
            booking.save()
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

@login_required
def my_bookings(request):
    """
    Display a list of bookings made by the logged-in user.
    
    The view retrieves all bookings associated with the current user,
    ordered by booking date (newest first) and time slot.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date', 'time_slot')
    return render(
        request, 
        'booking/my_bookings.html',
        {
            'bookings': bookings
        }
)
