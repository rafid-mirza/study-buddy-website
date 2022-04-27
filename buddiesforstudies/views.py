from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from .models import classes, jsonData, toggled_classes, participant, conversation
from django.views.generic import CreateView
from .models import classes, jsonData, toggled_classes, Location
import os
from twilio.rest import Client

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
        if aclass.title in jsonData.objects.get(label="classes").classes_list:
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
        return render(request, 'remove_class.html', {'error_message': "You did not select a class."})
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
            return render(request, 'toggle_class.html', {'error_message': "You did not select a class."})
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
            return render(request, 'untoggle_class.html', {'error_message': "You did not select a class."})
        else:
            for i in choice:
                    class_to_untoggle = toggled_classes.objects.get(title = i, user = request.user)
                    class_to_untoggle.delete()
            return HttpResponseRedirect(reverse('index'))


def messages_home(request):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # Checks if user already exists in models, and if it does it gets the user id
    user_id = None
    for member in participant.objects.all():
        if member.identity == request.user.username:
            user_id = member.user_id
    if user_id is None:
        user = client.conversations.users.create(identity=request.user.username)
        temp_participant = participant(user_id=user.sid, identity=request.user.username)

    # Checks for chats the user is in
    chats = []
    for chat in conversation.objects.all():
        for member in chat.participants.all():
            if member.identity is request.user.username:
                chats.append(chat)
    chat_messages = []
    chat_participants = []
    if chats:
        participants = client.conversations.conversations(chats[0].chat_id).participants.list()
        for chatMember in participants:
            chat_participants.append(chatMember['identity'])
        messages = client.conversations.conversations(chats[0].chat_id).messages.list()
        for message in messages['messages']:
            chat_messages.append([message['body'], message['author'], message['date_updated']])
        return render(request, 'messages.html', {'conversations': chats, 'messages': chat_messages,
                                                 "participants": chat_participants, 'current_chat': chats[0].chat_id})


def create_chat_one(request):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    friendly_name = request.POST['name']
    chat = client.conversations.conversations.create(friendly_name=friendly_name)
    chat_object = conversation(friendly_name=friendly_name, chat_id=chat.sid)
    member = client.conversations.conversations(chat_object.chat_id).participants.create(
        identity=request.user.username)
    chat_object.save()
    chat_object.participants.add(participant.objects.get(identity=request.user.username))
    return messages_home(request)


def send_message(request):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.conversations.conversations(request.POST["conversation_id"]).messages.create(
        author=request.user.username, body=request.POST["message"])
    return refresh_feed(request)


def refresh_feed(request):
    # Checks for chats the user is in but this version keeps the spot in the messages list
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    chats = []
    for chat in conversation.objects.all():
        for member in chat.participants.all():
            if member.identity is request.user.username:
                chats.append(chat)
    chat_messages = []
    chat_participants = []
    if chats:
        participants = client.conversations.conversations(request.POST["conversation_id"]).participants.list()
        for member in participants:
            chat_participants.append(member['identity'])
        messages = client.conversations.conversations(request.POST["conversation_id"]).messages.list()
        for message in messages['messages']:
            chat_messages.append([message['body'], message['author'], message['date_updated']])
    return render(request, 'messages.html', {'conversations': chats, 'messages': chat_messages,
                                             "participants": chat_participants,
                                             "current_chat": request.POST["conversation_id"]})


def add_participant(request):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    try:
        existing_user = participant.objects.get(identity=request.POST["name"])
        new_member = client.conversations.conversations(request.POST["conversation_id"]).participants.create(
            identity=request.POST["name"])
        chat_object = conversation.objects.get(chat_id=request.POST["conversation_id"])
        chat_object.participants.add(existing_user)
    except(KeyError, participant.DoesNotExist):
        return render(request, 'messages.html',
                      {"error_message": "User does not exist or has not ever clicked on messages"})
    return refresh_feed(request)





class AddLocationView(CreateView):
    model = Location
    template_name = "maps.html"
    success_url = "/buddiesforstudies/maps"
    fields = ("location", "address")

