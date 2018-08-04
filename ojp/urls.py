from ojp.models import *
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from ojp.views.user import *
from ojp.views.job_seeker import *
from ojp.views.job_provider import *
# from ojp.views.data_json import *
from django.conf.urls.static import static
# from django.conf.urls import handler404


app_name='ojp'

urlpatterns = [
    path('',HomePage.as_view(),name='home'),
    path('jpsignup/',JPSignupController.as_view(),name='jpsignup'),
    path('jplogin/',JPLoginController.as_view(),name='jplogin'),
    path('jssignup/',JSSignupController.as_view(),name='jssignup'),
    path('jslogin/',JSLoginController.as_view(),name='jslogin'),
    path('jplogout/',JPLogoutControl,name='jplogout'),
    path('jslogout/',JSLogoutControl,name='jslogout'),

    path('jobseekerhome/',JobSeekersHome.as_view(),name='jshome'),
    path('jobseekerprofile/',JobSeekersProfile.as_view(),name='jsprofile'),
    path('jobseekerviewjobs/',JobSeekersViewJobs.as_view(),name='jsvj'),
    path('jobseekerdetails/',JobSeekersDetailss.as_view(),name='jsdetails'),
    path('jobseekerapply/<int:pk>/',JobSeekerApplyJob,name='jsapply'),
    path('jobseekerviewjob/<int:pk>/',JobSeekerViewJob.as_view(),name='jsaj'),
    path('jobseekerviewappliedjobs/', JobSeekersAppliedJobs.as_view(), name='jsvaj'),
    path('appliedjobdelete/<int:pk>/',AppliedJobDelete,name='ajd'),
    path('appliedjobstatus/<int:pk>/',AppliedJobStatus.as_view(),name='ajs'),
    path('jobseekerhelpdesk/',JobSeekersHelpDesk.as_view(),name='jshd'),
    path('jobseekerresume/', JobSeekersResume.as_view(), name='jsres'),
    path('jobseekerprofileedit/', JobSeekerledit.as_view(), name='jsledit'),



    path('jobproviderhome/', JobProvidersHome.as_view(), name='jphome'),
    path('jobproviderprofile/<slug:pk>/', JobProvidersProfile.as_view(), name='jpprofile'),
    path('jobproviderprofileedit/', JobProvidersledit.as_view(), name='jpledit'),
    path('jobproviderpostjobs/', JobProvidersPostJobs.as_view(), name='jppj'),
    path('jobproviderdetails/', JobProviderDetails.as_view(), name='jpdetails'),
    path('jobproviderpostjobs/<int:pk>/',JobProvidersPostJobsEdit.as_view(),name='jppjedit'),
    path('jobproviderdelete/<int:pk>/',JobDelete,name='jpdelete'),
    path('jobproviderviewappliedcandidates/', JobProviderViewAppliedCandidates.as_view(), name='jpvac'),
    path('jobproviderviewappliedcandidate/<int:pk>/', JobProviderViewAppliedCandidate.as_view(), name='jpvd'),
    path('jobseekeraccept/<int:pk>/',JSAccept.as_view(),name='jsa'),
    path('jobseekerreject/<int:pk>/', JSReject.as_view(), name='jsr')
    # path('delete/<int:pk>',JobDelete(pk=pk))
    # path('logout/',LogoutControl,name='logout'),
    # path('addcollege/',AddCollege.as_view(),name='addcollege'),
    # path('viewcolleges/',ViewColleges.as_view(),name='viewcolleges'),
    # path('<int:pk>/addstudent/',AddStudent.as_view(),name='addstudent'),
    # path('<int:pk>/viewstudents/',ViewStudents.as_view(),name='viewstudents'),
    # path('<int:pk>/updatecollege/',UpdateCollege.as_view(),name='updatecollege'),
    # path('<int:pk>/updatestudent/',UpdateStudent.as_view(),name="updatestudent"),
    # path('<int:pk>/deletecollege/',DeleteCollege.as_view(),name='deletecollege'),
    # path('<int:pk>/deletestudent/',DeleteStudent.as_view(),name="deletestudent"),
    # # path('api/colleges/<int:pk>/',college_list,name='json_colleges'),
    # path('api/colleges/',college_list,name='json_colleges1'),
    # path('api/colleges/<int:pk>/',student_details,name='json_student'),
    # path('',TemplateView.as_view(template_name="index.html"),name="rjs")
    # path('api/colleges/<int:pk>/',college_list2,name='json_colleges')
    ]