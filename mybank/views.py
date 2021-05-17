import self as self
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm,LoginForm,AccountCreationForm
from .models import CustomUser,Account
from django.views.generic import TemplateView
from django.contrib.auth import login as djangologin

# Create your views here.

#REGISTRATION
#using user model

class Registration(TemplateView):
    form_class=UserRegistrationForm
    template_name = "registration.html"
    context={}
    def get(self,request,*args,**kwargs):
        self.context["form"]=self.form_class()
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"login.html")
        else:
            self.context["form"]=form
            return render(request,self.template_name,self.context)


#LOGIN
class LoginView(TemplateView):
    model=CustomUser
    template_name = "login.html"
    form_class=LoginForm
    context={}
    def get(self,request,*args,**kwargs):
        self.context["form"]=self.form_class()
        return render(request, self.template_name, self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=self.model.objects.get(username=username)
            if (user.username==username) & (user.password==password):
                djangologin(request,user)
                print("success")
                return redirect("index")
            else:
                print("failed")
                return render(request, self.template_name, self.context)

def index(request):
    context={}
    try:
        account = Account.objects.get(user=request.user)
        status = account.active_status
        print(status)
        flag = True if status == "Active" else False
        print(flag)
        context["flag"] = flag
        return render(request, "home.html",context)
    except:
        return render(request, "home.html", context)

#ACCOUNT CREATION
class AccountCreateView(TemplateView):
    model=Account
    template_name = "createaccount.html"
    form_class=AccountCreationForm
    context={}
    def get(self,request,*args,**kwargs):
        account_number=""
        account=self.model.objects.all().last()
        if account:
            acno=int(account.account_number.split("-")[1])+1
            print("SBK-",acno)
            account_number="SBK-"+str(acno)
            print(account_number)
        else:
            account_number="SBK-1000"
        self.context["form"]=self.form_class(initial={"account_number":account_number,"user":request.user})
        return render(request, self.template_name, self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            self.context["form"]=form
            return render(request, self.template_name, self.context)