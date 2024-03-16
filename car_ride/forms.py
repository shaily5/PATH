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