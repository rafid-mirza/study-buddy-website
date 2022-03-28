from django.contrib import admin
from .models import Example, user, classes, jsonData

admin.site.register(Example)
admin.site.register(classes)
admin.site.register(jsonData)
