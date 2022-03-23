from django.db import models
from django.contrib.auth.models import User
import requests
import json


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
