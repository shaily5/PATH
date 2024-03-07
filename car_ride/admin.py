from django.contrib import admin

from .models import RegisterDriver, CarType, Location, Ride, BookedRide

admin.site.register(RegisterDriver)
admin.site.register(CarType)
admin.site.register(Location)
admin.site.register(Ride)
admin.site.register(BookedRide)
