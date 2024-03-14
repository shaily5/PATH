from django.urls import path
from car_ride import views
urlpatterns=[
    path('register/', views.Register, name="register"),
    path('')
]