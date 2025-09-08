from django.contrib import admin
from .models import Restaurant
from .models import RestaurantCarouselImage


# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """"
    Admin interface for :model:`restaurant.Restaurant`.

    **Displayed fields:**

    - name
    - city
    - phone_number
    - is_active
    """
    list_display = (
        'name',
        'city',
        'phone_number',
        'is_active',
        'table_capacity',
        'online_capacity'
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RestaurantCarouselImage)
class RestaurantCarouselImageAdmin(admin.ModelAdmin):
    """
    Admin interface for :model:`restaurant.RestaurantCarouselImage`.

    **Displayed fields:**

    - restaurant
    - order
    - caption

    **Features:**

    - Carousel images can be ordered by the 'order' field.
    """
    list_display = ('restaurant', 'order', 'caption')
    list_filter = ('restaurant',)
    ordering = ('restaurant', 'order')
