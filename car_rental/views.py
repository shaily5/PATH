from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from PATH.models import Customuser
from .forms import CarForm, RentalReservationForm, AddNewUser, LoginForm, CarRentalForm, LicenseDetailForm
from car_rental.models import Car, RentalReservation, RentalInvoice, CustomUser, LicenseDetail
from django.urls import reverse_lazy

# views.py


def showUserDashboard(request):
    return render(request, 'car_rental/services/userDashboard.html')

def getReservations(request):
    customer = Customuser.objects.get(username__username=request.session['username'])

    reservations = RentalReservation.objects.filter(customer__username__username=request.session['username'])

    for reservation in reservations:
        car = Car.objects.get(pk=reservation.car_id.pk)

        rental_start_date = reservation.rental_start_date
        rental_end_date = reservation.rental_end_date

        # Calculate the number of days by subtracting the start date from the end date
        num_days = (rental_end_date - rental_start_date).days + 1
        reservation.num_days = num_days
        reservation.perDayCharge = car.daily_rate
        reservation.netCharge = (reservation.perDayCharge * num_days)
        reservation.insurance = 25
        reservation.image = car.photo.url
        taxes = (float(reservation.perDayCharge * num_days) + float(25)) * float(
            0.13)  # Add 1 to include both start and end dates
        reservation.taxes = taxes

        reservation.total = float(reservation.taxes) + float(25) + (float(car.daily_rate) * float(num_days))

    return render(request, 'car_rental/services/rentSuccess.html',
                  {"id": customer.pk, 'reservations': reservations})

def dashboard(request):
    data = Car.objects.all()
    return render(request, 'car_rental/dashboard.html',{'cars':data})

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

def getCars(request,param):
    data = Car.objects.filter(car_type=param)
    return render(request, 'car_rental/services/availableCars.html',{'data':data})


def getCarDetail(request,car_id):
    if request.session.get('details_car_id') is None:
        request.session['details_car_id'] = car_id

    if request.session.get('username') is not None:
        car = get_object_or_404(Car, id=car_id)
        data = Car.objects.all()
        return render(request, 'car_rental/services/carDetails.html', {'data': data, 'car': car})
    else:
        return render(request, "PATH/login.html")


def show_photos(request):
    photos = Car.objects.all()
    return render(request, 'car_rental/show_uploaded_image.html', {'cars': photos})

def forgot_password(request):
    return render(request, 'car_rental/authentication/forget_pass.html', )



def authenticate_user(email, password):
    try:
        user = CustomUser.objects.get(email=email)

        if not user:  # Use check_password method to compare passwords securely
            return None # Return user object and success message
        else:
            if password == user.password:
                return user.id, "Authentication Successfull"  # Return None and incorrect password message
            else:
                return None
    except CustomUser.DoesNotExist:
        return None  # Return None and email does not exist message


def homepage(request):
    if request.method == 'POST':
        seats = request.POST.get('seats')

        car_type = request.POST.get('car_type')
        fuel_type = request.POST.get('fuel_type')

        # Filter cars based on the submitted form data
        filtered_cars = Car.objects.filter(seats=seats, car_type=car_type, fuel_type=fuel_type)
        return render(request, "car_rental/services/dashboard.html", {"cars": filtered_cars})
    else:
        # If no filter criteria submitted, display all cars

        data = Car.objects.all()
        return render(request, "car_rental/services/dashboard.html", {"cars": data})


def bookRentalCar(request):

        if request.method == "GET":
            if request.session.get('username') is None:
                return render(request, "PATH/login.html")
            else:
                cars = Car.objects.filter(car_type=request.session.get('car_type'))
                return render(request, "car_rental/services/availableCars.html", {'cars': cars})

        if request.method == "POST":

            # if request.session.get('car_type') is None:

            rental_start_date = request.POST['rental_start_date']
            rental_end_date = request.POST['rental_end_date']
            pickup_time = request.POST['pickup_time']
            return_time = request.POST['return_time']
            pickup_location = request.POST['pickup_location']
            car_type = request.POST['car_type']

            request.session['car_type'] = car_type
            request.session['rental_start_date'] = rental_start_date
            request.session['rental_end_date'] = rental_end_date
            request.session['pickup_time'] = pickup_time
            request.session['return_time'] = return_time
            request.session['pickup_location'] = pickup_location

            if request.session.get('rented_car_id') is not None:

                try:
                    license_detail_exists = LicenseDetail.objects.get(customer__username=request.user.pk)

                    customer = Customuser.objects.get(username__username=request.session['username'])
                    car_type = request.session.get('car_type')
                    rental_start_date = request.session['rental_start_date']
                    rental_end_date = request.session.get('rental_end_date')
                    pickup_time = request.session.get('pickup_time')
                    return_time = request.session.get('return_time')
                    pickup_location = request.session.get('pickup_location')
                    car_id = request.session.get('rented_car_id')
                    car = get_object_or_404(Car, id=car_id)

                    rental_details = RentalReservation(
                        car_type=car_type,
                        rental_start_date=rental_start_date,
                        rental_end_date=rental_end_date,
                        pickup_time=pickup_time,
                        return_time=return_time,
                        pickup_location=pickup_location,
                        car_id=car,
                        customer=customer,
                    )
                    rental_details.save()

                    request.session['car_type'] = None
                    request.session['rental_start_date'] = None
                    request.session['rental_end_date'] = None
                    request.session['pickup_time'] = None
                    request.session['return_time'] = None
                    request.session['pickup_location'] = None
                    request.session['rented_car_id'] = None
                    car_ids = []

                    reservations = RentalReservation.objects.filter(customer__username__username=request.session['username'])

                    for reservation in reservations:
                        car = Car.objects.get(pk=reservation.car_id.pk)

                        rental_start_date = reservation.rental_start_date
                        rental_end_date = reservation.rental_end_date

                        # Calculate the number of days by subtracting the start date from the end date
                        num_days = (rental_end_date - rental_start_date).days + 1
                        reservation.num_days = num_days
                        reservation.perDayCharge = car.daily_rate
                        reservation.netCharge = (reservation.perDayCharge*num_days)
                        reservation.insurance = 25
                        taxes=(float(reservation.perDayCharge*num_days)+float(25))*float(0.13)# Add 1 to include both start and end dates
                        reservation.taxes = taxes
                        reservation.image = car.photo.url
                        reservation.total = float(reservation.taxes) + float(25) + (
                                    float(car.daily_rate) * float(num_days))

                    return render(request, 'car_rental/services/rentSuccess.html',
                                  {"id": customer.pk, 'reservations': reservations})
                except LicenseDetail.DoesNotExist:

                    form = LicenseDetailForm()
                    return render(request, 'car_rental/authentication/licenseDetails.html',
                                  {'LicenseForm': form, 'car_id': request.session.get('rented_car_id'),
                                   'car_type': request.session.get('car_type')})

            if request.session.get('username') is not None:
                cars = Car.objects.filter(car_type=request.session.get('car_type'))
                return render(request, "car_rental/services/availableCars.html", {'cars': cars})
            else:
                return render(request, "PATH/login.html")

def loginView(request):
    #
    # if request.session.get('details_car_id') is not None:
    #     return redirect(getCarDetail)

    if request.method == "GET":
        form=LoginForm()
        return render(request, "car_rental/authentication/login.html",{'LoginForm':form})

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate_user(email, password)
        if user is not None:
            request.session['user_id'] = user
            return render(request, "car_rental/services/dashboard.html",{'id':request.session['user_id']})

        else:
            form = LoginForm()
            errMsg= "Invalid username or password!"
            return render(request, "car_rental/authentication/login.html",{"errMsg":errMsg,'LoginForm':form})


def signup(request):
    if request.method == 'GET':
        form= AddNewUser()
        return render(request, "car_rental/authentication/signup.html",{'addUserForm':form,"msg":''})

    if request.method == 'POST':
        usern = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password != cpassword:
            msg="Password does not match Confirm Password"
            return render(request, 'car_rental/authentication/signup.html',{'errorMsg': msg})

        form = AddNewUser(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            newUser.save()
            msg = "Data Saved Successfully"
            form = LoginForm()
            return render(request, 'car_rental/authentication/login.html', {"LoginForm":form,"msg": msg})
        else:
            msg = "Failed"
            return render(request, 'car_rental/authentication/signup.html', {'SignUpForm': form,'msg':msg})





class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'car_rental/authentication/password_reset.html'
    email_template_name = 'car_rental/authentication/password_reset_email.html'
    subject_template_name = 'car_rental/authentication/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('rentallogin')

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

def license_detail_view(request,car_id,car_type):

    request.session['rented_car_id'] = car_id
    request.session['car_type'] = car_type

    if request.session.get('pickup_time') is None:
        # request.session['user_id'] = user

        return render(request, "car_rental/services/dashboard.html",{'car_id_selected':car_id,'car_type':request.session.get('car_type')})

    if request.method == 'GET':

       try:
            license_detail_exists = LicenseDetail.objects.get(customer__username=request.user.pk)

            customer = Customuser.objects.get(username__username=request.session['username'])
            car_type = request.session.get('car_type')
            rental_start_date = request.session.get('rental_start_date')
            rental_end_date = request.session.get('rental_end_date')
            pickup_time = request.session.get('pickup_time')
            return_time = request.session.get('return_time')
            pickup_location = request.session.get('pickup_location')
            car_id = request.session.get('rented_car_id')
            car = get_object_or_404(Car, id=car_id)

            rental_details = RentalReservation(
                car_type=car_type,
                rental_start_date=rental_start_date,
                rental_end_date=rental_end_date,
                pickup_time=pickup_time,
                return_time=return_time,
                pickup_location=pickup_location,
                car_id=car,
                customer=customer,
            )
            rental_details.save()

            request.session['car_type'] = None
            request.session['rental_start_date'] = None
            request.session['rental_end_date'] = None
            request.session['pickup_time'] = None
            request.session['return_time'] = None
            request.session['pickup_location'] = None
            request.session['rented_car_id'] = None

            reservations = RentalReservation.objects.filter(customer__username__username=request.session['username'])

            for reservation in reservations:
                car = Car.objects.get(pk=reservation.car_id.pk)

                rental_start_date = reservation.rental_start_date
                rental_end_date = reservation.rental_end_date

                # Calculate the number of days by subtracting the start date from the end date
                num_days = (rental_end_date - rental_start_date).days + 1
                reservation.num_days = num_days
                reservation.perDayCharge = car.daily_rate
                reservation.netCharge = (reservation.perDayCharge * num_days)
                reservation.insurance = 25
                reservation.image = car.photo.url
                taxes = (float(reservation.perDayCharge * num_days) + float(25)) * float(
                    0.13)  # Add 1 to include both start and end dates
                reservation.taxes = taxes

                reservation.total = float(reservation.taxes) + float(25) + (float(car.daily_rate) * float(num_days))

            return render(request, 'car_rental/services/rentSuccess.html',
                          {"id": customer.pk, 'reservations': reservations})
       except LicenseDetail.DoesNotExist:

           form = LicenseDetailForm()
           return render(request, 'car_rental/authentication/licenseDetails.html',
                         {'LicenseForm': form, 'car_id': request.session.get('rented_car_id'),'car_type':request.session.get('car_type')})


    if request.method == 'POST':
            issuing_country= request.POST['issuing_country']
            issuing_authority= request.POST['issuing_authority']
            driving_license_number=request.POST['driving_license_number']
            expiry_date=request.POST['expiry_date']
            birth_date=request.POST['birth_date']
            issue_date=request.POST['issue_date']
            customer = Customuser.objects.get(username__username=request.session['username'])

            car_type = request.session.get('car_type')
            rental_start_date = request.session.get('rental_start_date')
            rental_end_date = request.session.get('rental_end_date')
            pickup_time = request.session.get('pickup_time')
            return_time = request.session.get('return_time')
            pickup_location = request.session.get('pickup_location')
            car_id = request.session.get('rented_car_id')

            car = get_object_or_404(Car, id=car_id)

            rental_details = RentalReservation(
                car_type=car_type,
                rental_start_date=rental_start_date,
                rental_end_date=rental_end_date,
                pickup_time=pickup_time,
                return_time=return_time,
                pickup_location=pickup_location,
                car_id=car,
                customer=customer,
            )
            rental_details.save()

            license_detail = LicenseDetail(
                issuing_country=issuing_country,
                issuing_authority=issuing_authority,
                driving_license_number=driving_license_number,
                expiry_date=expiry_date,
                customer=customer,
                birth_date=birth_date,
                issue_date=issue_date,
            )
            license_detail.save()

            request.session['car_type'] = None
            request.session['rental_start_date'] = None
            request.session['rental_end_date'] = None
            request.session['pickup_time'] = None
            request.session['return_time'] = None
            request.session['pickup_location'] = None
            request.session['rented_car_id'] = None

            reservations = RentalReservation.objects.filter(customer__username__username=request.session['username'])

            for reservation in reservations:
                car = Car.objects.get(pk=reservation.car_id.pk)

                rental_start_date = reservation.rental_start_date
                rental_end_date = reservation.rental_end_date

                # Calculate the number of days by subtracting the start date from the end date
                num_days = (rental_end_date - rental_start_date).days + 1
                reservation.num_days = num_days
                reservation.perDayCharge = car.daily_rate
                reservation.netCharge = (reservation.perDayCharge * num_days)
                reservation.insurance = 25
                reservation.image = car.photo.url
                taxes = (float(reservation.perDayCharge * num_days) + float(25)) * float(
                    0.13)  # Add 1 to include both start and end dates
                reservation.taxes = taxes

                reservation.total = float(reservation.taxes) + float(25) + (float(car.daily_rate) * float(num_days))

            return render(request, 'car_rental/services/rentSuccess.html',
                          {"id": customer.pk, 'reservations': reservations})

            # all_reservations = RentalReservation.objects.filter()
