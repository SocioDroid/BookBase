
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include # new

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView, name = 'login'),
    url('signup/', views.register, name ='signup'),
    url('sell/$', views.CreatePostView.as_view(), name='sell'),
    url('buy/',views.BuyView,name='buy')
]