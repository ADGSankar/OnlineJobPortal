from django import forms
from ojp.models import *

i_or_d_clz_list = [('none','None'),('inter', 'Inter'), ('diploma', 'Diploma')]
he_type_list=[('none','None'),('degree','Degree'),('btech','Btech'),('others','Others')]
hei_type_list=[('none','None'),('mtech','Mtech'),('mba','MBA'),('mca','MCA'),('others','Others')]
class JobSeekerDetails1(forms.Form):
    dp=forms.ImageField(required=True)
    resume=forms.FileField(required=False)

    email=forms.EmailField(max_length=40,required=True)
    mobile=forms.CharField(max_length=10,required=True)

    t_school=forms.CharField(max_length=20,required=True)
    t_pyear=forms.IntegerField(required=True)
    t_gpa=forms.FloatField(required=True)

    ird_type=forms.CharField(widget=forms.Select(choices=i_or_d_clz_list))
    ird_clz_name=forms.CharField(max_length=100,required=True)
    ird_pyear=forms.IntegerField(required=True)
    ird_percentage=forms.FloatField(required=True)

    h1_type=forms.CharField(widget=forms.Select(choices=he_type_list))
    h1_clz_name = forms.CharField(max_length=50, required=True)
    h1_specilization=forms.CharField(max_length=50, required=True)
    h1_pyear = forms.IntegerField(required=True)
    h1_percentage = forms.FloatField(required=True)

    h2_type=forms.CharField(widget=forms.Select(choices=hei_type_list))
    h2_clz_name = forms.CharField(max_length=50, required=True)
    h2_specilization=forms.CharField(max_length=50, required=True)
    h2_pyear = forms.IntegerField(required=True)
    h2_percentage = forms.FloatField(required=True)




