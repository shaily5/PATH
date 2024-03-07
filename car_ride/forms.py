from django import forms
from .models import Ride

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = 'all'
        widgets = {
            'pickup_date': forms.SelectDateWidget(),
            'drop_off_date': forms.SelectDateWidget(),
                }