from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Account, Address

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "first_name", "last_name"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        # fields = "__all__"
        exclude = ["user", "account_no", "balance"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"})
        } 



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        # fields = "__all__"
        exclude = ["user"]


# class CreateAccountForm(UserCreationForm):
#     # user = forms.OneToOneField(User, on_delete=forms.CASCADE, related_name="accounts")
#     # account_no = forms.IntegerField(unique=True)
#     account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
#     birth_date = forms.DateField()
#     gender = forms.ChoiceField(choices=GENDER_TYPE)

#     street = forms.CharField(max_length=100)
#     city = forms.CharField(max_length=100)
#     postal_code = forms.IntegerField()
#     country = forms.CharField(max_length=100)

#     class Meta:
#         model = User
#         fields = ["first_name", "last_name", "email"]

    
#     def save(self, commit=True):
#         new_user = super().save(commit=False)
#         if commit == True:
#             new_user.save()
#             account_type = self.cleaned_data.get("account_type")
#             birth_date = self.cleaned_data.get("")
#             gender =
#             street =
#             city =
#             postal_code =
#             country =


