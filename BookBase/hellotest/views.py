from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.generic import TemplateView

def helloFunc(request):
    return render(request, 'home.html', {})

def aboutPage(request):
    return render(request, 'about.html', {})
