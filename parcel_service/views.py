from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcel, createParcelRide
from .forms import ParcelForm, CreateParcelRideForm, RideSearchForm
from django.http import HttpResponse
from django.http import JsonResponse
from car_ride.models import Mycar
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# def parcel_list(request):
#     parcels = Parcel.objects.all()
#     return render(request, 'parcel/parcel_list.html', {'parcels': parcels})
#
# def parcel_detail(request, parcel_id):
#     parcel = get_object_or_404(Parcel, pk=parcel_id)
#     return render(request, 'parcel/parcel_detail.html', {'parcel': parcel})
#
# def create_parcel(request):
#     if request.method == 'POST':
#         form = ParcelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('parcel_list')
#     else:
#         form = ParcelForm()
#     return render(request, 'parcel/parcel_form.html', {'form': form})
#
# def create_parcel_ride(request):
#     if request.method == 'POST':
#         form = CreateParcelRideForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#             #return HttpResponse('Your ride is saved.')
#     else:
#         form = CreateParcelRideForm()
#     return render(request, 'parcel/create_parcel_ride.html', {'form': form})
#
#
# def dashboard(request):
#     rides = createParcelRide.objects.all()
#     return render(request, 'parcel/dashboard.html', {'rides': rides})
#
# def dashboard_enduser(request):
#     rides = createParcelRide.objects.all()
#     if request.method == 'POST':
#         form = RideSearchForm(request.POST)
#         if form.is_valid():
#             source = form.cleaned_data['source']
#             destination = form.cleaned_data['destination']
#             rides = createParcelRide.objects.filter(source=source, destination=destination)
#             if not rides:
#                 message = "No ride found."
#             else:
#                 message = ""
#     else:
#         form = RideSearchForm()
#         message = ""
#
#     return render(request, 'parcel/dashboard_enduser.html', {'rides': rides, 'form': form, 'message': message})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcel, createParcelRide
from .forms import ParcelForm, CreateParcelRideForm, RideSearchForm
from django.http import HttpResponse
def parcel_list(request):
    parcels = Parcel.objects.all()
    return render(request, 'parcel/parcel_list.html', {'parcels': parcels})

def parcel_detail(request, parcel_id):
    parcel = get_object_or_404(Parcel, pk=parcel_id)
    return render(request, 'parcel/parcel_detail.html', {'parcel': parcel})

def create_parcel(request):
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parcel_list')
    else:
        form = ParcelForm()
    return render(request, 'parcel/parcel_form.html', {'form': form})

def create_parcel_ride(request):
    if request.method == 'POST':
        form = CreateParcelRideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
            #return HttpResponse('Your ride is saved.')
    else:
        form = CreateParcelRideForm()
    return render(request, 'parcel/create_parcel_ride.html', {'form': form})


# def dashboard(request):
#     rides = createParcelRide.objects.all()
#     return render(request, 'parcel/dashboard.html', {'rides': rides})


@login_required
def dashboard(request):
    # Get the current logged-in user
    user = request.user

    # Query the Mycar model to get all rides posted by the user
    user_rides = Mycar.objects.filter(cust__usern=user)

    # # Pass the user's rides to the template
    # context = {
    #     'user_rides': user_rides
    # }

    return render(request, 'parcel/dashboard.html', {'user_rides': user_rides})

# def dashboard_enduser(request):
#     rides = createParcelRide.objects.all()
#     if request.method == 'POST':
#         form = RideSearchForm(request.POST)
#         if form.is_valid():
#             source = form.cleaned_data['source']
#             destination = form.cleaned_data['destination']
#             rides = createParcelRide.objects.filter(source=source, destination=destination)
#             if not rides:
#                 message = "No ride found."
#             else:
#                 message = ""
#     else:
#         form = RideSearchForm()
#         message = ""
#
#     return render(request, 'parcel/dashboard_enduser.html', {'rides': rides, 'form': form, 'message': message})

def dashboard_enduser(request):
    rides = Mycar.objects.all()

    if request.method == 'POST':
        form = RideSearchForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            date = form.cleaned_data.get('date', None)

            if date:
                rides = rides.filter(from_date=date)
            rides = rides.filter(from_place=source, to_place=destination)

            if not rides:
                message = "No ride found."
            else:
                message = ""
    else:
        form = RideSearchForm()
        message = ""

    return render(request, 'parcel/dashboard_enduser.html', {'rides': rides, 'form': form, 'message': message})

def get_ride_details(request, ride_id):
    try:
        ride = Mycar.objects.get(pk=ride_id)
        data = {
            'car_num': ride.car_num,
            'company': ride.company,
            'car_name': ride.car_name,
            'car_type': ride.car_type,
            'from_place': ride.from_place,
            'to_place': ride.to_place,
            'from_date': ride.from_date,
            'to_date': ride.to_date,
            'price': ride.price,
            'total_seats': ride.total_seats,
            'seats_booked': ride.seats_booked,
            'car_img': ride.car_img.url if ride.car_img else ''  # Assuming car_img is an ImageField
        }
        return JsonResponse(data)
    except Mycar.DoesNotExist:
        return JsonResponse({'error': 'Ride not found'}, status=404)