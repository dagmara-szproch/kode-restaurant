from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class Restaurant(models.Model):
    """
    Stores information about a restaurant, including contact details,
    description, table and online capacities.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    table_capacity = models.PositiveIntegerField(default=80)
    online_capacity = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.name


class RestaurantCarouselImage(models.Model):
    """
    Stores a single carousel image related to a :model:`restaurant.Restaurant`,
    including the image file, optional caption, and display order.
    """
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='carousel_images',
        on_delete=models.CASCADE
    )
    image = CloudinaryField('image')
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.restaurant.name} - Image{self.order}"