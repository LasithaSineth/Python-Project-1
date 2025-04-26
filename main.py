# main.py
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
# Import the module itself
import bank_operator

# Initialize Rich Console
# It will automatically handle the print statements with formatting tags
# from bank_operator.py if they are output to the console.
console = Console()

def menu():
    """Displays the main menu and handles user choices."""
    while True:
        console.clear() # Optional: Clears screen

        table = Table(title="🏦 Bank System Menu", title_style="bold magenta", show_header=True, header_style="bold blue")

        table.add_column("Option", style="cyan", justify="center", width=6)
        table.add_column("Description", style="white")

        table.add_row("1", "Create User")
        table.add_row("2", "List Users")
        table.add_row("3", "Add Account")
        table.add_row("4", "Deposit")
        table.add_row("5", "Withdraw")
        table.add_row("6", "View Transactions")
        table.add_row("7", "Exit")

        console.print(table)

        choice = Prompt.ask("👉 Choose option", choices=[str(i) for i in range(1, 8)], default="7")

        console.print("-" * 30) # Separator

        if choice == '1':
            bank_operator.create_user()
        elif choice == '2':
            bank_operator.list_users()
        elif choice == '3':
            bank_operator.create_account()
        elif choice == '4':
            bank_operator.deposit_money()
        elif choice == '5':
            bank_operator.withdraw_money()
        elif choice == '6':
            bank_operator.view_transactions()
        elif choice == '7':
            console.print("\n👋 Exiting... Thank you for using the Bank System!", style="bold green")
            break # Exit the loop

        # Pause at the end of each operation before showing the menu again
        Prompt.ask("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()