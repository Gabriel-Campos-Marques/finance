from django.urls import path
from .views import TransactionImportView, MobillsExportView

app_name = 'integrations'

urlpatterns = [
    path('import/', TransactionImportView.as_view(), name='transaction_import'),
    path('export/mobills/', MobillsExportView.as_view(), name='export_mobills'),
]
