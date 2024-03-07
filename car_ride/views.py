from .models import Ride
from django.contrib import messages
from django.shortcuts import render


def home(request):
    return render(request, 'car_ride/home.html')

def all_rides(request):
    rides = Ride.objects.all()
    return render(request, 'car_ride/all_rides.html', {'rides':rides})

