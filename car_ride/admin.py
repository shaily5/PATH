from django.contrib import admin

from .models import Customer, ContactUs, Mycar, Booking

admin.site.register(Customer)
admin.site.register(ContactUs)
admin.site.register(Mycar)
admin.site.register(Booking)