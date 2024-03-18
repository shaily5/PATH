from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import CarForm, RentalReservationForm, AddNewUser, LoginForm
from car_rental.models import Car, RentalReservation, RentalInvoice, CustomUser


# views.py

def dashboard(request):
    return render(request, 'car_rental/dashboard.html')

# Create your views here.
def car_list(request):
    cars = Car.objects.all()
    output = ', '.join([str(car) for car in cars])
    return HttpResponse(output)

def rental_reservation_list(request):
    # Retrieve all rental reservations
    reservations = RentalReservation.objects.all()

    # Create a string representation of each reservation
    reservation_strings = [
        f"Car: {reservation.car}, Customer: {reservation.customer}, Status: {reservation.status}"
        for reservation in reservations
    ]

    # Join the reservation strings with line breaks
    response_body = '\n'.join(reservation_strings)

    # Return the response with the reservation information
    return HttpResponse(response_body, content_type='text/plain')

def rental_invoice_detail(request, invoice_number):
    try:
        invoice = RentalInvoice.objects.get(invoice_number=invoice_number)
    except RentalInvoice.DoesNotExist:
        # Handle the case where the invoice does not exist
        return render(request, 'invoice_not_found.html')

    return render(request, 'rental_invoice_detail.html', {'invoice': invoice})

def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another view
    else:
        form = CarForm()
    return render(request, 'car_rental/create_car.html', {'form': form})

def show_photos(request):
    photos = Car.objects.all()
    return render(request, 'car_rental/show_uploaded_image.html', {'cars': photos})

def forgot_password(request):
    return render(request, 'car_rental/authentication/forget_pass.html', )


class CustomLoginView(LoginView):
    form_class = LoginForm()

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


def loginView(request):
    if request.method == "GET":
        return render(request, "car_rental/authentication/login.html")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            print("from login", user)
            return render(request, "car_rental/services/dashboard.html")

        else:
            messages.error(request, "Invalid username or password!")
            return render(request, "car_rental/authentication/login.html")

    return render(request, "car_rental/authentication/login.html")


def signup(request):
    if request.method == 'GET':
        form= AddNewUser()
        return render(request, "car_rental/authentication/signup.html",{'addUserForm':form})

    if request.method == 'POST':
        usern = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password1']
        cpassword = request.POST['password2']

        if password != cpassword:
            msg="Password does not match Confirm Password"
            return render(request, 'car_rental/authentication/signup.html',{'errorMsg': msg})

        form = AddNewUser(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            newUser.save()
            msg = "Data Saved Successfully"
            # form = AddNewUser()
            return render(request, 'car_rental/authentication/login.html', {"msg": msg})
        else:
            msg = "Failed"
            return render(request, 'car_rental/authentication/signup.html', {'SignUpForm': form,'msg':msg})



def rental_reservation_view(request):
    # Retrieve customer's details from the session
    customer_id = request.session.get('customer_id')
    # customer = request.session.get('customer', None)
    if customer_id is None:
        # Redirect or handle the case where customer details are not available in the session
        pass

    if request.method == 'POST':
        form = RentalReservationForm(request.POST)
        if form.is_valid():
            # Save the reservation object
            reservation = form.save(commit=False)
            reservation.customer = customer_id
            reservation.save()
            # Redirect or show success message
    else:
        # Filter available cars based on the selected car type
        selected_car_type = request.GET.get('car_type', None)
        if selected_car_type:
            available_cars = Car.objects.filter(type=selected_car_type)
        else:
            available_cars = Car.objects.all()

        form = RentalReservationForm()

    return render(request, 'car_rental/rental_reservation.html', {'RentalForm': form})
