# account/bank_account.py
from account.transaction import Transaction
from typing import List

class BankAccount:
    def __init__(self, initial_balance: float = 0.0):
        # Validate initial balance
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ValueError("Initial balance must be a non-negative number.")
        self.balance: float = float(initial_balance)
        self.transactions_history: List[Transaction] = []
        # Add initial balance as a deposit if it's positive
        if initial_balance > 0:
             self.transactions_history.append(Transaction(initial_balance, "deposit"))
        self.account_type: str = "Generic" # Base type

    def deposit(self, amount: float):
        # Validate deposit amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            # Raise error for invalid amount
            raise ValueError("Deposit amount must be a positive number.")
        self.balance += amount
        self.transactions_history.append(Transaction(amount, "deposit"))
        print(f"Deposit successful. New balance: Rs. {self.balance:.2f}") # Feedback

    def withdraw(self, amount: float):
        # Validate withdrawal amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            # Raise error for invalid amount
            raise ValueError("Withdrawal amount must be a positive number.")

        # Check for sufficient funds BEFORE withdrawal
        if self.balance < amount:
            # Raise error for insufficient funds
            raise ValueError(f"Insufficient Balance! Available: Rs. {self.balance:.2f}, Needed: Rs. {amount:.2f}")

        # Corrected logic: subtract amount
        self.balance -= amount
        self.transactions_history.append(Transaction(amount, "withdraw"))
        # Optional: Print success message here if not handled by caller
        # print(f"Withdrawal successful. New balance: Rs. {self.balance:.2f}")

    def get_balance(self) -> float:
        return self.balance

    def get_transaction_history(self) -> List[Transaction]:
        return self.transactions_history

    def get_account_type(self) -> str:
        return self.account_type

# --- Specific Account Types ---

class SavingsAccount(BankAccount):
    MIN_BALANCE = 100.0 # Define minimum balance as float

    def __init__(self, initial_balance: float = 0.0):
        super().__init__(initial_balance)
        self.account_type = "Savings Account" # Consistent naming

    def withdraw(self, amount: float):
        # Validate amount first (inherited check from super().withdraw will handle positive check)
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number.")

        # Check minimum balance rule BEFORE attempting withdrawal
        if (self.balance - amount) < self.MIN_BALANCE:
            raise ValueError(f"Withdrawal failed. Balance cannot fall below minimum of Rs. {self.MIN_BALANCE:.2f}")
        # If check passes, proceed with the withdrawal using parent method
        super().withdraw(amount) # This will handle amount validation and balance check again (redundant but safe)

    def get_account_type(self) -> str:
        return "Savings Account"

class CurrentAccount(BankAccount):
    def __init__(self, initial_balance: float = 0.0):
        super().__init__(initial_balance)
        self.account_type = "Current Account" # Consistent naming

    # No special withdraw rules, inherits base BankAccount.withdraw
    def get_account_type(self) -> str:
        return "Current Account"

class StudentAccount(BankAccount):
    MIN_BALANCE_ALLOWED = 0.0 # Students can potentially go to 0, but check specific rules
    WITHDRAW_LIMIT_MSG = "A minimum balance of Rs. 0.00 needed to withdraw from a Students account!" # Adjust if needed

    def __init__(self, initial_balance: float = 0.0):
        super().__init__(initial_balance)
        self.account_type = "Student Account" # Consistent naming

    def withdraw(self, amount: float):
         # Validate amount first
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number.")

        # Check minimum balance rule BEFORE attempting withdrawal
        # Assuming students account can go down to 0, but not below.
        # The original check `(self.balance - amount) < 100` seemed arbitrary,
        # let's enforce it cannot go below MIN_BALANCE_ALLOWED (e.g., 0)
        if (self.balance - amount) < self.MIN_BALANCE_ALLOWED:
            raise ValueError(f"Withdrawal failed. Balance cannot fall below Rs. {self.MIN_BALANCE_ALLOWED:.2f}")
        # If check passes, proceed with the withdrawal
        super().withdraw(amount)

    def get_account_type(self) -> str:
        return "Student Account"