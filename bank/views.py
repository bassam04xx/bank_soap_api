# bank/views.py
from bank.models import Account, Transaction
from spyne import Application, rpc, ServiceBase, Unicode, Decimal
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

accounts = {}  # Placeholder for storing account data in memory

class BankService(ServiceBase):
    @rpc(Account, _returns=Unicode)
    def create_account(ctx, account):
        accounts[account.account_name] = account.balance
        return f"Account {account.account_name} created with balance {account.balance}"

    @rpc(Transaction, _returns=Unicode)
    def deposit(ctx, transaction):
        if transaction.account_name in accounts:
            accounts[transaction.account_name] += transaction.amount
            return f"Deposited {transaction.amount} to {transaction.account_name}"
        return f"Account {transaction.account_name} not found."

    @rpc(Transaction, _returns=Unicode)
    def withdraw(ctx, transaction):
        if transaction.account_name in accounts:
            if accounts[transaction.account_name] >= transaction.amount:
                accounts[transaction.account_name] -= transaction.amount
                return f"Withdrew {transaction.amount} from {transaction.account_name}"
            return "Insufficient balance."
        return f"Account {transaction.account_name} not found."

    @rpc(Unicode, _returns=Unicode)
    def get_account_balance(ctx, account_name):
        if account_name in accounts:
            return f"Balance for {account_name} is {accounts[account_name]}"
        return f"Account {account_name} not found."

application = Application([BankService], 'bank.soap', in_protocol=Soap11(), out_protocol=Soap11())
django_app = DjangoApplication(application)

# Allow CORS for all requests

soap_app = csrf_exempt(DjangoApplication(application))

@csrf_exempt  # Exempt from CSRF validation
def soap_service(request):
    response = soap_app(request)
    return HttpResponse(response.content, content_type='text/xml')
