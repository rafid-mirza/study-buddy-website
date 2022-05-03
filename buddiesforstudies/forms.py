from django import forms
from django.forms import ModelForm
from .models import Location, User
from django.db.models import Q
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class LocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        users = kwargs.pop('users')
        super(LocationForm, self).__init__(*args, **kwargs)
        test2 = self.request.user.user_info_set.all()[0].match_students.replace(" ", "").split(",")
        if users != None:
            users = list(user.username for user in users)
            users.remove(self.request.user.username)
            test2 += users
        self.fields['users'].queryset = User.objects.filter(username__in = test2)


    class Meta:
        model = Location
        fields = ['location', 'address', 'date','time','users']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if datetime.datetime.combine(date,time) < datetime.datetime.now():
            msg = "Must be future date"
            self.add_error('date', msg)
            self.add_error('time', msg)
    users = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
