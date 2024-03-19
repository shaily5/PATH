from django.contrib import admin

from .models import Customer, ContactUs, Mycar, Booking, Notification

admin.site.register(Customer)
admin.site.register(ContactUs)
admin.site.register(Mycar)
admin.site.register(Booking)
admin.site.register(Notification)