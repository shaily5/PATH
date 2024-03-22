from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Customuser, Notification
from car_ride.models import Customer
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from PATH.forms import ContactForm


def homepage(request):
    print("C Home")
    return render(request, 'PATH/homepage.html')  # Replace 'home.html' with the name of your home template

current_time = timezone.now().strftime("%H:%M:%S %d-%m-%Y")
def LoginUser(request):
    if request.method == "GET":
        return render(request, "PATH/login.html")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("from login", user)
            print("current: ", timezone.now())

            try:
                customer = Customuser.objects.get(username=user)
            except Customuser.DoesNotExist:
                customer = None
            if customer:
                car_type = request.session.get('car_type')

                if car_type is not None:
                    return redirect(reverse('bookRentalCar'))
                    #
                    # return redirect("bookRentalCar")
                else:
                    request.session['username'] = user.username
                    login_message = f"{current_time}: Hello {user.username}, You have successfully logged into your account."
                    Notification.objects.create(user=customer, message=login_message)
                    return redirect('PATH:homepage')
            # return render(request,'PATH/homepage.html',{"username":username})
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('PATH:login')

    return render(request, "PATH/login.html")

def Register(request):
    if request.method == 'GET':
        return render(request, "PATH/register.html")

    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
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
                obj = User.objects.create_user(username=username, email=email, password=password)
                cust = Customuser.objects.create(username=obj, firstname=firstname, email=email, mobile=mobile, gender=gender,
                                               address=address, city=city, state=state)
                # ride = Customer.objects.create(usern=obj, fname=firstname, email=email, mobile=mobile, gender=gender,
                #                                address=address, city=city, state=state)
                # print("check:", ride)

                messages.success(request, "Account created successfully!")
                return redirect('PATH:login')
            except IntegrityError:
                messages.warning(request, "Account already exists!")
                return redirect('PATH:register')
        return render(request, "PATH/register.html")

@login_required
def logoutView(request):
    logout(request)
    return redirect('PATH:homepage')