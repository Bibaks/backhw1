from django.db import models

class Person(models.Model):
    full_name = models.CharField(max_length=100)
    person_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.full_name


class BankAccount(models.Model):
    account_id = models.CharField(max_length=20, unique=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Added index on stock
    owner = models.ForeignKey(Person, related_name='accounts', on_delete=models.CASCADE)

    def __str__(self):
        return f"Account {self.account_id} owned by {self.owner.full_name}"
