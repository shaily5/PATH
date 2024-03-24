from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

class Customer(models.Model):
    usern = models.OneToOneField(User, on_delete=models.CASCADE, max_length=80, unique=True, blank=True)
    fname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=80, unique=True)
    gender = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11, null=False)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    #
    # def __str__(self):
    #     return f"{self.usern} - {self.email}"

    def __str__(self):
        return str(self.fname)

class ContactUs(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80, unique=True, blank=False)
    phone = models.CharField(max_length=11, null=False, blank=True)
    msg = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Mycar(models.Model):
    cust = models.ForeignKey(Customer, max_length=100, blank=True, null=True, on_delete=models.SET_NULL)
    car_num = models.CharField(max_length=10, unique=True)
    company = models.CharField(max_length=30)
    car_name = models.CharField(max_length=30)
    car_type = models.CharField(max_length=30)
    from_place = models.CharField(max_length=30)
    to_place = models.CharField(max_length=30)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    price = models.FloatField()
    car_img = models.ImageField(upload_to="cars", default="", null=True, blank=True)
    total_seats = models.IntegerField()
    seats_booked = models.IntegerField(default=0)
    departure_time = models.TimeField(default=timezone.now)  # Departure time
    arrival_time = models.TimeField(default=timezone.now)  # Arrival time
    is_parcel = models.BooleanField(default=False)
    kilograms = models.FloatField(blank=True, default=0)
    luggage_details = models.CharField(max_length=30)

    def update_seats_after_cancellation(self, num_seats_canceled):
        """
        Method to update total seats and seats booked after a booking is canceled.
        """
        self.seats_booked -= num_seats_canceled
        self.total_seats += num_seats_canceled
        self.save()

    def __str__(self):
        return self.car_num

    @property
    def imageURL(self):
        try:
            url = self.car_img.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.car_img.path)
        if img.height > 1500 or img.width > 1500:
            output_size = (1500, 1500)
            img.thumbnail(output_size)
            img.save(self.car_img.path)

class Booking(models.Model):
    name = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Mycar, on_delete=models.SET_NULL, null=True)
    contact = models.CharField(max_length=11, null=False)
    email = models.EmailField(max_length=80)
    # pickup = models.DateField()
    # dropoff = models.DateField()
    pick_add = models.CharField(max_length=100, null=False)
    drop_add = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    num_seats_booked = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

class Notification(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message)