from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView,TemplateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate,logout,login
from ojp.models import *
from ojp.templates.forms.login import *
from ojp.templates.forms.jobseekerdetails import *
from ojp.templates.forms.jobproviderdetails import *
# from ojp.templates.html import *
from django.contrib.auth.models import UserManager


class HomePage(View):
    def get(self,request):
        return render(request,
            template_name=r"home.html",
        )


