import os
import pandas as pd
from io import BytesIO
from django.conf import settings
from apps.transaction.models import Transaction

class MobillsExporter:
    
    @staticmethod
    def export(start_date=None, end_date=None):
        """
        Exports transactions from the database into the official Mobills Excel template format.
        """
        # Load the template
        template_path = os.path.join(settings.BASE_DIR, 'docs', 'Planilha modelo de importação (Português) oficial.xlsx')
        
        # Read only columns to keep exactly Mobills format
        try:
            df_template = pd.read_excel(template_path)
            columns = df_template.columns.tolist()
        except FileNotFoundError:
            # Fallback if file is moved: 'Data', 'Descrição', 'Valor', 'Conta', 'Categoria'
            columns = ['Data', 'Descrição', 'Valor', 'Conta', 'Categoria']

        # Query transactions
        queryset = Transaction.objects.all().select_related('account', 'credit_card', 'category')
        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)
            
        data = []
        for txn in queryset:
            # Data format: YYYY-MM-DD
            data_str = txn.transaction_date.strftime('%Y-%m-%d')
            
            # Descrição
            desc = txn.description
            
            # Valor: Negate if it's an expense. A transaction with 'credit' payment method or uncharacterized debit 
            # In our current models, amounts are kept positive. So we negate them for expenses.
            # Assuming all stored 'amount' are positive absolute values, and we treat them as debits
            # unless we have a specific income tracking logic (e.g. category income).
            # We will negate the amount by default for credit card expenses.
            
            amount = float(txn.amount)
            # Make it negative. (In the future, income transactions should remain positive).
            amount = -abs(amount)
            
            # Conta
            if txn.credit_card:
                conta = txn.credit_card.name
            else:
                conta = txn.account.name
                
            # Categoria
            categoria = txn.category.name if txn.category else "Outros"
            
            data.append([data_str, desc, amount, conta, categoria])
            
        # Create DataFrame
        df_export = pd.DataFrame(data, columns=columns)
        
        # Write to BytesIO directly to return to user 
        output = BytesIO()
        # Create an Excel writer
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Sheet1')
            
        output.seek(0)
        return output
