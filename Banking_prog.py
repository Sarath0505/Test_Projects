
def current_balance():
    print(f"Your Balance is {balance:.2f}")

def deposit():
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

def withdraw():
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

def transaction_history():
    if not history:
        print("No Transactions Yet")
        return

    for transaction in history:
        print(
            f"{transaction['type']}: "
            f"Amount = {transaction['amount']:.2f},"
            f"Balance Before = {transaction['before']:.2f},"
            f"Balance After = {transaction['after']:.2f},"
        )

balance = 0
is_running = True
history = []

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

    if choice == '1':
        print("-" * 35)
        current_balance()
    elif choice == '2':
        print("-" * 35)
        amount = deposit()
        if amount > 0:
            before = balance
            balance += amount
            history.append({
                "type": "Deposit",
                "amount": amount,
                "before": before,
                "after": balance
            })
    elif choice == '3':
        print("-" * 35)
        amount = withdraw()
        if amount > 0:
            before = balance
            balance -= amount
            history.append({
                "type": "Withdraw",
                "amount": amount,
                "before": before,
                "after": balance
            })
    elif choice == '4':
        print("-" * 35)
        transaction_history()
    elif choice == '5':
        is_running = False
    else:
        print("Invalid Choice")

print("-" * 35)
print("Thank you For banking with Koya's")
print("-" * 35)
