from django.db import models
from apps.core.models import BaseModel

class Transaction(BaseModel):
    PAYMENT_METHODS = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
        ('pix', 'Pix'),
        ('cash', 'Cash'),
        ('transfer', 'Transfer')
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('category.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='transactions')
    credit_card = models.ForeignKey('account.CreditCard', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    transaction_date = models.DateField()
    import_hash = models.CharField(max_length=255, unique=True, null=True, blank=True, help_text="Hash to prevent duplicate imports")

    def __str__(self):
        return self.description
