from datetime import datetime
from django.db import models

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