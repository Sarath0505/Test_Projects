# Defining Functions
# Current Balance
def current_balance(balance):
    print(f"Your Balance is {balance:.2f}")
#Deposit Function
def deposit(balance):
    amount = input("Please enter an amount to deposit or * to cancel : ")

    if amount == '*':
        return 0
    try:
        amount = float(amount)
    except ValueError:
        print("invalid entry")
        return 0

    if float(amount) <= 0:
        print("Amount can't be less than zero")
        return 0
    else:
        return float(amount)
# Withdraw Function
def withdraw(balance):
    amount = input("Please enter an amount to be withdrawn 0r * to cancel: ")

    if amount == '*':
        return 0
    try:
        amount = float(amount)
    except ValueError:
        print("invalid entry")
        return 0

    if float(amount) > balance:
        print("Insufficient Balance")
        return 0
    if float(amount) <= 0:
        print("Invalid amount")
        return 0
    else:
        return float(amount)
# Transaction History
def transaction_history(history):
    if not history:
        print("No Transactions Yet")
        return
# Iterating Each transaction done in the program into a list of dictionaries
    for transaction in history:
        print(
            f"{transaction['type']}: "
            f"Amount = {transaction['amount']:.2f},"
            f"Balance Before = {transaction['before']:.2f},"
            f"Balance After = {transaction['after']:.2f},"
        )
def main():
#Declared Global Variables

    balance = 0
    is_running = True
    history = []


# Program
    while is_running:
        print("-"*35)
        print("Welcome to Koya's Banking")
        print("-" * 35)
        print("Please select your choice")
        print("1.Balance")
        print("2.Deposit")
        print("3.Withdraw")
        print("4.Transaction History")
        print("5.Exit")
        print("-" * 35)

        choice = input("Please Enter a number 1-5: ")
# Current Balance
        if choice == '1':
            print("-" * 35)
            current_balance(balance)
# Deposit Amount
        elif choice == '2':
            print("-" * 35)
            amount = deposit(balance)
            if amount > 0:
                before = balance
                balance += amount
                history.append({
                    "type": "Deposit",
                    "amount": amount,
                    "before": before,
                    "after": balance
                })
# Withdraw
        elif choice == '3':
            print("-" * 35)
            amount = withdraw(balance)
            if amount > 0:
                before = balance
                balance -= amount
                history.append({
                    "type": "Withdraw",
                    "amount": amount,
                    "before": before,
                    "after": balance
                })
# Transaction History
        elif choice == '4':
            print("-" * 35)
            transaction_history(history)
        elif choice == '5':
            is_running = False
        else:
            print("Invalid Choice")

    print("-" * 35)
    print("Thank you For banking with Koya's")
    print("-" * 35)

if __name__ == "__main__":
    main()