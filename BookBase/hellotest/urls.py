from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', helloFunc, name="home"),
    path('about/', aboutPage, name="about"),
]
