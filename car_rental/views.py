from django.http import HttpResponse
from django.shortcuts import render

from .models import Car, RentalReservation


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