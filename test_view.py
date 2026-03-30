import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
django.setup()

from django.test import Client
from apps.account.models import CreditCard, Account
from django.urls import reverse

a = Account.objects.first()
if not a:
    print("No account. Exiting.")
    sys.exit(0)

from apps.transaction.models import Transaction
Transaction.objects.all().delete()
CreditCard.objects.all().delete()

client = Client()
url = reverse('integrations:transaction_import')
print(f"Testing URL with Account ID {a.id}")
with open('docs/Fatura_Porto_Seguro_2026-03-30.xlsx', 'rb') as f:
    resp = client.post(url, {
        'institution': 'porto',
        'file_type': 'excel',
        'file': f,
        'account_id': a.id,
        'year': 2026
    })

print('Status:', resp.status_code)
if resp.status_code == 200:
    print('JSON:', resp.json())
else:
    print('Content:', resp.content.decode('utf-8'))

print("Credit Cards Created:")
for c in CreditCard.objects.all():
    print(f"- {c.name} (Suffix: {c.card_suffix}) -> {c.transactions.count()} transactions")
