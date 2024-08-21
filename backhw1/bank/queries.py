from django.db.models import *
from bank.models import *
from faker import Faker
import random
from django.db.models import Max
from django.db import transaction
import time
from django.db.models import Sum


#q1

# Initialize Faker
faker = Faker()

# Create random Person records
people = []
for _ in range(1000):  # Creating 1000 random people
    people.append(Person(full_name=faker.name(), person_id=faker.unique.random_number(digits=10, fix_len=True)))

Person.objects.bulk_create(people)

# Fetch all created people to assign them accounts
people = Person.objects.all()

# Create 20,000 bank account records
accounts = []  # Make sure to initialize the accounts list

for _ in range(20000):
    accounts.append(BankAccount(
        account_id=faker.unique.bothify(text='????-########'),  # Random account id
        stock=random.uniform(100.00, 10000.00),  # Random stock balance
        owner=random.choice(people)  # Assigning a random owner from the created people
    ))

# Bulk create 20,000 accounts
BankAccount.objects.bulk_create(accounts)

print("20,000 records have been successfully created!")


#q2

def account_owner():
    return Person.objects.annotate(account_balance=Sum('accounts__stock')).values("account_balance",'full_name')

#q3

# Get the maximum stock value
max_stock = BankAccount.objects.aggregate(Max('stock'))['stock__max']

# Retrieve the account with the maximum stock
account_with_max_stock = BankAccount.objects.filter(stock=max_stock).select_related('owner').first()

# Print the account details
print(f"Account ID: {account_with_max_stock.account_id}, Owner: {account_with_max_stock.owner.full_name}, Stock: {account_with_max_stock.stock}")


#q4

# Get the 5 accounts with the least stock
accounts_with_least_stock = BankAccount.objects.all().order_by('stock')[:5]

# Print the account details
for account in accounts_with_least_stock:
    print(f"Account ID: {account.account_id}, Owner: {account.owner.full_name}, Stock: {account.stock}")


#q5

# this is in utild.py file

from bank.utils import transfer_money



#q6


# Get accounts where account ID (numeric part) is greater than stock
accounts = BankAccount.objects.all()

# Filter accounts where account ID (as an integer) is greater than the stock
matching_accounts = []

for account in accounts:
    try:
        # Convert account_id to an integer (this will fail for non-numeric IDs)
        account_id_as_int = int(account.account_id)

        # Print account ID and stock for debugging
        print(f"Checking Account ID: {account.account_id} (as int: {account_id_as_int}), Stock: {account.stock}")

        # Compare account ID as integer with the stock
        if account_id_as_int > account.stock:
            matching_accounts.append(account)
    except ValueError:
        # Skip accounts with non-numeric account IDs
        print(f"Skipped non-numeric Account ID: {account.account_id}")

# Print the matching accounts
if matching_accounts:
    for account in matching_accounts:
        print(f"Account ID: {account.account_id}, Stock: {account.stock}")
else:
    print("No accounts found where Account ID (as integer) is greater than Stock.")


#q7

# Get accounts where owner's person_id (numeric part) is greater than stock
accounts = BankAccount.objects.select_related('owner').all()

# Filter accounts where owner's person_id (as an integer) is greater than the stock
matching_accounts = []

for account in accounts:
    try:
        # Convert owner.person_id to an integer
        owner_id_as_int = int(account.owner.person_id)

        # Print owner ID and stock for debugging
        print(f"Checking Owner ID: {account.owner.person_id} (as int: {owner_id_as_int}), Stock: {account.stock}")

        # Compare owner ID as integer with the stock
        if owner_id_as_int > account.stock:
            matching_accounts.append(account)
    except ValueError:
        # Skip owners with non-numeric IDs
        print(f"Skipped non-numeric Owner ID: {account.owner.person_id}")

# Print the matching accounts
if matching_accounts:
    for account in matching_accounts:
        print(f"Account ID: {account.account_id}, Owner ID: {account.owner.person_id}, Stock: {account.stock}")
else:
    print("No accounts found where Owner ID is greater than Stock.")


#q8



faker = Faker()

# Fetch all persons (you might want to create some if needed)
people = Person.objects.all()

# Create 10 million bank account records in batches
batch_size = 10000  # Create 10,000 at a time to avoid memory overload
accounts = []

for _ in range(10000000):  # 10 million iterations
    accounts.append(BankAccount(
        account_id=faker.unique.bothify(text='????-########'),
        stock=random.uniform(0.5 * 10**6, 3 * 10**6),  # Stock between 0.5M and 3M
        owner=random.choice(people)
    ))

    if len(accounts) >= batch_size:
        BankAccount.objects.bulk_create(accounts)
        accounts = []

# Insert any remaining accounts
if accounts:
    BankAccount.objects.bulk_create(accounts)

print("10 million records created.")

#Query Without Index

start_time = time.time()

accounts_no_index = BankAccount.objects.filter(stock__gt=2 * 10**6) | BankAccount.objects.filter(stock__lt=1 * 10**6)
accounts_no_index = list(accounts_no_index)

end_time = time.time()

print(f"Query without index took {end_time - start_time} seconds.")

# Query with index
start_time = time.time()

accounts_with_index = BankAccount.objects.filter(stock__gt=2 * 10**6) | BankAccount.objects.filter(stock__lt=1 * 10**6)
accounts_with_index = list(accounts_with_index)

end_time = time.time()

print(f"Query with index took {end_time - start_time} seconds.")


#q9

# Query to sum the stock of each person
people_with_stock = Person.objects.annotate(total_stock=Sum('accounts__stock'))

# Print each person's name and their total stock
for person in people_with_stock:
    print(f"Person: {person.full_name}, Total Stock: {person.total_stock}")

