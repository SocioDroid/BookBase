from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
<<<<<<< HEAD
=======
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.contrib import admin
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static # new
>>>>>>> BUY QWorking
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView, name = 'login'),
    url('signup/', views.register, name ='signup'),
<<<<<<< HEAD
    url('sell/$', views.CreatePostView.as_view(), name='sell')
=======
    url('sell/$', views.sell, name='sell'),
    url('buy/',views.BuyView,name='buybook')
>>>>>>> BUY QWorking
]