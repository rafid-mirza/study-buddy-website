from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("It's like tinder, but for finding people to study with")
