from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User
import requests
from django import forms
from mapbox_location_field.models import LocationField, AddressAutoHiddenField

class Location(models.Model):  
    location = LocationField( map_attrs={"center": (-78.50, 38.04)})
    address = AddressAutoHiddenField(default = "")
    def __str__(self):
        return self.address
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1', null = TRUE)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2', null = TRUE)
    user_3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_3', blank = TRUE, null = TRUE)
    date = models.DateField(null=TRUE)
    time = models.TimeField(null=TRUE)


class user_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name =  models.CharField(max_length=128)
    year = models.CharField(max_length=1)
    major = models.CharField(max_length=128)
    level_of_seriousness =  models.CharField(max_length=2)

    def __str__(self):
        return self.name


class user(models.Model):
    username = ""


class Example(models.Model):
    example_text = models.CharField(max_length=200)


class classes(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class jsonData(models.Model):
    label = models.CharField(max_length=128)
    url = 'https://api.devhub.virginia.edu/v1/courses'
    data = requests.get(url).json()
    classes_list = []
    for list in data["class_schedules"]["records"]:
        classes_list.append(list[0] + " " + list[1])


class toggled_classes(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Room(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name
