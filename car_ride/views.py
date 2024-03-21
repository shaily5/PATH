from datetime import datetime
from decimal import Decimal
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
from .models import Customer, Mycar, ContactUs, Booking, Notification
from django.contrib.auth.decorators import login_required
from .forms import SearchForm, AddcarForm, BookingForm, BookingEditForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random
import string

current_time = timezone.now().strftime("%H:%M:%S %d-%m-%Y")
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
            print("current: ", timezone.now())

            try:
                customer = Customer.objects.get(usern=user)
            except Customer.DoesNotExist:
                customer = None
            if customer:
                login_message = f"{current_time}: Hello {user.username}, You have successfully logged into your account."
                Notification.objects.create(user=customer, message=login_message)
            return redirect('car_ride:dashboard')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('car_ride:login')
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

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            messages.warning(request, e.messages[0])
            return render(request, "registration.html")

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
                return redirect('car_ride:login')
            except IntegrityError:
                messages.warning(request, "Account already exists!")
                return redirect('car_ride:register')
        return render(request, "registration.html")

# Home page
def home(request):
    return render(request, "home.html")

@login_required(login_url='login')
def dash(request):
    if request.user.is_authenticated:
        print("from dashboard", request.user)
        return render(request, "dashboard.html")

# @login_required(login_url='login')
def Addcar(request):
    print('Hello1')
    if request.method == 'GET':
        print('Hello2', request.user.is_authenticated, type(request.user))
        if request.user.is_authenticated:
            print('Hello3')
            form = AddcarForm()
            print('Hello4')
            return render(request, "addmycar.html", {'form': form})

    if request.method == 'POST':
        print('Hello5')
        if request.user.is_authenticated:
            form = AddcarForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                form.instance.cust = request.user.customer
                car_name = form.cleaned_data.get('car_name')
                form.save()

                notification_message = f'{current_time}: Your new car {car_name} has been added successfully!'
                Notification.objects.create(user=request.user.customer, message=notification_message)

                return redirect('car_ride:dashboard')
            else:
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

            # Validate from_place and to_place
            if not from_place or not to_place:
                messages.error(request, "Both 'From' and 'To' places are required.")
                return render(request, "search.html", {'form': form})

            # Validate from_date and to_date
            if from_date and to_date and from_date > to_date:
                messages.error(request, "The 'From' date cannot be later than the 'To' date.")
                return render(request, "search.html", {'form': form})

            cars = Mycar.objects.filter(
                Q(from_place__icontains=from_place) &
                Q(to_place__icontains=to_place)
            )

            if from_date:
                cars = cars.filter(from_date=from_date)
            if to_date:
                cars = cars.filter(to_date=to_date)

            if request.user.is_authenticated:
                search_notification = f"{current_time}: You searched for cars from {from_place} to {to_place} for {from_date} to {to_date}"
                Notification.objects.create(user=request.user.customer, message=search_notification)

            return render(request, "searched_cars.html", {'cars': cars})
        else:
            return render(request, "search.html", {'form': form})

def MyBookings(request):
    print("from my booking", request.user, request.method)
    if request.method == 'GET':
        print("-----")
        if request.user.is_authenticated:
            user = request.user
            cust = Customer.objects.get(usern=user)
            print("User:", request.user)
            print("Customer Name:", cust)
            custs = Booking.objects.filter(name=cust, car__isnull=False, car__in=Mycar.objects.all(), pickup__gte=datetime.now())
            # custs = Booking.objects.filter(name=cust)
            print("Bookings", custs)
            context = {'book': custs}
            return render(request, "mybooking.html", context)
    else:
        return HttpResponseForbidden("You are not authorized to perform this action.")

def MyAccount(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            cust = Customer.objects.get(usern=user)
            # print(cust)
            context = {'cust': cust}
            return render(request, "myaccount.html", context)

def Cars(request):
    if request.method == 'GET':
        mycars = Mycar.objects.all()
        return render(request, "allcars.html", {'mycars': mycars})

def MyCarList(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            username = Customer.objects.get(usern=user)
            custs = Mycar.objects.filter(cust=username)
            print("from MyCarList: ", custs)
            context = {'custs': custs}
            return render(request, "mycar_list.html", context)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('car_ride:home')

def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        car = booking.car
        num_seats_canceled = booking.num_seats_booked
        booking.delete()
        car.update_seats_after_cancellation(num_seats_canceled)

        foryou = f"{current_time}: Your booking of {booking.car.cust}'s car {car.car_name} has been canceled"
        forowner = f"{current_time}: User {booking.name.fname} has canceled the booking of your car {booking.car.car_name}"
        Notification.objects.create(user=booking.name, message=foryou)
        Notification.objects.create(user=booking.car.cust, message=forowner)

        print("cancel msg: ", foryou)
        print("message2: ", forowner)

        return render(request, 'cancel_booking.html')
    else:
        return redirect('car_ride:customerbookings')

def Booked(request, car_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            cust = Customer.objects.get(usern=user)
            try:
                book = Booking.objects.filter(car_id=car_id, name=cust)
            except Booking.DoesNotExist:
                messages.error(request, "No booking found for this car yet.")
                return redirect('home')

            # total_price = sum(booking.price for booking in book)
            print("Checking:", book)
            context = {'book': book}
            return render(request, "mybooking.html", context)

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = BookingEditForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            edit_message = f"{current_time}: Your booking details for {booking.car.car_name} have been updated."
            edit_message_owner = f"{current_time}: Booking details for your car {booking.car.car_name} have been updated."
            Notification.objects.create(user=booking.name, message=edit_message)
            Notification.objects.create(user=booking.car.cust, message=edit_message_owner)
            return redirect('car_ride:mybookings')
    else:
        form = BookingEditForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

def Contactus(request):
    if request.method == "GET":
        return render(request, "contact.html")

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['msg']
        if len(phone) != 10 or not phone.isdigit():
            messages.warning(request, "The phone number provided is not 10 digits!")
        elif phone.startswith('0'):
            messages.warning(request, "The phone number provided is not valid!")
        else:
            contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg)
            contact_us.save()
            messages.success(request, "Thank you for contacting us, we will reach you soon.")

        return render(request, "contact.html")

def user_notifications(request):
    if request.user.is_authenticated:
        user = request.user.customer
        notifications = Notification.objects.filter(user=user)
        print("notify: ", notifications)
        context = {'notifications': notifications}
        return render(request, 'user_notifications.html', context)
    else:
        messages.warning(request, "Please log in to see your notifications")
        return redirect('car_ride:login')