from django.contrib import admin

from car_ride.models import Customer
from .models import Car,RentalReservation,CustomUser
# Register your models here.

admin.site.register(Car)
admin.site.register(RentalReservation)
admin.site.register(CustomUser)

# admin.site.register(Customer)
