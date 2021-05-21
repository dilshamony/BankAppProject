import self as self
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm,LoginForm,AccountCreationForm,TransactionCreateForm
from .models import CustomUser,Account,FundTransactions
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



class GetUserMixin(object):
    def get_user(self,account_num):
        return  Account.objects.get(account_number=account_num)

class TransactionView(TemplateView,GetUserMixin):
    model = FundTransactions
    template_name = "transactions.html"
    form_class = TransactionCreateForm
    context={}
    def get(self,request,*args,**kwargs):
        self.context["form"]=self.form_class(initial={"user":request.user})
        return render(request,self.template_name, self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            to_account=form.cleaned_data.get("to_account_number")
            amount=form.cleaned_data.get("amount")
            remarks=form.cleaned_data.get("remarks")
            account=self.get_user(to_account)
            account.balance+=int(amount)
            account.save()
            current_account=Account.objects.get(user=request.user)
            current_account.balance-=int(amount)
            current_account.save()
            transaction=FundTransactions(user=request.user,amount=amount,to_accno=to_account,remarks=remarks)
            transaction.save()
            return redirect("index")
        else:
            self.context["form"]=form
            return render(request,self.template_name)


#BALANCE ENQUIRY
class BalanceEnq(TemplateView):
    def get(self,request,*args,**kwargs):
        account=Account.objects.get(user=request.user)
        balance=account.balance
        return render(request,"balancechk.html",{"balance":balance})


#TRANSACTION HISTORY
class TransactionHistory(TemplateView):
    def get(self, request,*args,**kwargs):
        debit_transactions=FundTransactions.objects.filter(user=request.user)
        #fetch logined user account
        l_user=Account.objects.get(user=request.user)
        credit_transactions=FundTransactions.objects.filter(to_accno=l_user.account_number)
        return render(request,"Transactionhistory.html",{"dtransactions":debit_transactions,"ctransactions":credit_transactions})