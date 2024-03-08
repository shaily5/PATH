from .models import Ride, BookedRide
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RideForm
from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, 'car_ride/home.html')

def all_rides(request):
    rides = Ride.objects.all()
    return render(request, 'car_ride/all_rides.html', {'rides':rides})

def post_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_rides')
    else:
        form = RideForm()
    return render(request, 'car_ride/post_ride.html', {'form': form})

def edit_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            return redirect('all_rides')
    else:
        form = RideForm(instance=ride)
    return render(request, 'car_ride/edit_ride.html', {'form': form})

def about_us(request):
    return render(request, 'car_ride/about_us.html')

def landing(request):
    return render(request, 'landing.html')

# def all_booked_rides(request):
#     all_booked_rides = BookedRide.objects.filter(passenger_id=request.user.id)
#     return render(request, 'passenger/all_booked_rides.html', {'all_booked_rides': all_booked_rides})

def passenger_home(request):
    return render(request, 'passenger/passenger_home.html')

def passenger_rides(request):
    rides = Ride.objects.all()
    return render(request, 'passenger/passenger_rides.html', {'rides': rides})

def passenger_confirm(request):
    passenger_details = request.POST
    return render(request, 'passenger/passenger_confirm.html', {'passenger_details': passenger_details})

def all_booked_rides(request):

    all_booked_rides = BookedRide.objects.filter(passenger=request.user.id)
    booked_rides_details = []

    for booked_ride in all_booked_rides:
        ride = booked_ride.ride
        rider_name = ride.rider_name
        rider_email = ride.rider_email
        rider_phone = ride.rider_phone
        ride_details = {
            'ride': ride,
            'rider_name': rider_name,
            'rider_email': rider_email,
            'rider_phone': rider_phone,
            'passenger_details': {
                'passenger_name': booked_ride.passenger_name,
                'passenger_email': booked_ride.passenger_email,
                'passenger_phone': booked_ride.passenger_phone,
            }
        }
        booked_rides_details.append(ride_details)

    return render(request, 'passenger/all_booked_rides.html', {'booked_rides_details': booked_rides_details})