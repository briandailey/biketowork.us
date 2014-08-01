from django.shortcuts import render, render_to_response, HttpResponse
from .models import Ride

def recent(request):
    return HttpResponse('leeeroy jenkins!')
