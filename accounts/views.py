from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm, AccountForm, AddressForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from transactions.models import Transaction

from datetime import datetime

from .models import Account, Address

class AccountView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "accounts/account_home.html"
    context_object_name = "transactions"
    login_url = "/account/login"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        ).order_by("-created_at")

        query = {}

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            query.update(
                created_at__date__gte = start_date,
                created_at__date__lte = end_date
            )

        try:
            list_length = int(self.request.GET.get('list_length', 25))
        except ValueError:
            list_length = 25
        else:
            if not list_length <= 100:
                list_length = 25

        txn_type = self.request.GET.get("txn_type")

        
        if txn_type:
            if txn_type == "loan-pending":
                query.update(
                    txn_type = 3,
                    approval = False
                )
                queryset = queryset.filter(**query)
        elif list_length:
            query.update(
                approval = True
            )
            queryset = queryset.filter(**query)[:list_length]

        return queryset

def create_account(request):
    user_form = UserForm()
    account_form = AccountForm()
    address_form = AddressForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)
        address_form = AddressForm(request.POST)
        if all([user_form.is_valid(), account_form.is_valid(), address_form.is_valid()]):
            user = user_form.save(commit=True)

            account_form.instance.user = user
            account_form.instance.account_no = int(user.id) + 1000
            address_form.instance.user = user

            account_form.save()
            address_form.save()

            username = request.POST["username"]
            password = request.POST["password1"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

            messages.success(request, "Account Created Successfully")

            return redirect("account")

    return render(request, "accounts/form_create_account.html", {
        "UserForm": user_form,
        "AccountForm": account_form,
        "AddressForm": address_form
    })


def edit_account(request, id):

    # user_form = UserForm(instance=User.objects.get(pk=id))
    Account_form = AccountForm(instance=Account.objects.get(pk=id))
    # address_form = AddressForm(instance=Address.objects.get(pk=id))
    
    return render(request, "accounts/form_create_account.html", {
        # "UserForm": user_form,
        "AccountForm": Account_form,
        # "AddressForm": address_form
    })




def login_account(request):
    user_form = AuthenticationForm(request)
    
    if request.method == "POST":
        user_form = AuthenticationForm(request, request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data["username"]
            password = user_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("accounts:home")
            


    return render(request, "accounts/form_login.html", {
        "LoginForm": user_form
    })

def logout_account(reqeust):
    logout(request=reqeust)
    return redirect("accounts:login")

