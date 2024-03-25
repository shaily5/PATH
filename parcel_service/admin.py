from django.contrib import admin
from.models import Parcel,createParcelRide, ParcelService, Location
# Register your models here.
admin.site.register(Parcel)
admin.site.register(createParcelRide)
admin.site.register(ParcelService)
admin.site.register(Location)