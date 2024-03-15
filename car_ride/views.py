from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
# import mysql.connector as sql
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound, HttpResponse
# from requests import request
from django.contrib.auth.hashers import make_password
from .models import Customer, Mycar, ContactUs, Booking
from django.contrib.auth.decorators import login_required

def LoginUser(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        usern = request.POST['usern']
        password = request.POST['password']

        user = authenticate(request, username=usern, password=password)
        if user is not None:
            login(request, user)
            print("from login", user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    return render(request, "login.html")

def Register(request):
    if request.method == 'GET':
        return render(request, "registration.html")

    if request.method == 'POST':
        usern = request.POST['usern']
        fname = request.POST['fname']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        if len(mobile) != 10 or not mobile.isdigit():
            messages.warning(request, "The phone number provided is not 10 digits!")
        elif mobile.startswith('0'):
            messages.warning(request, "The phone number provided is not valid!")
        else:
            try:
                obj = User.objects.create_user(username=usern, email=email, password=password)
                cust = Customer.objects.create(usern=obj, fname=fname, email=email, mobile=mobile, gender=gender,
                                               address=address, city=city, state=state)
                messages.success(request, "Account created successfully!")
                return redirect('login')
            except IntegrityError:
                messages.warning(request, "Account already exists!")
                return redirect('register')
        return render(request, "registration.html")

# Home page
def home(request):
    return render(request, "home.html")

# Function to show dashboard to the logged in users
@login_required(login_url='login')
def dash(request):
    if request.user.is_authenticated:
        print("from dashboard", request.user)
        return render(request, "dashboard.html")