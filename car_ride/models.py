from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    usern = models.OneToOneField(User, on_delete=models.CASCADE, max_length=80, unique=True, blank=True)
    fname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=80, unique=True)
    gender = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11, null=False)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)

    def _str_(self):
        return str(self.fname)

class ContactUs(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80, unique=True, blank=False)
    phone = models.CharField(max_length=11, null=False, blank=True)
    msg = models.CharField(max_length=200)

    def _str_(self):
        return self.name

