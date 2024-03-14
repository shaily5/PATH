from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import CarForm
# from .forms import PhotoForm
from .models import Car, RentalReservation, RentalInvoice


def dashboard(request):
    return render(request, 'car_rental/dashboard.html')

# Create your views here.
def car_list(request):
    cars = Car.objects.all()
    output = ', '.join([str(car) for car in cars])
    return HttpResponse(output)

def rental_reservation_list(request):
    # Retrieve all rental reservations
    reservations = RentalReservation.objects.all()

    # Create a string representation of each reservation
    reservation_strings = [
        f"Car: {reservation.car}, Customer: {reservation.customer}, Status: {reservation.status}"
        for reservation in reservations
    ]

    # Join the reservation strings with line breaks
    response_body = '\n'.join(reservation_strings)

    # Return the response with the reservation information
    return HttpResponse(response_body, content_type='text/plain')

def rental_invoice_detail(request, invoice_number):
    try:
        invoice = RentalInvoice.objects.get(invoice_number=invoice_number)
    except RentalInvoice.DoesNotExist:
        # Handle the case where the invoice does not exist
        return render(request, 'invoice_not_found.html')

    return render(request, 'rental_invoice_detail.html', {'invoice': invoice})

def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another view
    else:
        form = CarForm()
    return render(request, 'car_rental/create_car.html', {'form': form})

# def upload_photo(request):
#     if request.method == 'POST':
#         form = PhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('show_photos')
#     else:
#         form = PhotoForm()
#     return render(request, 'car_rental/create_car.html', {'form': form})
#
def show_photos(request):
    photos = Car.objects.all()
    return render(request, 'car_rental/show_uploaded_image.html', {'cars': photos})