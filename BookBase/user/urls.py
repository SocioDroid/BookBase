
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    url('signup/', views.register, name='signup'),
    url('login/', auth_views.LoginView, name = 'login'),

    url('sell/$', views.CreatePostView.as_view(), name='sell'),
    url('buy/',views.BuyView,name='buy'),
    url('dashboard/', views.dashboard, name='dashboard'),
]
