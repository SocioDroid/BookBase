from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView, name = 'login'),
    url('signup/', views.register, name ='signup'),
    url('sell/', views.sell, name='sell')
]
