# forms.py
from django import forms
from .models import Car, RentalReservation


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'color', 'photo','daily_rate','available']


class RentalReservationForm(forms.ModelForm):
    class Meta:
        model = RentalReservation
        fields = ['rental_start_date', 'rental_end_date', 'car', 'pickup_location','dropoff_location', 'pickup_time', 'return_time', 'car_type']
