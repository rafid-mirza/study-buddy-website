from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import classes


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
        aclass.save()
    return HttpResponseRedirect(reverse('index'))

def remove_class(request):
    model = classes
    return render(request, 'remove_class.html')

def remove(request):
    try:
        aclass = classes.objects.get(title = request.POST['choice'], user = request.user)
    except (KeyError, classes.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'remove_class.html', {'error_message': "You didn't select a class."})
    else:
        aclass.delete()
        return HttpResponseRedirect(reverse('index'))