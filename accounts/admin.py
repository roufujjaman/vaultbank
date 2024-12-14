from django.contrib import admin
from .models import Account, Address
# Register your models here.

class AccountsAdmin(admin.ModelAdmin):
    list_display = ["user", "account_no", "account_type"]

class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "street", "city", "postal_code", "country"]


admin.site.register(Account, AccountsAdmin)
admin.site.register(Address, AddressAdmin)
