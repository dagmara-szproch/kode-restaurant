from django.urls import path
from . import views
urlpatterns = [
    path('', views.my_booking, name='my_booking'),
]