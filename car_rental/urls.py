from django.urls import path, include

from car_rental import views

urlpatterns = [
    path('cars/', views.car_list, name='car-list'),
]