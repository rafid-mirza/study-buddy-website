from django.db import models


class Example(models.Model):
    example_text = models.CharField(max_length=200)