from django.shortcuts import render
from django.contrib.auth.models import User
from  .forms import UserRegistrationForm
from .models import CustomUser
from django.views.generic import TemplateView

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


#LOGIN