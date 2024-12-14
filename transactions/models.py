from django.db import models
from accounts.models import Account

TRANSACTION_TYPE = (
    (1, 'Deposit'),
    (2, 'Withdrawal'),
    (3, 'Loan'),
    (4, 'Payment'),
    (5, 'Received'),
    (6, 'Sent')
)

class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name="transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_post_txn = models.DecimalField(decimal_places=2, max_digits=12)
    txn_type = models.IntegerField(choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount}[{self.txn_type}]"
    
    
    class Meta:
        ordering = ["created_at"]
    


# class Loan(models.Model):
#     account = models.ForeignKey(Account, related_name="loan", on_delete=models.CASCADE)
#     amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    