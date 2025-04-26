# transaction.py
from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type):
        # Basic validation
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Transaction amount must be a positive number.")
        if transaction_type not in ["deposit", "withdraw"]:
            raise ValueError("Invalid transaction type.")

        self.amount = amount
        self.transaction_type = transaction_type  # "deposit" or "withdraw"
        self.timestamp = datetime.now()

    def __str__(self):
        # Consistent currency symbol
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.transaction_type.upper()}: Rs. {self.amount:.2f}"