from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class RegisterDriver(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name

class CarType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Location(models.Model):
    state = models.CharField(max_length=100, choices=[
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('MB', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NT', 'Northwest Territories'),
        ('NS', 'Nova Scotia'),
        ('NU', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Quebec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon'),
    ])
    city = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.city},{self.state}"

class Ride(models.Model):
    rider_name = models.CharField(max_length=100)
    rider_email = models.EmailField()
    rider_phone = models.CharField(max_length=20)
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=100)
    from_location = models.ForeignKey('Location', related_name='from_location_rides', on_delete=models.CASCADE)
    to_location = models.ForeignKey('Location', related_name='to_location_rides', on_delete=models.CASCADE)
    pickup_date = models.DateTimeField(default=datetime.now)
    drop_off_date = models.DateTimeField(default=datetime.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def _str_(self):
        return f"{self.rider_name}'s ride from {self.from_location} to {self.to_location}"

class BookedRide(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    driver = models.ForeignKey(RegisterDriver, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)