from django.db import models


class user(models.Model):
    username = ""

class Example(models.Model):
    example_text = models.CharField(max_length=200)