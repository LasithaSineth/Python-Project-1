# account/user.py
import re
from typing import List, TYPE_CHECKING

# To avoid circular imports for type hinting
if TYPE_CHECKING:
    from account.bank_account import BankAccount

class User:
    # Basic regex for email validation (can be more complex)
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __init__(self, name: str, email: str):
        if not name:
            raise ValueError("User name cannot be empty.")
        if not self.is_valid_email(email):
            # Raise error during creation if email is invalid
            raise ValueError(f"Invalid email format: {email}")

        self.name: str = name
        self.email: str = email
        self.accounts: List['BankAccount'] = [] # Use forward reference string

    def add_account(self, account: 'BankAccount'): # Use forward reference string
        self.accounts.append(account)

    def get_total_balance(self) -> float:
        # Correctly sum balances from all accounts
        return sum(account.get_balance() for account in self.accounts)

    def get_account_count(self) -> int:
        # Return the actual number of accounts
        return len(self.accounts)

    # def remove_account(self, account):
    #     # Placeholder - Implementation needed if required
    #     # self.accounts.remove(account) ? Needs logic to identify account.
    #     return "Account removal not implemented"

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        # Implement basic email validation
        if email and re.match(cls.EMAIL_REGEX, email):
            return True
        return False

    def __str__(self) -> str:
        # Updated string representation with correct methods
        return f"{self.name} ({self.email}) - {self.get_account_count()} account(s), Total Balance: Rs. {self.get_total_balance():.2f}"