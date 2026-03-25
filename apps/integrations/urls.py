from django.urls import path
from .views import TransactionImportView

app_name = 'integrations'

urlpatterns = [
    path('import/', TransactionImportView.as_view(), name='transaction_import'),
]
