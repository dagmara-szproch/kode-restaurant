from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/book/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('edit-booking/<int:pk>/', views.edit_booking, name='edit_booking'),
    path('cancel-booking/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]