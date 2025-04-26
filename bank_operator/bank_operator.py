from account.user import User
from account.bank_account import BankAccount, SavingsAccount, CurrentAccount, StudentAccount

users = []

def create_user():
    name = input("Enter name: ")
    email = input("Enter email: ")
    user = User(name, email)
    if not user.is_valid_email(email):
        print("Invalid email format! Please enter a valid email address.")
        return
    users.append(user)
    print(f"User {name} created.\n")

def list_users():
    if not users:
        print("No users available. Please create a user first.")
        return
    for i, user in enumerate(users):
        print(f"{i+1}. {user}")

def create_account():
    if not users:
        print("No users available. Please create a user first.")
        return
    list_users()
    try:
        idx = int(input("Select user number: ")) - 1
        if idx < 0 or idx >= len(users):
            print("Invalid user selection.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return

    print("Account Type:")
    print("1. Savings Account")
    print("2. Students Account")
    print("3. Current Account")
    try:
        account_choice = int(input("Enter your choice (1, 2, 3): "))
        if account_choice not in [1, 2, 3]:
            print("Invalid account type!")
            return
    except ValueError:
        print("Invalid account type!")
        return

    amount = float(input("Enter initial deposit: "))
    if amount < 0:
        print("Initial deposit must be a positive number!")
        return

    if account_choice == 1:
        account = SavingsAccount(amount)
    elif account_choice == 2:
        account = StudentAccount(amount)
    else:
        account = CurrentAccount(amount)

    users[idx].add_account(account)
    print(f"{account.get_account_type()} added!\n")

def deposit_money():
    list_users()
    try:
        idx = int(input("Select user: ")) - 1
        if idx < 0 or idx >= len(users):
            print("Invalid user selection.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return

    user = users[idx]
    for i, acc in enumerate(user.accounts):
        print(f"{i+1}. Balance: Rs. {acc.get_balance()}")
    
    try:
        acc_idx = int(input("Select account: ")) - 1
        if acc_idx < 0 or acc_idx >= len(user.accounts):
            print("Invalid account selection.\n")
            return
    except ValueError:
        print("Invalid input. Please select a valid account.\n")
        return

    amount = float(input("Enter amount to deposit: "))  # Fixed bug
    if amount <= 0:
        print("Deposit amount must be greater than zero.\n")
        return
    user.accounts[acc_idx].deposit(amount)

def withdraw_money():
    list_users()
    try:
        idx = int(input("Select user: ")) - 1
        if idx < 0 or idx >= len(users):
            print("Invalid user selection.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return

    user = users[idx]
    for i, acc in enumerate(user.accounts):
        print(f"{i+1}. Balance: Rs. {acc.get_balance()}")
    
    try:
        acc_idx = int(input("Select account: ")) - 1
        if acc_idx < 0 or acc_idx >= len(user.accounts):
            print("Invalid account selection.\n")
            return
    except ValueError:
        print("Invalid input. Please select a valid account.\n")
        return

    amount = float(input("Enter amount to withdraw: "))
    if amount <= 0:
        print("Withdrawal amount must be greater than zero.\n")
        return

    try:
        user.accounts[acc_idx].withdraw(amount)
        print("Withdrawal successful.\n")
    except ValueError as e:
        print(f"Error: {e}\n")

def view_transactions():
    list_users()
    try:
        idx = int(input("Select user: ")) - 1
        if idx < 0 or idx >= len(users):
            print("Invalid user selection.\n")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.\n")
        return

    user = users[idx]
    for i, acc in enumerate(user.accounts):
        print(f"\n{acc.get_account_type()} {i+1} - Balance: Rs. {acc.get_balance()}")
        for tx in acc.get_transaction_history():
            print(tx)
