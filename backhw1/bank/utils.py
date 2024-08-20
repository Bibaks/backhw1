from django.db import transaction
from bank.models import BankAccount

def transfer_money(sender_account_id, receiver_account_id, amount):
    try:
        sender = BankAccount.objects.get(account_id=sender_account_id)
        receiver = BankAccount.objects.get(account_id=receiver_account_id)

        if sender.stock < amount:
            return "Insufficient funds"

        with transaction.atomic():
            sender.stock -= amount
            sender.save()

            receiver.stock += amount
            receiver.save()

        return f"Transferred {amount} from {sender.account_id} to {receiver.account_id}"

    except BankAccount.DoesNotExist:
        return "One or both accounts do not exist"

