from django import forms
from ojp.models import *
from django.contrib.auth.forms import UserChangeForm

class SignUp(forms.Form):
    first_name=forms.CharField(max_length=30,required=True)
    last_name=forms.CharField(max_length=30,required=True)
    username=forms.CharField(max_length=30,required=True)
    password=forms.CharField(max_length=30,required=True,widget=forms.PasswordInput)

class Login(forms.Form):
    username=forms.CharField(max_length=30,required=True)
    password=forms.CharField(max_length=30,required=True,widget=forms.PasswordInput)


class EditProfile(UserChangeForm):
    class Meta:
        model=CUser
        fields={
            'username','password','first_name','last_name'
        }