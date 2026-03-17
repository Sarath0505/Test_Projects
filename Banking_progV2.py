import sqlite3


DB_NAME = "bank.db"


# -------------------------
# Database Functions
# -------------------------
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            before_balance REAL NOT NULL,
            after_balance REAL NOT NULL,
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
    """)

    conn.commit()
    conn.close()


def load_data():
    accounts = {}

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Load accounts
    cursor.execute("SELECT account_number, name, balance FROM accounts")
    account_rows = cursor.fetchall()

    for account_number, name, balance in account_rows:
        accounts[account_number] = {
            "name": name,
            "balance": balance,
            "history": []
        }

    # Load transaction history
    cursor.execute("""
        SELECT account_number, type, amount, before_balance, after_balance
        FROM transactions
        ORDER BY id
    """)
    transaction_rows = cursor.fetchall()

    for account_number, txn_type, amount, before_balance, after_balance in transaction_rows:
        if account_number in accounts:
            accounts[account_number]["history"].append({
                "type": txn_type,
                "amount": amount,
                "before": before_balance,
                "after": after_balance
            })

    conn.close()
    return accounts


def save_data(accounts):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Clear old data
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM accounts")

    # Insert accounts and transactions from memory
    for account_number, account_data in accounts.items():
        cursor.execute("""
            INSERT INTO accounts (account_number, name, balance)
            VALUES (?, ?, ?)
        """, (account_number, account_data["name"], account_data["balance"]))

        for transaction in account_data["history"]:
            cursor.execute("""
                INSERT INTO transactions (
                    account_number, type, amount, before_balance, after_balance
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                account_number,
                transaction["type"],
                transaction["amount"],
                transaction["before"],
                transaction["after"]
            ))

    conn.commit()
    conn.close()


# -------------------------
# Account Functions
# -------------------------
def account_info(accounts):
    print("-" * 35)
    account_number = input("Enter account number: ").strip()
    name = input("Enter account holder name: ").strip()

    if not account_number:
        print("Account number cannot be empty.")
        return None

    if not name:
        print("Name cannot be empty.")
        return None

    if account_number in accounts:
        stored_name = accounts[account_number]["name"]
        if stored_name.lower() != name.lower():
            print(f"Account number already exists under the name '{stored_name}'.")
            print("Using the existing account.")
        else:
            print("Existing account loaded successfully.")
    else:
        accounts[account_number] = {
            "name": name,
            "balance": 0.0,
            "history": []
        }
        print("New account created successfully.")

    return account_number


# -------------------------
# Banking Functions
# -------------------------
def current_balance(accounts, current_account):
    balance = accounts[current_account]["balance"]
    print(f"Current Balance: {balance:.2f}")


def deposit(accounts, current_account):
    amount = input("Please enter an amount to deposit or * to cancel: ").strip()

    if amount == '*':
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid entry.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    before = accounts[current_account]["balance"]
    accounts[current_account]["balance"] += amount
    after = accounts[current_account]["balance"]

    accounts[current_account]["history"].append({
        "type": "Deposit",
        "amount": amount,
        "before": before,
        "after": after
    })

    print(f"Deposit successful. New balance: {after:.2f}")


def withdraw(accounts, current_account):
    amount = input("Please enter an amount to withdraw or * to cancel: ").strip()

    if amount == '*':
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid entry.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    current_balance_value = accounts[current_account]["balance"]

    if amount > current_balance_value:
        print("Insufficient balance.")
        return

    before = current_balance_value
    accounts[current_account]["balance"] -= amount
    after = accounts[current_account]["balance"]

    accounts[current_account]["history"].append({
        "type": "Withdraw",
        "amount": amount,
        "before": before,
        "after": after
    })

    print(f"Withdrawal successful. New balance: {after:.2f}")


def transaction_history(accounts, current_account):
    history = accounts[current_account]["history"]

    if not history:
        print("No transactions yet.")
        return

    print(f"Transaction History for Account {current_account} - {accounts[current_account]['name']}")
    print("-" * 70)

    for transaction in history:
        print(
            f"{transaction['type']}: "
            f"Amount = {transaction['amount']:.2f}, "
            f"Balance Before = {transaction['before']:.2f}, "
            f"Balance After = {transaction['after']:.2f}"
        )


# -------------------------
# Main Program
# -------------------------
def main():
    setup_database()
    accounts = load_data()

    print("-" * 35)
    print("Welcome to Koya's Banking")
    print("-" * 35)

    current_account = None

    while current_account is None:
        current_account = account_info(accounts)

    is_running = True

    while is_running:
        print("\n" + "-" * 35)
        print(f"Logged in as: {accounts[current_account]['name']} ({current_account})")
        print("-" * 35)
        print("1. Show Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Switch / Create Account")
        print("6. Exit")
        print("-" * 35)

        choice = input("Please enter a number 1-6: ").strip()

        if choice == '1':
            print("-" * 35)
            current_balance(accounts, current_account)

        elif choice == '2':
            print("-" * 35)
            deposit(accounts, current_account)

        elif choice == '3':
            print("-" * 35)
            withdraw(accounts, current_account)

        elif choice == '4':
            print("-" * 35)
            transaction_history(accounts, current_account)

        elif choice == '5':
            print("-" * 35)
            selected_account = account_info(accounts)
            if selected_account is not None:
                current_account = selected_account

        elif choice == '6':
            save_data(accounts)
            is_running = False

        else:
            print("Invalid choice.")

    print("-" * 35)
    print("All data saved to SQLite database.")
    print("Thank you for banking with Koya's.")
    print("-" * 35)


if __name__ == "__main__":
    main()