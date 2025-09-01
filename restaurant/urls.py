from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # default to home view
    path('<slug:slug>/', views.restaurant_detail, name='restaurant_detail'),
]