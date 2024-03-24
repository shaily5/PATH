from django import forms
from .models import Mycar, Booking

class AddcarForm(forms.ModelForm):
    CAR_TYPE_CHOICES = [
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
        ('Crossover SUV', 'Crossover SUV'),
        ('Mini Van', 'Mini Van'),
    ]
    LUGGAGE_CHOICES = [
        ('Small (max 7 KG)', 'Small (max 7 KG)'),
        ('Medium (max 15 KG)', 'Medium (max 15 KG)'),
        ('Large (max 23 KG)', 'Large (max 23 KG)'),
    ]
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    car_type = forms.ChoiceField(choices=CAR_TYPE_CHOICES, required=True)
    total_seats = forms.IntegerField(required=True)
    departure_time = forms.CharField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'))
    arrival_time = forms.CharField(required=True, widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'))
    is_parcel = forms.BooleanField(required=False, label='Are you taking Parcel?')
    kilograms = forms.FloatField(required=False, label='Kilograms', initial=0)
    luggage_details = forms.ChoiceField(choices=LUGGAGE_CHOICES, label='Luggage Details')

    class Meta:
        model = Mycar
        fields = ['car_num', 'company', 'car_name', 'car_type', 'from_place', 'to_place', 'from_date', 'to_date', 'departure_time', 'arrival_time', 'price', 'car_img',  'total_seats', 'is_parcel', 'kilograms', 'luggage_details']
        labels = {'car_num': 'Car Number', 'company': 'Company Name', 'car_name': 'Car Name', 'car_type': 'Car Type', 'from_place': 'From Place', 'to_place': 'To Place', 'departure_time': 'Departure Time', 'arrival_time': 'Arrival Time', 'car_img': 'Car Image', 'total_seats': 'Total Seats', 'luggage_details': 'Luggage Details'}


    def __init__(self, *args, **kwargs):
        super(AddcarForm, self).__init__(*args, **kwargs)

class SearchForm(forms.ModelForm):
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mycar
        fields = ['from_place', 'to_place', 'from_date', 'to_date']
        labels = {'from_place': 'From Place', 'to_place': 'To Place', 'from_date': 'From Date', 'to_date':'To Date'}

class BookingForm(forms.ModelForm):
    # pickup = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    # dropoff = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    num_seats_booked = forms.IntegerField(required=True, min_value=1, label='Seats')

    class Meta:
        model = Booking
        # fields = ['contact', 'email', 'pickup', 'dropoff', 'pick_add', 'drop_add', 'num_seats_booked']
        fields = ['contact', 'email', 'pick_add', 'drop_add', 'num_seats_booked']
        labels = {'contact': 'Contact', 'email': 'Email', 'pick_add': 'Pickup Address', 'drop_add': 'Dropoff Address'}

class BookingEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        # fields = ['contact', 'email', 'pickup', 'dropoff', 'pick_add', 'drop_add']
        fields = ['contact', 'email', 'pick_add', 'drop_add']
        labels = {'contact': 'Contact', 'email': 'Email', 'pick_add': 'Pickup Address', 'drop_add': 'Dropoff Address'}

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username', max_length=100)

class CarForm(forms.ModelForm):
    class Meta:
        model = Mycar
        fields = ['car_name', 'car_type', 'company', 'car_num', 'from_place', 'to_place', 'from_date', 'to_date', 'departure_time', 'arrival_time', 'price', 'total_seats']
        labels = {'car_num': 'Car Number', 'company': 'Company Name', 'car_name': 'Car Name', 'car_type': 'Car Type',
                  'from_place': 'From Place', 'to_place': 'To Place',
                  'departure_time': 'Departure Time', 'arrival_time': 'Arrival Time', 'total_seats': 'Total Seats'}