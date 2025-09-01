from django.shortcuts import render, get_object_or_404
from .models import Restaurant

# Create your views here.
def home(request):
    """View for the home page. Defaults to the first restaurant. """
    restaurant = Restaurant.objects.first()
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})

def restaurant_detail(request, slug):
    """ Detail page for any restaurant identified by its slug. """
    restaurant = get_object_or_404(Restaurant, slug=slug)
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})