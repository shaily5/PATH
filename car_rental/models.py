from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.email

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

# Rental Reservation Model
class RentalReservation(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]

    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    customer = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')

    def __str__(self):
        return f"{self.car} - {self.customer} - Status: {self.status}"

class RentalInvoice(models.Model):
    rental_reservation = models.OneToOneField('RentalReservation', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - Total: ${self.amount_due}"