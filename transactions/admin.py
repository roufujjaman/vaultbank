from django.contrib import admin
from .models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'txn_type', 'created_at', 'approval']

    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.balance_post_txn = obj.account.balance
        obj.account.save()
        return super().save_model(request, obj, form, change)



admin.site.register(Transaction, TransactionAdmin)
