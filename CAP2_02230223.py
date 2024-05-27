import random     # Importing the random module for generating random numbers
import os      # Importing the os module for file operations

class BankAccount:
    account_types = ["Savings", "Current"]     # Defining available account types


    def __init__(self, name, account_type, balance=0):
        self.account_number = random.randint(100000000, 999999999)    # Generating a random account number
        self.password = str(random.randint(1000, 9999))     # Generating a random password
        self.name = name
        self.account_type = account_type
        self.balance = balance 

    def deposit(self, amount):
        self.balance += amount      # Increasing the balance by the deposit amount
        print(f"Successfully deposited Nu.{amount}. New balance: Nu.{self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount       # Decreasing the balance by the withdrawal amount if sufficient funds
            print(f"Successfully withdrawn Nu.{amount}. New balance: Nu.{self.balance}")
        else:
            print("Insufficient funds.")

    def transfer(self, other_account, amount):
        if self.balance >= amount:
            self.balance -= amount     # Decreasing the balance by the transfer amount
            other_account.balance += amount     # Increasing the recipient's balance by the transfer amount
            print(f"Successfully transferred Nu.{amount} to account {other_account.account_number}. New balance: Nu.{self.balance}")
        else:
            print("Insufficient funds.")

    def __str__(self):
        return f"Account Number: {self.account_number}\nPassword: {self.password}\nName: {self.name}\nAccount Type: {self.account_type}\nBalance: Nu.{self.balance}"

class PersonalAccount(BankAccount):
    def __init__(self, name, account_type, balance=0):
        super().__init__(name, account_type, balance)    # Initializing a personal account


class BusinessAccount(BankAccount):
    def __init__(self, name, account_type, balance=0):
        super().__init__(name, account_type, balance)       # Initializing a business account


accounts = []

def load_accounts():
    global accounts
    if os.path.isfile("accounts.txt"):      # Checking if the accounts file exists
        with open("accounts.txt", "r") as f:
            for line in f:
                account_number, password, name, account_type, balance = line.strip().split(",")
                if account_type == "Savings":
                    account = PersonalAccount(name, account_type, float(balance))
                else:
                    account = BusinessAccount(name, account_type, float(balance))
                account.account_number = int(account_number)
                account.password = password
                accounts.append(account)

def save_accounts():
    with open("accounts.txt", "w") as f:
        for account in accounts:
            f.write(f"{account.account_number},{account.password},{account.name},{account.account_type},{account.balance}\n")

def create_account():
    name = input("Enter your name: ")
    account_type = input(f"Enter account type ({', '.join(BankAccount.account_types)}): ")
    if account_type not in BankAccount.account_types:
        print("Invalid account type.")
        return
    if account_type == "Savings":
        account = PersonalAccount(name, account_type)
    else:
        account = BusinessAccount(name, account_type)
    accounts.append(account)
    print(f"Account created successfully!\n{account}")
    save_accounts()

def login():
    account_number = int(input("Enter your account number: "))
    password = input("Enter your password: ")
    for account in accounts:
        if account.account_number == account_number and account.password == password:
            return account       # Returning the account if login credentials are correct
    print("Invalid account number or password.")
    return None

def delete_account(account):
    accounts.remove(account)
    print("Account deleted successfully.")
    save_accounts()

def main():
    load_accounts()
    while True:
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            account = login()
            if account:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        print(f"Balance: Nu.{account.balance}")
                    elif choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        save_accounts()
                    elif choice == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        save_accounts()
                    elif choice == "4":
                        recipient_account_number = int(input("Enter recipient account number: "))
                        recipient_account = next((a for a in accounts if a.account_number == recipient_account_number), None)
                        if recipient_account:
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(recipient_account, amount)
                            save_accounts()
                        else:
                            print("Invalid recipient account number.")
                    elif choice == "5":
                        delete_account(account)
                        break
                    elif choice == "6":
                        break
                    else:
                        print("Invalid choice.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()