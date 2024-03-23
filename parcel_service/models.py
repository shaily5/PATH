

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    sender = models.CharField(max_length=150)
    recipient = models.CharField(max_length=150)
    source = models.TextField()
    destination = models.TextField()
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Parcel from {self.source} to {self.destination} - {self.description} (Sender: {self.sender}, Receiver: {self.recipient})"

class createParcelRide(models.Model):
    username = models.CharField(max_length=150)
    source = models.TextField()
    destination = models.TextField()
    description = models.TextField()
class ParcelService(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return f"Parcel from {self.source} to {self.destination}"