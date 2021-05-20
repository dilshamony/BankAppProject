from .models import  Account
from django.contrib import messages
from django.shortcuts import redirect


def account_created_validator(func):
    def wrapper (request,*args,**kwargs):
        try:
            account=Account.objects.get(user=request.user)
            status=account.active_status
            if status=="Active":
                messages.error(request,"Account created for this user")
                return  redirect("index")
            else:
                return func(request,*args,**kwargs)
        except:
            func(request, *args, **kwargs)
    return wrapper