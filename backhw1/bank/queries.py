from django.db.models import *
from bank.models import *

def account_owner():
    return Person.objects.annotate(account_balance=Sum('accounts__stock')).values("account_balance",'full_name')