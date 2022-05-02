from django import forms
from django.forms import ModelForm
from .models import Location, User
from django.db.models import Q

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class LocationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LocationForm, self).__init__(*args, **kwargs)
        test2 = self.request.user.user_info_set.all()[0].match_students.replace(" ", "").split(",")
        self.fields['users'].queryset = User.objects.filter(username__in = test2)


    class Meta:
        model = Location
        fields = ['location', 'address', 'date','time','users']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }
    users = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
