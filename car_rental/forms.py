# forms.py
from django import forms
from .models import Car, RentalReservation, CustomUser, LicenseDetail


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'color', 'photo','daily_rate','available','car_type']


class LicenseDetailForm(forms.ModelForm):
    class Meta:
        model = LicenseDetail
        fields = ['issuing_country', 'issuing_authority', 'birth_date', 'driving_license_number', 'expiry_date']

class RentalReservationForm(forms.ModelForm):
    class Meta:
        model = RentalReservation
        fields = ['rental_start_date', 'rental_end_date', 'pickup_location', 'pickup_time', 'return_time', 'car_type']


class AddNewUser(forms.ModelForm):

    fullname = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))

    cpassword = forms.CharField(max_length=50,
                                required=True,
                                label=("Confirm Password"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'password', 'cpassword']


class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           'id': 'email',
                                                           'name': 'email',
                                                           }))

    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    # remember_me = forms.BooleanField(required=False, label='Remember me?', widget=forms.CheckboxInput(attrs={'class': 'checkbox-input', 'id': 'checkbox1'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

class CarRentalForm(forms.Form):
    PICKUP_LOCATIONS = [
        ('Windsor', 'Windsor'),
        ('Toronto', 'Toronto'),
        ('London', 'London'),
    ]

    CAR_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van'),
    ]

    pickup_location = forms.ChoiceField(choices=PICKUP_LOCATIONS, required=True, widget=forms.Select(attrs={'class': 'input-group1'}))
    pickup_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Pickup Date', 'class': 'input-group1'}), required=True)
    return_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'Return Date', 'class': 'input-group1'}), required=True)
    car_type = forms.ChoiceField(choices=CAR_TYPES, required=True, widget=forms.Select(attrs={'class': 'input-group2'}))
    pickup_time = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'Pickup Time', 'class': 'input-group2'}), required=True)
    return_time = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'Return Time', 'class': 'input-group2'}), required=True)

