from django import forms
from django.forms import ModelForm
from .models import Location

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['location', 'address', 'user_1', 'user_3', 'date','time']
        widgets = {
            'date': DateInput(),
            'time': TimeInput()
        }