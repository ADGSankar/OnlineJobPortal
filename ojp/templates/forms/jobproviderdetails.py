from django import forms
from ojp.models import *

class JobProviderDetails1(forms.Form):
    company_name=forms.CharField(max_length=50,required=True)
    logo=forms.ImageField(max_length=10)
    admin_name=forms.CharField(max_length=30,required=True)
    email=forms.EmailField(required=True)
    mobile=forms.CharField(max_length=10)
    address=forms.CharField(widget=forms.Textarea)

class PostJobs(forms.Form):
    job_title=forms.CharField(max_length=50,required=True)
    salary=forms.FloatField(required=True)
    work_hours=forms.IntegerField(required=True)
    required_experiance=forms.IntegerField(help_text="In Years")
    qualifications=forms.CharField(widget=forms.Textarea,required=True)
    note=forms.CharField(widget=forms.Textarea,help_text="Other Requirments")

# class JPAccept(forms.Form):
#     notes=forms.CharField(widget=forms.Textarea,help_text="notes",required=True)
#
# class JPReject(forms.Form):
#     reason=forms.CharField(widget=forms.Textarea,help_text="Reason",required=True)