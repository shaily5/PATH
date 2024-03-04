from django.urls import path, include

urlpatterns = [
    path('cars/', car_list, name='car-list'),
]