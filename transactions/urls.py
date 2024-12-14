from django.urls import path
from . import views

app_name = "transactions"
urlpatterns = [
    # path("", views.Home.as_view()),
    path("deposit", views.DepositView.as_view(), name="deposit"),
    path("withdraw", views.WithdrawView.as_view(), name="withdraw"),
    path("transfer", views.TransferView.as_view(), name="transfer"),
    path("loan", views.LoanRequestView.as_view(), name="loan"),
]