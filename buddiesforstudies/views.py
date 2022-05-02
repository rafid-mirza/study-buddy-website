from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from .models import classes, jsonData, toggled_classes, Room
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import classes, jsonData, toggled_classes, Location, user_info
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LocationForm
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html',{})
    return render(request, 'login.html',{
        'locations': Location.objects.filter(users__in = [request.user]).order_by('date', 'time')
        })

def input_information(request):
    model = user_info
    return render(request, 'info_retrieve.html')

def info_submit(request):
    major_input = request.POST.get('major').upper()
    level_of_seriousness_input = request.POST.get('seriousness')
    name_input = request.POST.get('name')
    year_input = request.POST.get('year')

    if len(name_input) > 128:
        return render(request, 'info_retrieve.html', {'error_message': "Name cannot exceed 128 characters"})
    if len(major_input) > 128:
        return render(request, 'info_retrieve.html', {'error_message': "Major title cannot exceed 128 characters"})
    not_a_number = False
    try:
        float(year_input)
    except ValueError:
        not_a_number = True
    if len(year_input) > 1 or not_a_number:
        return render(request, 'info_retrieve.html', {'error_message': "Year must be a number 1-9"})
    not_a_number = False
    try:
        float(level_of_seriousness_input)
    except ValueError:
        not_a_number = True
    if (len(level_of_seriousness_input) > 1 and level_of_seriousness_input != "10") or not_a_number:
        return render(request, 'info_retrieve.html', {'error_message': "Interest must be a number 1-10"})
    queryset = user_info.objects.filter(user = request.user)
    if len(queryset) > 0:
        queryset[0].delete()
    ainfo = user_info(major = major_input, level_of_seriousness = level_of_seriousness_input, name = name_input, year = year_input, user = request.user, match_students = "")
    ainfo.save()
    return HttpResponseRedirect(reverse('matching'))

def classes_view(request):
    return render(request, 'classes_view.html')

def add_class(request):
    model = classes
    return render(request, 'add_class.html')


def submit(request):
    aclass = classes(title = request.POST['title'].upper(), user = request.user)
    try:
        classes.objects.get(title = request.POST['title'].upper(), user = request.user)
    except (KeyError, classes.DoesNotExist):
        if aclass.title in jsonData.objects.get(label="classes").classes_list:
            aclass.save()
        else:
            return render(request, 'add_class.html', {'error_message': "That class does not exist."})
    return HttpResponseRedirect(reverse('classes_view'))


def remove_class(request):
    model = classes
    return render(request, 'remove_class.html')


def remove(request):
    try:
        aclass = classes.objects.get(title = request.POST['choice'], user = request.user)
        aclass2 = toggled_classes.objects.get(title=request.POST['choice'], user=request.user)
    except (KeyError, classes.DoesNotExist):
        # Redisplay the class removing form.
        return render(request, 'remove_class.html', {'error_message': "You did not select a class."})
    except toggled_classes.DoesNotExist:
        aclass.delete()
        return HttpResponseRedirect(reverse('classes_view'))
    else:
        aclass.delete()
        aclass2.delete()
        return HttpResponseRedirect(reverse('classes_view'))


def toggle_class(request):
    model = toggled_classes
    return render(request, 'toggle_class.html')


def toggle(request):
    if request.method == 'POST':
        choice = request.POST.getlist('choice')
        if not choice:
            return render(request, 'toggle_class.html', {'error_message': "You did not select a class."})
        else:
            for i in choice:
                if toggled_classes.objects.filter(title=i,user=request.user).exists():
                    return render(request, 'toggle_class.html', {'error_message': "One or more of these classes has already been toggled."})
                else:
                    class_to_toggle = toggled_classes(title=i, user=request.user)
                    class_to_toggle.save()
            return HttpResponseRedirect(reverse('classes_view'))


def untoggle_class(request):
    model = toggled_classes
    return render(request, 'untoggle_class.html')


def untoggle(request):
    if request.method == 'POST':
        choice = request.POST.getlist('choice')
        if not choice:
            return render(request, 'untoggle_class.html', {'error_message': "You did not select a class."})
        else:
            for i in choice:
                    class_to_untoggle = toggled_classes.objects.get(title = i, user = request.user)
                    class_to_untoggle.delete()
            return HttpResponseRedirect(reverse('classes_view'))


def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room_index.html', {'rooms': rooms})


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'room_detail.html', {'room': room})


def token(request):
    identity = request.user.username
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    user_token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        user_token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': user_token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)




class AddLocationView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = "maps.html"
    success_url = "/buddiesforstudies/"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        instance.users.add(self.request.user)
        return HttpResponseRedirect(reverse('index'))
    def get_form_kwargs(self):
        kwargs = super(AddLocationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class UpdateLocationView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "maps.html"
    success_url = "/buddiesforstudies/"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        instance.users.add(self.request.user)
        return HttpResponseRedirect(reverse('index'))
    def get_form_kwargs(self):
        kwargs = super(UpdateLocationView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

def remove_user(request, id):
    location = Location.objects.get(id = id)
    location.users.remove(request.user)
    return HttpResponseRedirect(reverse('index'))

class DeleteLocationView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = "maps_delete.html"
    success_url = "/buddiesforstudies/"





def major_evaluation(request, candidateusers):
    second = majormatch(request, candidateusers)
    if len(second) == 1:  # if the length of this output is only one, return it
        return render(request, 'matching.html', {'data': second[0]})
    elif len(second) < 1:  # if none of the same major
        finalmatch = interestmatch(request, candidateusers)  # evaluate list by major
        return render(request, 'matching.html', {'data': finalmatch}, )  # return the highest similar interest
    else:
        finalmatch = interestmatch(request, second)  # if multiple same major, evaluate that list by intereest
        return render(request, 'matching.html', {'data': finalmatch}, )

def majormatch(request, candiateusers):
    same_major = []
    for candidate in candiateusers:
        if request.user.user_info_set.all()[0].major == candidate.user_info_set.all()[0].major:
            if (request.user != candidate):
                same_major.append(candidate)
    return same_major

def interestmatch(request, candidateusers):
    closest_interest = 1000000000
    match = None
    for candidate in candidateusers:
        similarity = abs(int(request.user.user_info_set.all()[0].level_of_seriousness) - int(candidate.user_info_set.all()[0].level_of_seriousness))
        if similarity < closest_interest:
            closest_interest = similarity
            match = candidate
    if (match == None): user_info.objects.filter(user = request.user).update(match_students = request.user.user_info_set.all()[0].match_students + ", " + " ")
    else: user_info.objects.filter(user = request.user).update(match_students = request.user.user_info_set.all()[0].match_students  + match.username+ ", ")
    return match

def clearmatches(request):
    user_info.objects.filter(user=request.user).update(match_students='')
    return HttpResponseRedirect(reverse('matching'))

def match(request):
    if len(list(request.user.user_info_set.all())) == 0:
        return HttpResponseRedirect(reverse('info'))
    data = list(user_info.objects.all())
    for d in data:
        if d.user == request.user:
            data.remove(d)
        if d.user.username in request.user.user_info_set.all()[0].match_students:
            data.remove(d)
    class_count = {}
    for d in data: # for all the users that have entered info # don't compare against self
        if d.user != request.user:
            for c in d.user.toggled_classes_set.all(): # for every class they've inputted
                for cl in request.user.toggled_classes_set.all(): # if there's a match with the user's class
                    if c.title == cl.title:
                        if c.user not in class_count.keys():# if this user does not have classes yet, initialize count
                            class_count[c.user] = 1
                        else:
                            class_count[c.user] = class_count.get(c.user,0) +1 #otherwise, increase it by 1

    if len(class_count) == 1:
        user_info.objects.filter(user = request.user).update(match_students = request.user.user_info_set.all()[0].match_students  + list(class_count.keys())[0].username +", " )
        return render(request, 'matching.html', {'data': list(class_count.keys())[0]})

    if len(class_count) > 1:# if more than one class
        same_classes = True
        i = 1
        classes = list(class_count.values())# evaluate all the counts
        highest_classes = classes[i-1]
        while i < len(classes):# if at any point not all the classes counts are the same
            if classes[i] != classes[i-1]:
                same_classes =False # we don't have the same number of classes
            if highest_classes < classes[i]: # update global variable
                highest_classes = classes[i]
            i+=1
        if same_classes: # if all the same, evaluate by majors
            return major_evaluation(request, list(class_count.keys()))

        else:# if all different numbers of classes
            most_class = []
            for c in class_count.keys(): # only pay attention to the highest ones
                if class_count[c] == highest_classes:
                    most_class.append(c)
            if len(most_class) == 1:# if only one has the most, return that
                user_info.objects.filter(user = request.user).update(match_students = request.user.user_info_set.all()[0].match_students+ most_class[0].username + ", ")#str(most_class[0].username)
                return render(request, 'matching.html', {'data': most_class[0]})
            else:# otherwise, match based on major
               return major_evaluation(request, most_class)
    else:
        # otherwise, there are no classes, so let's evaluate by major
        noclass_candidates = []
        for d in data:
            if (d.user!= request.user):
                noclass_candidates.append(d.user)

        second = majormatch(request, noclass_candidates)
        return major_evaluation(request, second)


