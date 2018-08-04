from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CUser(AbstractUser):
     is_jp = models.BooleanField(default=False)

class JobSeekerDetails(models.Model):
    dp = models.FileField(default=None)
    resume = models.FileField(default=None,)
    email=models.EmailField()
    mobile=models.CharField(max_length=10)

    t_school=models.CharField(max_length=20)
    t_pyear=models.IntegerField()
    t_gpa=models.FloatField()

    ird_type=models.CharField(max_length=10)
    ird_clz_name=models.CharField(max_length=50)
    ird_pyear=models.IntegerField()
    ird_percentage=models.FloatField()

    h1_type=models.CharField(max_length=10)
    h1_clz_name=models.CharField(max_length=50)
    h1_specilization=models.CharField(max_length=50)
    h1_pyear=models.IntegerField()
    h1_percentage=models.FloatField()

    h2_type = models.CharField(max_length=10)
    h2_clz_name = models.CharField(max_length=50)
    h2_specilization = models.CharField(max_length=50)
    h2_pyear = models.IntegerField()
    h2_percentage = models.FloatField()
    jobseeker=models.OneToOneField(CUser,on_delete=models.CASCADE)


class JPDetails(models.Model):
    company=models.ForeignKey(CUser,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=50)
    logo=models.FileField()
    admin_name=models.CharField(max_length=30)
    email=models.EmailField()
    mobile=models.CharField(max_length=10)
    address=models.TextField(max_length=100)

class JPPostJobs(models.Model):
    company=models.ForeignKey(CUser,on_delete=models.CASCADE)
    cdetails=models.ForeignKey(JPDetails,on_delete=models.CASCADE)
    job_title=models.CharField(max_length=50)
    salary=models.FloatField()
    work_hours=models.IntegerField()
    required_experiance=models.IntegerField()
    qualifications=models.TextField(max_length=100)
    note=models.TextField(max_length=100)



class JSAppliedJobs(models.Model):
    job = models.ForeignKey(JPPostJobs, on_delete=models.CASCADE)
    js = models.ForeignKey(CUser, on_delete=models.CASCADE)
    is_selected=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    reason=models.TextField(max_length=100,default="")
    notes=models.TextField(max_length=100,default="")