from django.db import models
from apps.core.models import BaseModel

class Account(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CreditCard(BaseModel):
    name = models.CharField(max_length=255)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_cards')
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    statement_closing_date = models.IntegerField(help_text="Day of the month the statement closes")
    statement_due_date = models.IntegerField(help_text="Day of the month the statement is due")

    def __str__(self):
        return self.name
