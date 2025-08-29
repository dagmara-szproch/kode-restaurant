from django.db import models

# Create your models here.
class Restaurant(models.Model):
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
    