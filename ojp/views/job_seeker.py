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
import sys
from django.db.utils import IntegrityError
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import FormMessagesMixin



def handle_uploaded_file(f,path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class JSLoginController(View):
    def get(self,request):
        # import ipdb
        # ipdb.set_trace()
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            form=Login()
            return render(request,
                template_name="jslogin.html",
                context={'form' :form}
            )
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        # import ipdb
        # ipdb.set_trace()
        if user is not None and user.is_jp is False:
            login(request, user)
            # messages.add_message(self.request,messages.SUCCESS,'Login Successful')
            return redirect("ojp:jshome")
        else:
            messages.error(self.request,"Invalid username / password")
            return redirect("ojp:jslogin")

class JSSignupController(View):
    def get(self,request):
        form=SignUp()
        return render(request,
            template_name="jssignup.html",
            context={'form' :form}
        )
    def post(self, request, *args, **kwargs):
            # import ipdb
            # ipdb.set_trace()
            try:
                i = CUser.objects.create_user(username=request.POST['username'], password=request.POST['password'],first_name=request.POST['first_name'], last_name=request.POST['last_name'],is_jp=False)
            except  IntegrityError:
                messages.error(request,message="Username already exists.Please choose another username")
                return redirect('ojp:jssignup')

            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('ojp:jsdetails')



def JSLogoutControl(request):
    logout(request)
    return redirect("ojp:home")



class JobSeekersHome(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            return render(request,
                template_name=r"web/js/jshome.html",
                context={'req':request,'jsd':jsd[0]}
            )


class JobSeekersHelpDesk(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            return render(request,
                template_name=r"web/js/jshd.html",
                context={'req':request,'jsd':jsd[0]}
            )

class JobSeekersResume(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            return render(request,
                template_name=r"web/js/jsresume.html",
                context={'req':request,'jsd':jsd[0]}
            )


class JobSeekersProfile(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            form=JobSeekerDetails1
            jsd=JobSeekerDetails.objects.filter(jobseeker=request.user)
            return render(request,
                template_name=r"web/js/jsprofile.html",
                context={'form':form,'jsd':jsd[0],'req':request}
            )

    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        old_dp = JobSeekerDetails.objects.filter(jobseeker=request.user)[0].dp
        new_dp = request.FILES.get("dp")
        old_res=JobSeekerDetails.objects.filter(jobseeker=request.user)[0].resume
        new_res=request.FILES.get("resume")
        if new_dp != None:
            new_dp.name = (new_dp.name).lower()
            if (new_dp.name).endswith(".jpg"):
                new_dp.name = request.user.username + ".jpg"
            elif (new_dp.name).endswith(".jpeg"):
                new_dp.name = request.user.username + ".jpeg"
            elif (new_dp.name).endswith(".png"):
                new_dp.name = request.user.username + ".png"
            else:
                return redirect("ojp:jsprofile")
            handle_uploaded_file(new_dp, 'ojp/media/' + new_dp.name)
        else:
            new_dp=old_dp



        if new_res != None:
            if (new_res.name).endswith(".pdf"):
                new_res.name=request.user.username+ ".pdf"
            else:
                return redirect("ojp:jsprofile")
            handle_uploaded_file(new_res, 'ojp/media/' + new_res.name)
        else:
            new_res = old_res

        # import ipdb
        # ipdb.set_trace()



        JobSeekerDetails.objects.filter(jobseeker=request.user).update(
            dp=request.FILES.get('', new_dp),
            resume=request.FILES.get('', new_res),

            email = request.POST["email"],
            mobile = request.POST["mobile"],

            t_school = request.POST["t_school"],
            t_pyear = request.POST["t_pyear"],
            t_gpa = request.POST["t_gpa"],

            ird_type = request.POST["ird_type"],
            ird_clz_name = request.POST["ird_clz_name"],
            ird_pyear = request.POST["ird_pyear"],
            ird_percentage = request.POST["ird_percentage"],

            h1_type = request.POST["h1_type"],
            h1_clz_name = request.POST["h1_clz_name"],
            h1_specilization = request.POST["h1_specilization"],
            h1_pyear = request.POST["h1_pyear"],
            h1_percentage = request.POST["h1_percentage"],

            h2_type = request.POST["h2_type"],
            h2_clz_name = request.POST["h2_clz_name"],
            h2_specilization = request.POST["h2_specilization"],
            h2_pyear = request.POST["h2_pyear"],
            h2_percentage = request.POST["h2_percentage"]

        )
        # import ipdb
        # ipdb.set_trace()
        return redirect("ojp:jsprofile")

class JobSeekersViewJobs(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            vj=JPPostJobs.objects.all()
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/js/jsvj.html",
                context={'jobs':vj,'req':request,'jsd':jsd[0]}
            )

def AppliedJobDelete(request,pk):
    # import ipdb
    # ipdb.set_trace()
    JSAppliedJobs.objects.filter(job_id=pk,js_id=request.user.id).delete()
    return redirect("ojp:jsvaj")

def JobSeekerApplyJob(request,pk):
    jsa = JSAppliedJobs.objects.filter(job_id=pk,js_id=request.user.id)
    # import ipdb
    # ipdb.set_trace()
    if not jsa:
        jsa=JSAppliedJobs()
        jsa.job=JPPostJobs.objects.filter(id=pk)[0]
        jsa.js=request.user
        jsa.save()
        return redirect("ojp:jsvj")
    else:
        return render(request, r"web/js/notification_page.html",context={"req":request})
class JobSeekerViewJob(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            aj=JPPostJobs.objects.filter(id=pk)
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/js/jsaj.html",
                context={'aj':aj[0],'req':request,'jsd':jsd[0]}
            )

class JobSeekersAppliedJobs(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            vaj=JSAppliedJobs.objects.filter(js_id=request.user.id)

            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/js/jsvaj.html",
                context={'jobs':vaj,'req':request,'jsd':jsd[0]}
            )

class AppliedJobStatus(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')

        else:
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            aj=JSAppliedJobs.objects.filter(job_id=pk,js_id=request.user.id)
            if aj:

                if aj[0].is_selected:
                    return render(request, r"web/js/jsastatus.html",context={"req":request,"aj":aj[0],'jsd':jsd[0]})
                elif aj[0].is_rejected:
                    return render(request, r"web/js/jsrstatus.html",context={"req":request,"aj":aj[0],'jsd':jsd[0]})
            return render(request, r"web/js/jsnostatus.html", context={"req": request,'jsd':jsd[0]})


class JobSeekersDetailss(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        form = JobSeekerDetails1
        return render(request,
            template_name=r"web/js/jsdetails.html",
            context={'form': form,}
        )
    def post(self, request, *args, **kwargs):
        jsd=JobSeekerDetails()
        # import ipdb
        # ipdb.set_trace()
        jsd.dp=request.FILES.get('dp',None)
        jsd.resume=request.FILES.get('resume',None)
        jsd.email=request.POST["email"]
        jsd.mobile=request.POST["mobile"]

        jsd.t_school=request.POST["t_school"]
        jsd.t_pyear=request.POST["t_pyear"]
        jsd.t_gpa=request.POST["t_gpa"]

        jsd.ird_type=request.POST["ird_type"]
        jsd.ird_clz_name=request.POST["ird_clz_name"]
        jsd.ird_pyear=request.POST["ird_pyear"]
        jsd.ird_percentage=request.POST["ird_percentage"]

        jsd.h1_type=request.POST["h1_type"]
        jsd.h1_clz_name=request.POST["h1_clz_name"]
        jsd.h1_specilization=request.POST["h1_specilization"]
        jsd.h1_pyear=request.POST["h1_pyear"]
        jsd.h1_percentage=request.POST["h1_percentage"]

        jsd.h2_type=request.POST["h2_type"]
        jsd.h2_clz_name=request.POST["h2_clz_name"]
        jsd.h2_specilization=request.POST["h2_specilization"]
        jsd.h2_pyear=request.POST["h2_pyear"]
        jsd.h2_percentage=request.POST["h2_percentage"]

        jsd.jobseeker=request.user
        logout(request)
        jsd.save()
        return redirect('ojp:jslogin')




class JobSeekerledit(LoginRequiredMixin,View):
    login_url = '/jslogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        if (request.user.is_authenticated) and (request.user.is_jp):
            return redirect('ojp:jphome')
        else:
            ud=CUser.objects.filter(id=request.user.id)
            jsd = JobSeekerDetails.objects.filter(jobseeker=request.user)
            # form=JobProviderDetails1()
            return render(request,
                template_name=r"web/js/jsledit.html",
                context={'ud':ud[0],'jsd':jsd[0]}
            )

    def post(self, request, *args, **kwargs):
        ud=CUser.objects.get(username=request.user.username)
        ud.first_name=request.POST["first_name"]
        ud.last_name=request.POST["last_name"]
        ud.username=request.POST["username"]
        if request.POST["password"] != '':
            ud.set_password(request.POST["password"])
        try:
            ud.save()
        except IntegrityError:
            messages.error(request, message="Username already exists.Please choose another username")
            return redirect('ojp:jsledit')

        return redirect("ojp:jsprofile")

