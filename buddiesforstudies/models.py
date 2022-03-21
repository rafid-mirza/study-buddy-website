from django.db import models
from django.contrib.auth.models import User


class user(models.Model):
    username = ""

class Example(models.Model):
    example_text = models.CharField(max_length=200)

class classes(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
