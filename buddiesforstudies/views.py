from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from .models import classes, jsonData, Location


def index(request):
    return render(request, 'login.html',{})

def add_class(request):
    model = classes
    return render(request, 'add_class.html')

def submit(request):
    aclass = classes(title = request.POST['title'], user = request.user)
    try:
        classes.objects.get(title = request.POST['title'], user = request.user)
    except (KeyError, classes.DoesNotExist):
        if (aclass.title in jsonData.objects.get(label="classes").classes_list):
            aclass.save()
        else:
            return render(request, 'add_class.html', {'error_message': "That class does not exist."})
    return HttpResponseRedirect(reverse('index'))

def remove_class(request):
    model = classes
    return render(request, 'remove_class.html')

def remove(request):
    try:
        aclass = classes.objects.get(title = request.POST['choice'], user = request.user)
    except (KeyError, classes.DoesNotExist):
        # Redisplay the class removing form.
        return render(request, 'remove_class.html', {'error_message': "You didn't select a class."})
    else:
        aclass.delete()
        return HttpResponseRedirect(reverse('index'))

class AddLocationView(CreateView):
    model = Location
    template_name = "maps.html"
    success_url = "/buddiesforstudies/maps"
    fields = ("location", "address")
