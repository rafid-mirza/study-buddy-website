from django.contrib import admin
from .models import Example, user, classes, jsonData, Location
from mapbox_location_field.admin import MapAdmin

admin.site.register(Example)
admin.site.register(classes)
admin.site.register(jsonData)
admin.site.register(Location, MapAdmin)
