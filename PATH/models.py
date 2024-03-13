from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128,default='')
    date_of_birth = models.DateField(null=True, blank=True)
    # Add more fields as needed

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        # Check the provided password against the hashed password
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return f"Post:{self.title}"
