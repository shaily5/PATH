from django.urls import path, include

from car_rental import views

urlpatterns = [
    path('cars/', views.car_list, name='car-list'),
    path('rental_reservation_list/', views.rental_reservation_list, name='rental_reservation_list'),
    path('invoice/<str:invoice_number>/', views.rental_invoice_detail, name='rental_invoice_detail'),
    path('rental/dashboard/', views.dashboard, name='car-list'),

    path('create_new_car/', views.create_car, name='create_car'),
    path('show_photos/', views.show_photos, name='show_photos')
]