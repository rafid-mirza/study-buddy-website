from django.contrib import admin
from .models import Example, user, classes

admin.site.register(Example)
admin.site.register(classes)
