from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView, name = 'login'),
    url('signup/', views.register, name ='signup'),
    url('sell/$', views.CreatePostView.as_view(), name='sell')
]