from django import forms
from .models import UserProfileInfo,Sell
from django.contrib.auth.models import User
class UserForm( forms.ModelForm ):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password', 'email')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('college','department', 'year','phoneNo')

class SellForm(forms.ModelForm):

    class Meta:
        model = Sell
        fields = ['title', 'author', 'description','price','bookImage']