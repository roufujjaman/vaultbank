# Generated by Django 5.0.2 on 2024-11-28 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_address_options_account_delete_accounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('balance_post_txn', models.DecimalField(decimal_places=2, max_digits=12)),
                ('txn_type', models.IntegerField(choices=[(1, 'Deposite'), (2, 'Withdrawal'), (3, 'Loan'), (4, 'Payment')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approval', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
