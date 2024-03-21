from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class Customuser(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, max_length=80, unique=True, blank=True)
    firstname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=80, unique=True)
    gender = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11, null=False)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.username} - {self.email}"

    def _str_(self):
        return str(self.firstname)


class Notification(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message)
