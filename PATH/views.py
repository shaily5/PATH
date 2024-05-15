from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from car_rental.models import Car
from .models import Customuser, Notification
from car_ride.models import Customer
from django.db import IntegrityError
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from PATH.forms import ContactForm

def homepage(request):
    # print("C Home")
    visit_count = request.session.get('visit_count', 0) + 1
    request.session['visit_count'] = visit_count
    cars = Car.objects.all()
    return render(request, 'PATH/homepage.html',{'cars':cars, 'visit_count': visit_count})  # Replace 'home.html' with the name of your home template

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
                request.session['username']=user.username
                if request.session.get('car_type') is not None:
                    cars = Car.objects.filter(car_type=request.session.get('car_type'))
                    return render(request, "car_rental/services/availableCars.html", {'cars': cars})
                elif request.session.get('details_car_id') is not None:
                    car = get_object_or_404(Car, id=request.session.get('details_car_id'))
                    data = Car.objects.all()
                    return render(request, 'car_rental/services/carDetails.html', {'data': data, 'car': car})

                else:
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
                ride = Customer.objects.create(usern=obj, fname=firstname, email=email, mobile=mobile, gender=gender,
                                               address=address, city=city, state=state)
                print("check:", ride)
                messages.success(request, "Account created successfully!")
                return redirect('PATH:login')
            except IntegrityError:
                messages.warning(request, "Account already exists!")
                return redirect('PATH:register')
        return render(request, "PATH/register.html")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'PATH/authentication/password_reset.html'
    email_template_name = 'PATH/authentication/password_reset_email.html'
    subject_template_name = 'PATH/authentication/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('PATH:login')

@login_required
def logoutView(request):
    logout(request)
    return redirect('PATH:homepage')