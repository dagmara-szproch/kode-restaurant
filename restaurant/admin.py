from django.contrib import admin
from .models import Restaurant
from .models import RestaurantCarouselImage

# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city', 'phone_number', 'is_active', 'table_capacity', 'online_capacity')

@admin.register(RestaurantCarouselImage)
class RestaurantCarouselImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'order', 'caption')
    list_filter = ('restaurant',)
    ordering = ('restaurant', 'order')