from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcel, createParcelRide
from .forms import ParcelForm, CreateParcelRideForm, RideSearchForm
from django.http import HttpResponse
from django.http import JsonResponse
from car_ride.models import Mycar
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcel, createParcelRide
from .forms import ParcelForm, CreateParcelRideForm, RideSearchForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required




def homepage(request):
    # return render(request, 'parcel/homepage.html')
    return render(request, 'homepage.html')
def parcel_list(request):
    parcels = Parcel.objects.all()
    return render(request, 'parcel/parcel_list.html', {'parcels': parcels})

def parcel_detail(request, parcel_id):
    parcel = get_object_or_404(Parcel, pk=parcel_id)
    return render(request, 'parcel/parcel_detail.html', {'parcel': parcel})

def create_parcel(request, ride_id):
    ride = get_object_or_404(Mycar, pk=ride_id)  # Get the ride object using the ride_id
    if request.method == 'POST':
        form = ParcelForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the parcel with the associated ride
            parcel = form.save(commit=False)
            parcel.sender = form.cleaned_data['sender']
            parcel.requester = request.user
            parcel.ride_id = ride_id
            parcel.receiver = ride.cust.usern
            parcel.source_city = form.cleaned_data['source_city']
            parcel.destination_city = form.cleaned_data['destination_city']
            parcel.save()
            return HttpResponse('Your parcel registration is saved.')
    else:
        form = ParcelForm()
    return render(request, 'parcel/parcel_form.html', {'form': form, 'ride': ride})

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



@login_required
def dashboard(request):
    # Get the current logged-in user
    user = request.user

    # Query the Mycar model to get all rides posted by the user
    user_rides = Mycar.objects.filter(cust__usern=user)
    all_parcel_requests = Parcel.objects.all()
    # # Pass the user's rides to the template
    # context = {
    #     'user_rides': user_rides
    # }

    return render(request, 'parcel/dashboard.html', {'user_rides': user_rides,'all_parcel_requests':all_parcel_requests})

def submit_parcel_request(request, ride_id):
    print("Hello1")
    if request.method == 'POST':
        form_1 = ParcelForm(request.POST, request.FILES)
        print("Hello2")
        if form_1.is_valid():
            parcel_request = form_1.save(commit=False)
            parcel_request.requester = request.user
            parcel_request.ride_id = ride_id
            parcel_request.receiver = Parcel.objects.get(id=ride_id).user
            parcel_request.save()
            return redirect('parcel_service:dashboard_enduser')
            print(form_1)
    else:
        form_1 = ParcelForm()

    return render(request, 'parcel/dashboard_enduser.html', {'form_1': form_1})

def dashboard_enduser(request):
    rides = Mycar.objects.filter(is_parcel=True)
    message = ""
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
    parcel_form = ParcelForm()
    return render(request, 'parcel/dashboard_enduser.html', {'rides': rides, 'form': form, 'message': message, 'parcel_form': parcel_form})

def submit_parcel_request(request, ride_id):
    if request.method == 'POST':
        form_1 = ParcelForm(request.POST, request.FILES)
        if form_1.is_valid():
            parcel_request = form_1.save(commit=False)
            parcel_request.requester = request.user
            parcel_request.receiver = Mycar.objects.get(id=ride_id).cust.user
            parcel_request.save()
            return HttpResponse("Passed for request")
    else:
        form_1 = ParcelForm()

    return render(request, 'parcel/dashboard_enduser.html', {'form_1': form_1})
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
            'kilograms': ride.kilograms,
            'car_img': ride.car_img.url if ride.car_img else ''
        }
        return JsonResponse(data)
    except Mycar.DoesNotExist:
        return JsonResponse({'error': 'Ride not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred', 'message': str(e)}, status=500)


def get_parcel_requests(request, ride_id):
    ride = get_object_or_404(Mycar, pk=ride_id)
    parcel_requests = Parcel.objects.filter(ride_id=ride_id)

    data = {
        'parcel_requests': list(parcel_requests.values()),
        'error': None
    }
    return JsonResponse(data)

def parcel_requests_view(request, ride_id):
    # Get all parcel requests for the specified ride_id
    parcel_requests = Parcel.objects.filter(ride_id=ride_id, is_accepted='Requested')
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        is_accepted = request.POST.get('is_accepted')

        # Update the is_accepted status for the specified request_id
        parcel_request = Parcel.objects.get(id=request_id)
        parcel_request.is_accepted = is_accepted
        parcel_request.save()

        # Redirect to the same page after updating
        return redirect('parcel_service:parcel_request', ride_id=ride_id)
    return render(request, 'parcel/parcel_request.html', {'parcel_requests': parcel_requests})