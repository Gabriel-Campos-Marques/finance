from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'transaction_date', 'category', 'payment_method', 'account', 'is_active')
    search_fields = ('description',)
    list_filter = ('transaction_date', 'payment_method', 'is_active', 'account', 'credit_card')
    date_hierarchy = 'transaction_date'
    raw_id_fields = ('category', 'account', 'credit_card')
