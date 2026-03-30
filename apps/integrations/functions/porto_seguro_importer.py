import pandas as pd
import hashlib
from datetime import datetime
from apps.integrations.functions.interfaces import FileImporterInterface
from apps.transaction.models import Transaction
from apps.account.models import CreditCard
import math

class PortoSeguroInvoiceImporter(FileImporterInterface):
    def __init__(self, file_path, account_id, year):
        self.file_path = file_path
        self.account_id = account_id
        self.year = year

    def process(self):
        df = pd.read_excel(self.file_path)
        
        # Check if account exists
        from apps.account.models import Account
        try:
            account = Account.objects.get(id=self.account_id)
        except Account.DoesNotExist:
            raise ValueError(f"Account with id {self.account_id} does not exist.")
        
        transactions_to_create = []
        seen_hashes = {}
        
        # We start with no active credit card.
        # As soon as we hit a header row (Holder name + Cartão digits), we load/create the credit card.
        active_credit_card = None
        
        for index, row in df.iterrows():
            # Get columns dynamically based on index
            col_0 = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
            col_1 = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
            col_2 = row.iloc[2] # Crédito
            col_3 = row.iloc[3] # Débito
            col_5 = str(row.iloc[5]).replace('.0', '').strip() if pd.notna(row.iloc[5]) else "" # Cartão
            
            # Identify card holder row: col_0 has name, col_5 has digits, débito/crédito are NaN
            if col_0 and col_5 and pd.isna(col_2) and pd.isna(col_3) and "TOTAL" not in col_0.upper():
                holder_name = col_0
                card_digits = col_5
                
                # Try finding a credit card with these digits in suffix
                active_credit_card = CreditCard.objects.filter(
                    account_id=self.account_id,
                    card_suffix=card_digits
                ).first()
                
                # If no perfect suffix match, try matching by name as fallback, though suffix is better
                if not active_credit_card:
                    active_credit_card = CreditCard.objects.filter(
                        account_id=self.account_id,
                        name__icontains=card_digits
                    ).first()
                
                # If still not found, auto-create it
                if not active_credit_card:
                    card_name = f"Porto Seguro - {holder_name} {card_digits}"
                    active_credit_card = CreditCard.objects.create(
                        name=card_name,
                        account=account,
                        limit=0, # Unknown limit
                        statement_closing_date=1, # Default 
                        statement_due_date=10,    # Default
                        card_suffix=card_digits
                    )
                continue
            
            # If we don't have an active card yet, we can't save transactions
            if not active_credit_card:
                continue

            date_str = col_0
            description = col_1
            credit_val = col_2
            debit_val = col_3
            
            # Skip rows gracefully
            if "TOTAL" in date_str.upper() or not date_str or not description:
                continue
            
            if pd.isna(credit_val) and pd.isna(debit_val):
                continue

            # Parse amount
            amount_val = 0.0
            if pd.notna(debit_val) and str(debit_val).strip() != "":
                try:
                    amount_val = float(debit_val)
                except ValueError:
                    pass
            elif pd.notna(credit_val) and str(credit_val).strip() != "":
                try:
                    amount_val = -float(credit_val)
                except ValueError:
                    pass
            
            if amount_val == 0.0:
                continue
                
            try:
                day, month = [int(x) for x in date_str.split('/')]
                transaction_date = datetime(self.year, month, day).date()
            except Exception:
                continue

            # Base hash containing the specific card so multiple cards can have same descriptions safely
            base_hash_string = f"{transaction_date.isoformat()}|{description}|{amount_val:.2f}|{active_credit_card.id}"
            
            count = seen_hashes.get(base_hash_string, 0)
            seen_hashes[base_hash_string] = count + 1
            
            final_hash_string = f"{base_hash_string}|{count}"
            import_hash = hashlib.sha256(final_hash_string.encode('utf-8')).hexdigest()

            if not Transaction.objects.filter(import_hash=import_hash).exists():
                txn = Transaction(
                    description=description[:255],
                    amount=amount_val,
                    category=None,
                    payment_method='credit',
                    account=account,
                    credit_card=active_credit_card,
                    transaction_date=transaction_date,
                    import_hash=import_hash
                )
                transactions_to_create.append(txn)
                
        if transactions_to_create:
            Transaction.objects.bulk_create(transactions_to_create)
            
        return [txn.import_hash for txn in transactions_to_create]
