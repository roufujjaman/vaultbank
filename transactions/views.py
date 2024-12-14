from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import TransactionForm
from django.views.generic import CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, TRANSACTION_TYPE
from . import forms
from django.views.generic import ListView


from django.contrib import messages

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives

class TransactionView(LoginRequiredMixin, CreateView):
    login_url = "/account/login"
    model = Transaction
    template_name = 'transactions/transaction_form.html'
    success_url = '/account'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs.update(
                {"account": self.request.user.account}
            )
        return kwargs

class DepositView(TransactionView):
    form_class = forms.DepositForm
    title =  "Deposit"
    initial = {"txn_type": 1, "approval": True}
    
    
    extra_context = {
        "subtitle": "Deposit",
    }

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        account = self.request.user.account
        account.balance += amount

        account.save(
            update_fields = ["balance"]
        )

        messages.success(self.request, "Deposit Successfull")

        # email
        # subject_email = "Depost Success"
        # from_email = "vaultbank@gmail.com"
        # to_mail = "roufujjaman.rahat@northsouth.edu"
        
        # message = render_to_string(
        #     'transactions/email_deposit.html',
        #     {
        #         'user': self.request.user,
        #         'amount': amount,
        #         'balance': self.request.user.account.balance
        #     }
        # )

        # send_mail = EmailMultiAlternatives(subject_email, message, to=[to_mail])
        # send_mail.attach_alternative(message, "text/html")
        # send_mail.send()

        return super().form_valid(form)

class WithdrawView(TransactionView):
    form_class = forms.WithdrawForm
    initial = {"txn_type": 2, "approval": True}
    extra_context = {
        "subtitle": "Withdraw"
    }

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        account = self.request.user.account
        account.balance -= amount

        account.save(
            update_fields=["balance"]
        )

        messages.success(self.request, "Withdrawal Successfull")

        return super().form_valid(form)


class LoanRequestView(TransactionView):
    form_class = forms.LoanForm
    initial = {"txn_type": 3}
    extra_context = {
        "subtitle": "Loan Request"
    }

    def form_valid(self, form):

        messages.success(self.request, "Loan Request Successfull")
        return super().form_valid(form)


# class LoansView(LoginRequiredMixin, ListView):
#     model = Transaction
#     template_name = "transactions\payment_form.html"
#     extra_context = {
#         "subtitle": "Loan Payback"
#     }
    
#     context_object_name = "loanlist"


#     def get_queryset(self):
#         queryset = super().get_queryset().filter(
#             account= self.request.user.account,
#             txn_type=3
#         ).order_by("-created_at")
#         return queryset
    
#     def post(self, request, *args, **kwargs):
#         transaction_id = request.POST.get("id")


#         transaction = Transaction.objects.get(id=transaction_id)
#         account = request.user.account
        
#         if transaction.account == account:
#             account.balance -= transaction.amount
#             account.save(update_fields=["balance"])
            
#             new_transaction = Transaction.objects.create(
#                 account = transaction.account,
#                 amount = transaction.amount,
#                 balance_post_txn = account.balance,
#                 txn_type = 4
#             )
            
#             new_transaction.save()
#             transaction.delete()

#         return redirect("transactions:loan-list")
    
class TransferView(TransactionView):
    form_class = forms.TransferForm
    initial = {"txn_type": 6, "approval": True}
    extra_context = {
        "subtitle": "Transfer"
    }

    def form_valid(self, form):
        # gets transection amount
        amount = form.cleaned_data["amount"]
        # gets current account and update balance
        account = self.request.user.account
        account.balance -= amount

        # gets the other account and update balance & post transaction balance
        to_account_obj = form.to_account_obj
        to_account_obj.balance += amount
        to_aacount_balance_post_txn = to_account_obj.balance + amount

        # create new transaction for the other account
        new_trasnaction = Transaction(
            account = to_account_obj,
            amount = amount,
            balance_post_txn = to_aacount_balance_post_txn,
            txn_type = 5,
            approval = True
        )
        
        # save the new transaction
        new_trasnaction.save()
        # save the account since the balance is updated
        account.save()
        # save the other account since the blance is updated
        to_account_obj.save()
        
        # the form gets saved automatically

        messages.success(self.request, "Transfer Successfull")

        return super().form_valid(form)

