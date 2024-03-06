from django.urls import path, include

from car_rental import views

urlpatterns = [
    path('cars/', views.car_list, name='car-list'),
    path('rental_reservation_list/', views.rental_reservation_list, name='rental_reservation_list'),
]