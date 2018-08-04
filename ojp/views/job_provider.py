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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.utils import IntegrityError


def handle_uploaded_file(f,path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class JPLoginController(View):
    def get(self,request):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            form=Login()
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name="jplogin.html",
                context={'form' :form}
            )
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # import ipdb
        # ipdb.set_trace()
        if user is not None and user.is_jp is True:
            login(request, user)
            return redirect("ojp:jphome")
        else:
            messages.error(request,message="Invalid username/password")
            return redirect("ojp:jplogin")


class JPSignupController(View):
    def get(self,request):
        form=SignUp()

        return render(request,
            template_name="jpsignup.html",
            context={'form' :form}
        )
    def post(self, request, *args, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        try:
            i=CUser.objects.create_user(username=request.POST['username'],password=request.POST['password'],first_name=request.POST['first_name'],last_name=request.POST['last_name'],is_jp=True)
        except  IntegrityError:
            messages.error(request, message="Username already exists.Please choose another username")
            return redirect('ojp:jssignup')
        #here we are tempararily login the user for assigning jobproviders company value.if we don't do the anonimus user error will arise
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        #-----------------
        return redirect('ojp:jpdetails')

def JPLogoutControl(request):
    logout(request)
    return redirect("ojp:home")




class JobProvidersHome(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            cd = JPDetails.objects.filter(company=request.user)
            return render(request,
                template_name=r"web/jp/jphome.html",
                          context={'req':request,'cd':cd[0]}
            )

class JobProvidersledit(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            ud=CUser.objects.filter(id=request.user.id)
            cd = JPDetails.objects.filter(company=request.user)
            # form=JobProviderDetails1()
            return render(request,
                template_name=r"web/jp/jpledit.html",
                context={'ud':ud[0],'cd':cd[0]}
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
            return redirect('ojp:jpledit')

        return redirect("ojp:jpprofile", request.user.username)

class JobProviderspedit(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            ud=CUser.objects.filter(id=request.user.id)
            cd = JPDetails.objects.filter(company=request.user)
            form=PasswordChangeForm(request.user)
            return render(request,
                template_name=r"web/jp/jppedit.html",
                context={'ud':ud[0],'cd':cd[0],'form':form}
            )

    def post(self, request, *args, **kwargs):
        form=PasswordChangeForm(request.user,request.POST)
        # ud = CUser.objects.filter(id=request.user.id)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Your password was successfully updated!')

            # ud.set_password(request.POST["new_password1"])
        # import ipdb
        # ipdb.set_trace()
        return redirect("ojp:jpprofile", request.user.username)

class JobProvidersProfile(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self, request,pk):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            cd=JPDetails.objects.all().filter(company=request.user)
            form=JobProviderDetails1()
            return render(request,
                template_name=r"web/jp/jpprofile.html",
                context={'form':form,'cd':cd[0],'req':request,}
            )

    def post(self, request, *args, **kwargs):

        # import ipdb
        # ipdb.set_trace()
        old_logo = JPDetails.objects.filter(company=request.user)[0].logo
        new_logo=request.FILES.get("logo")
        if  new_logo != None:
            new_logo.name = (new_logo.name).lower()
            if (new_logo.name).endswith(".jpg"):
                new_logo.name = request.user.username + ".jpg"
            elif (new_logo.name).endswith(".jpeg"):
                new_logo.name = request.user.username + ".jpeg"
            elif (new_logo.name).endswith(".png"):
                new_logo. name = request.user.username + ".png"
            else:
                return redirect("ojp:jpprofile", request.user.username)
            handle_uploaded_file(new_logo, 'ojp/media/' + new_logo.name)
        else:
            new_logo=old_logo

        # handle_uploaded_file(request.FILES['logo'], 'ojp/media/' + new_logo.name)

#remember the we dont have to add the name of the image to the database every time because the pic name of a user is always username i.e  request.user.username+".jpg"
        JPDetails.objects.filter(company=request.user).update(company_name=request.POST["company_name"],
                                                              logo=request.FILES.get('',new_logo),
                                                              admin_name=request.POST["admin_name"],
                                                              email=request.POST["email"],
                                                              mobile=request.POST["mobile"],
                                                              address=request.POST["address"])



        return redirect("ojp:jpprofile", request.user.username)

    # def post(self, request, *args, **kwargs):
    #     import ipdb
    #     ipdb.set_trace()
    #     JPDetails.objects.filter(company=request.user).update(company_name=request.POST["company_name"],logo=request.POST["logo"],admin_name=request.POST["admin_name"],email=request.POST["email"],mobile=request.POST["mobile"],address=request.POST["address"])
    #     return redirect('ojp:jpprofile ',request.user.username )
    # model = JPDetails
    # form_class = JobProviderDetails1
    # template_name = r"web/jp/jpprofile.html"
    # success_url = reverse_lazy("ojp:jpprofile")
    # def get_object(self, queryset=None):
    #     return JPDetails.objects.get(pk=self.request.GET.get('pk'))  # or request.POST


class JobProvidersPostJobs(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):

        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')

        else:
            cd = JPDetails.objects.filter(company=request.user)
            form=PostJobs
            pj=JPPostJobs.objects.filter(company=request.user)
            return render(request,
                template_name=r"web/jp/jppj.html",
                context={'form':form,'postedjobs':pj,'req':request,'cd':cd[0]}
            )
    def post(self, request, *args, **kwargs):
        pj=JPPostJobs()
        # import ipdb
        # ipdb.set_trace()
        pj.company=request.user
        x=JPDetails.objects.filter(company=request.user)
        pj.cdetails=x[0]
        pj.job_title=request.POST["job_title"]
        pj.salary=request.POST["salary"]
        pj.work_hours=request.POST["work_hours"]
        pj.required_experiance=request.POST["required_experiance"]
        pj.qualifications=request.POST["qualifications"]
        pj.note=request.POST["note"]
        pj.save()
        return redirect('ojp:jppj')

class JobProvidersPostJobsEdit(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            cd = JPDetails.objects.filter(company=request.user)
            form=PostJobs
            jd=JPPostJobs.objects.filter(id=pk)
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/jp/jppjedit.html",
                context={'form':form,'jd':jd[0],'req':request,'cd':cd[0]}
            )

    def post(self, request, *args, **kwargs):
        JPPostJobs.objects.filter(id=kwargs['pk']).update(job_title=request.POST["job_title"],salary=request.POST["salary"],work_hours=request.POST["work_hours"],required_experiance=request.POST["required_experiance"],qualifications=request.POST["qualifications"],note=request.POST["note"])
        return redirect('ojp:jppj')

def JobDelete(request,pk):
    JPPostJobs.objects.filter(id=pk).delete()
    return redirect("ojp:jppj")

class JSAccept(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
          cd = JPDetails.objects.filter(company=request.user)
          jsa=JSAppliedJobs.objects.filter(id=pk)
          if not jsa[0].is_selected:
              return render(
                  request,
                  template_name=r"web/jp/jsan.html",
                  context={'req': request,'cd':cd[0]}
              )
          else:
              return render(request,r"web/jp/jpaa.html")

    def post(self,request, *args, **kwargs):
      JSAppliedJobs.objects.filter(id=kwargs['pk']).update(is_selected=True, is_rejected=False,notes=request.POST["notes"])
      return redirect("ojp:jpvac")


class JSReject(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
              jsa=JSAppliedJobs.objects.filter(id=pk)
              cd = JPDetails.objects.filter(company=request.user)
              if not jsa[0].is_rejected:
                  return render(
                      request,
                      template_name=r"web/jp/jsrn.html",
                      context={'req': request,'cd':cd[0]}
                  )
              else:
                  return render(request,r"web/jp/jpar.html")

    def post(self,request, *args, **kwargs):
      JSAppliedJobs.objects.filter(id=kwargs['pk']).update(is_selected=False, is_rejected=True,reason=request.POST["reason"])
      return redirect("ojp:jpvac")


class JobProviderViewAppliedCandidates(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            cd = JPDetails.objects.filter(company=request.user)
            ac=JSAppliedJobs.objects.filter(job__company=request.user)
            # import ipdb
            # ipdb.set_trace()
            return render(request,
                template_name=r"web/jp/jpvac.html",
                context={'ac':ac,'req':request,'cd':cd[0]}

            )
class JobProviderViewAppliedCandidate(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request,pk):
        if (request.user.is_authenticated) and (not request.user.is_jp):
            return redirect('ojp:jshome')
        else:
            cd = JPDetails.objects.filter(company=request.user)
            jad=JSAppliedJobs.objects.filter(id=pk)#to get the row corresponding to the job id and job seeker
            jsd=JobSeekerDetails.objects.filter(jobseeker_id=jad[0].js_id)


            return render(request,
                template_name=r"web/jp/jsvd.html",
                          context={'jsd':jsd[0],'req':request,'pk':pk,'cd':cd[0]}
            )

class JobProviderDetails(LoginRequiredMixin,View):
    login_url = '/jplogin/'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        form = JobProviderDetails1
        return render(request,
            template_name=r"web/jp/jpdetails.html",
            context={'form': form,}
        )

    def post(self, request, *args, **kwargs):

        jpd=JPDetails()
        jpd.company=request.user
        jpd.company_name=request.POST["company_name"]
        # import ipdb
        # ipdb.set_trace()
        jpd.logo=request.FILES["logo"]
        jpd.admin_name=request.POST["admin_name"]
        jpd.email=request.POST["email"]
        jpd.mobile=request.POST["mobile"]
        jpd.address=request.POST["address"]
        jpd.save()
        logout(request)#here we are logouting the user which is logged in the signup
        return redirect('ojp:jplogin')