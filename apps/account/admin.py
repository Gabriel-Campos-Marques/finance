from django.contrib import admin
from .models import Account, CreditCard

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'limit', 'statement_closing_date', 'statement_due_date', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'account')
