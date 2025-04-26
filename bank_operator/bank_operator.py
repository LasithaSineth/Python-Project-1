# bank_operator.py
from account.user import User
from account.bank_account import BankAccount, SavingsAccount, CurrentAccount, StudentAccount
from typing import List

# Global list to store users
users: List[User] = []

# --- Helper Functions ---

def _get_user_selection(prompt_message="Select user number: ") -> User | None:
    """Lists users and gets a valid user selection."""
    if not users:
        print("[bold red]No users available. Please create a user first.[/bold red]\n")
        return None

    list_users()
    while True:
        try:
            idx_str = input(prompt_message)
            idx = int(idx_str) - 1
            if 0 <= idx < len(users):
                return users[idx]
            else:
                # Issue #5 Fix: Invalid user selection message
                print("[bold red]Invalid user selection.[/bold red]\n")
                # Optional: Ask again or return None
                # return None # Or continue loop to ask again
        except ValueError:
            print("[bold red]Invalid input. Please enter a number.[/bold red]")
        # Add an option to cancel selection
        if input("Try again? (y/n): ").lower() != 'y':
            return None

def _get_account_selection(user: User, prompt_message="Select account number: ") -> BankAccount | None:
    """Lists accounts for a user and gets a valid account selection."""
    if not user.accounts:
        print(f"[bold yellow]User {user.name} has no accounts.[/bold yellow]\n")
        return None

    print(f"\nAccounts for {user.name}:")
    for i, acc in enumerate(user.accounts):
        print(f"{i+1}. {acc.get_account_type()} - Balance: Rs. {acc.get_balance():.2f}")

    while True:
        try:
            acc_idx_str = input(prompt_message)
            acc_idx = int(acc_idx_str) - 1
            if 0 <= acc_idx < len(user.accounts):
                return user.accounts[acc_idx]
            else:
                print("[bold red]Invalid account selection.[/bold red]\n")
        except ValueError:
            print("[bold red]Invalid input. Please enter a number.[/bold red]")
        # Add an option to cancel selection
        if input("Try again? (y/n): ").lower() != 'y':
            return None

def _get_positive_float_input(prompt_message: str) -> float | None:
    """Gets positive float input from the user."""
    while True:
        try:
            amount_str = input(prompt_message)
            amount = float(amount_str)
            if amount > 0:
                return amount
            else:
                print("[bold red]Amount must be positive.[/bold red]")
        except ValueError:
            print("[bold red]Invalid input. Please enter a number.[/bold red]")
        # Add an option to cancel
        if input("Try again? (y/n): ").lower() != 'y':
            return None


# --- Main Operations ---

def create_user():
    """Creates a new user."""
    print("\n--- Create New User ---")
    name = input("Enter name: ")
    email = input("Enter email: ")

    try:
        # Validation is now inside User.__init__ and is_valid_email
        user = User(name, email)
        users.append(user)
        print(f"[bold green]User '{name}' created successfully.[/bold green]\n")
    except ValueError as e:
        # Issue #7 Fix: Catch validation errors from User creation
        print(f"[bold red]Error creating user: {e}[/bold red]\n")

def list_users():
    """Lists all created users."""
    print("\n--- List of Users ---")
    if not users:
        print("No users in the system yet.")
        return

    for i, user in enumerate(users):
        # Use the __str__ method of the User class
        print(f"{i+1}. {user}")
    print("-" * 20)

def create_account():
    """Creates a new bank account for a selected user."""
    print("\n--- Add New Account ---")
    # Issue #1 & #4 Fix: Check if users exist before proceeding
    selected_user = _get_user_selection("Select user to add account for: ")
    if not selected_user:
        # Message already printed by _get_user_selection if no users exist
        return # Exit if no user selected or no users exist

    print("\nSelect Account Type:")
    print("1. Savings Account")
    print("2. Student Account") # Corrected name consistency
    print("3. Current Account")

    account_choice = None
    while account_choice is None:
        try:
            choice_str = input("Enter your choice (1, 2, 3): ")
            account_choice = int(choice_str)
            if account_choice not in [1, 2, 3]:
                # Issue #6 Fix: Handle invalid account type choice
                print("[bold red]Invalid account type![/bold red]")
                account_choice = None # Reset choice to loop again
                if input("Try again? (y/n): ").lower() != 'y':
                    return # Exit if user cancels
        except ValueError:
            print("[bold red]Invalid input. Please enter a number (1, 2, or 3).[/bold red]")
            if input("Try again? (y/n): ").lower() != 'y':
                 return # Exit if user cancels


    initial_deposit = _get_positive_float_input("Enter initial deposit amount (>= 0): ")
    # Allow 0 initial deposit, handle None if user cancelled input
    if initial_deposit is None:
         print("[bold yellow]Account creation cancelled.[/bold yellow]")
         return
    # Allow 0 deposit, but validate >=0
    while initial_deposit < 0 :
        print("[bold red]Initial deposit cannot be negative.[/bold red]")
        initial_deposit = _get_positive_float_input("Enter initial deposit amount (>= 0): ")
        if initial_deposit is None:
             print("[bold yellow]Account creation cancelled.[/bold yellow]")
             return


    account = None
    try:
        if account_choice == 1:
            account = SavingsAccount(initial_deposit)
        elif account_choice == 2:
            account = StudentAccount(initial_deposit)
        elif account_choice == 3:
            account = CurrentAccount(initial_deposit)
        # No 'else' needed because we validated account_choice

        if account:
            selected_user.add_account(account)
            print(f"[bold green]{account.get_account_type()} created successfully for {selected_user.name}.[/bold green]\n")

    except ValueError as e: # Catch potential errors from BankAccount init
        print(f"[bold red]Error creating account: {e}[/bold red]\n")


def deposit_money():
    """Deposits money into a selected user's account."""
    print("\n--- Deposit Money ---")
    selected_user = _get_user_selection("Select user for deposit: ")
    if not selected_user:
        return

    selected_account = _get_account_selection(selected_user, "Select account to deposit into: ")
    if not selected_account:
        return

    amount = _get_positive_float_input("Enter amount to deposit: ")
    if amount is None: # User cancelled input
        print("[bold yellow]Deposit cancelled.[/bold yellow]")
        return

    try:
        # Deposit method now handles validation and transaction recording
        selected_account.deposit(amount)
        # Success message is printed inside deposit() now
        # print(f"[bold green]Deposit successful. New balance: Rs. {selected_account.get_balance():.2f}[/bold green]\n")
    except ValueError as e:
        # Catch errors raised by the deposit method (e.g., invalid amount)
        print(f"[bold red]Deposit failed: {e}[/bold red]\n")


def withdraw_money():
    """Withdraws money from a selected user's account."""
    print("\n--- Withdraw Money ---")
    selected_user = _get_user_selection("Select user for withdrawal: ")
    if not selected_user:
        return

    selected_account = _get_account_selection(selected_user, "Select account to withdraw from: ")
    if not selected_account:
        return

    amount = _get_positive_float_input("Enter amount to withdraw: ")
    if amount is None: # User cancelled input
        print("[bold yellow]Withdrawal cancelled.[/bold yellow]")
        return

    try:
        # Withdraw method now handles validation, balance checks, rules, and raises ValueError
        selected_account.withdraw(amount)
        # Issue #2 Fix: Correct calculation is in withdraw(). Error handling catches issues.
        print(f"[bold green]Withdrawal successful. New balance: Rs. {selected_account.get_balance():.2f}[/bold green]\n")
    except ValueError as e:
        # Catch errors like insufficient funds, minimum balance violation, invalid amount
        print(f"[bold red]Withdrawal failed: {e}[/bold red]\n")

def view_transactions():
    """Views transaction history for a selected user's accounts."""
    print("\n--- View Transactions ---")
    selected_user = _get_user_selection("Select user to view transactions: ")
    if not selected_user:
        return

    if not selected_user.accounts:
        print(f"[bold yellow]User {selected_user.name} has no accounts.[/bold yellow]\n")
        return

    print(f"\n--- Transactions for {selected_user.name} ---")
    for i, acc in enumerate(selected_user.accounts):
        print(f"\n[bold cyan]Account {i+1}: {acc.get_account_type()} - Current Balance: Rs. {acc.get_balance():.2f}[/bold cyan]")
        history = acc.get_transaction_history()
        if not history:
            print("  No transactions yet.")
        else:
            for tx in history:
                print(f"  {tx}") # Use Transaction's __str__ method
    print("-" * 30)