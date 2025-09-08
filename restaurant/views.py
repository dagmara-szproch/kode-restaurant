from django.shortcuts import render, get_object_or_404
from .models import Restaurant


# Create your views here.
def home(request):
    """
    Display the home page showing the first available restaurant.

    **Context:**

    ``restaurant``
        An instance of :model:`restaurant.Restaurant`,
        the first restaurant in the database.
    ``carousel_images``
        All carousel images related to the selected restaurant.

    **Template:**

    :template:`restaurant/restaurant_detail.html`
    """
    restaurant = Restaurant.objects.first()
    carousel_images = restaurant.carousel_images.all()
    return render(request, 'restaurant/restaurant_detail.html', {
        'restaurant': restaurant,
        'carousel_images': carousel_images,
        })


def restaurant_detail(request, slug):
    """
    Display details for a specific restaurant identified by its slug.

    **Context**

    ``restaurant``
        An instance of :model:`restaurant.Restaurant` identified by the slug.
    ``carousel_images``
        All carousel images related to the selected restaurant.

    **Template:**

    :template:`restaurant/restaurant_detail.html`
    """
    restaurant = get_object_or_404(Restaurant, slug=slug)
    carousel_images = restaurant.carousel_images.all()
    return render(request, 'restaurant/restaurant_detail.html', {
        'restaurant': restaurant,
        'carousel_images': carousel_images,
    })
