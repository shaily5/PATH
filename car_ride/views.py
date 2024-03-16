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
from .forms import SearchForm, BookingForm

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

# Function to add user's car in the database
# @login_required(login_url='login')
def Addcar(request):
    # print('Hello1')
    if request.method == 'GET':
        # print('Hello2', request.user.is_authenticated, type(request.user))
        if request.user.is_authenticated:
            # print('Hello3')
            form = AddcarForm()
            # print('Hello4')
            return render(request, "addmycar.html", {'form': form})

    if request.method == 'POST':
        # print('Hello5')
        if request.user.is_authenticated:
            form = AddcarForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                form.instance.cust = request.user.customer
                form.save()
                return redirect('dashboard')
            else:
                # If form is invalid, render form again with errors
                return render(request, "addmycar.html", {'form': form})

    return render(request, "addmycar.html")



def CustomerBookings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            cust = Customer.objects.get(usern=user)
            mybook = Booking.objects.filter(name=cust)
            mycar = Mycar.objects.filter(cust=cust)
            otherbookings = Booking.objects.filter(car__in=mycar).exclude(name=cust)
            context = {'otherbookings': otherbookings}
            return render(request, "cust_booking.html", context)


def Search(request):
    if request.method == "GET":
        form = SearchForm()
        return render(request, "search.html", {'form': form})

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            from_place = form.cleaned_data['from_place']
            to_place = form.cleaned_data['to_place']
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']

            # Filter cars based on provided criteria
            cars = Mycar.objects.filter(
                from_place=from_place,
                to_place=to_place,
            )
            if from_date:
                cars = cars.filter(from_date=from_date)
            if to_date:
                cars = cars.filter(to_date=to_date)

            return render(request, "searched_cars.html", {'cars': cars})
        else:
            return render(request, "search.html", {'form': form})