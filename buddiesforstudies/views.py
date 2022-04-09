from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import classes, jsonData, toggled_classes


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
        aclass2 = toggled_classes.objects.get(title=request.POST['choice'], user=request.user)
    except (KeyError, classes.DoesNotExist):
        # Redisplay the class removing form.
        return render(request, 'remove_class.html', {'error_message': "You didn't select a class."})
    except toggled_classes.DoesNotExist:
        aclass.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        aclass.delete()
        aclass2.delete()
        return HttpResponseRedirect(reverse('index'))

def toggle_class(request):
    model = toggled_classes
    return render(request, 'toggle_class.html')

def toggle(request):
    if request.method == 'POST':
        choice = request.POST.getlist('choice')
        if not choice:
            return render(request, 'toggle_class.html', {'error_message': "You didn't select a class."})
        else:
            for i in choice:
                if toggled_classes.objects.filter(title=i,user=request.user).exists():
                    return render(request, 'toggle_class.html', {'error_message': "One or more of these classes has already been toggled."})
                else:
                    class_to_toggle = toggled_classes(title=i, user=request.user)
                    class_to_toggle.save()
            return HttpResponseRedirect(reverse('index'))
def untoggle_class(request):
    model = toggled_classes
    return render(request, 'untoggle_class.html')

def untoggle(request):
    if request.method == 'POST':
        choice = request.POST.getlist('choice')
        if not choice:
            return render(request, 'untoggle_class.html', {'error_message': "You didn't select a class."})
        else:
            for i in choice:
                    class_to_untoggle = toggled_classes.objects.get(title = i, user = request.user)
                    class_to_untoggle.delete()
            return HttpResponseRedirect(reverse('index'))



