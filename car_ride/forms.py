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
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    car_type = forms.ChoiceField(choices=CAR_TYPE_CHOICES, required=True)
    total_seats = forms.IntegerField(required=True)

    class Meta:
        model = Mycar
        fields = ['car_num', 'company', 'car_name', 'car_type', 'from_place', 'to_place', 'from_date', 'to_date', 'price', 'car_img',  'total_seats']
        labels = {'car_num': 'Car Number'}

    def __init__(self, *args, **kwargs):
        super(AddcarForm, self).__init__(*args, **kwargs)

class SearchForm(forms.ModelForm):
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mycar
        fields = ['from_place', 'to_place', 'from_date', 'to_date']
        labels = {'from_place': 'From Place', 'to_place': 'To Place', 'from_date': 'From Date', 'to_date':'ToDate'}

class BookingForm(forms.ModelForm):
    pickup = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    dropoff = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    num_seats_booked = forms.IntegerField(required=True, min_value=1)

    class Meta:
        model = Booking
        fields = ['contact', 'email', 'pickup', 'dropoff', 'pick_add', 'drop_add', 'num_seats_booked']

class BookingEditForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['contact', 'email', 'pickup', 'dropoff', 'pick_add', 'drop_add']

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username', max_length=100)

class CarForm(forms.ModelForm):
    class Meta:
        model = Mycar
        fields = ['car_name', 'car_type', 'company', 'car_num', 'from_place', 'to_place', 'from_date', 'to_date', 'price','total_seats', 'car_img']