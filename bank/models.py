# bank/models.py
from spyne import ComplexModel, Unicode, Decimal

class Account(ComplexModel):
    account_name = Unicode
    balance = Decimal

class Transaction(ComplexModel):
    account_name = Unicode
    amount = Decimal
    transaction_type = Unicode  # 'deposit' or 'withdrawal'
