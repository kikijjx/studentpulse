from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request): #httprequest
    return render(request, 'index.html')

def user(request): #httprequest
    return HttpResponse("userz")
