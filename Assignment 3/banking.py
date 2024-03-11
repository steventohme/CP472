from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type, account_number):
        self.amount = amount
        self.transaction_type = transaction_type
        self.account_number = account_number
        self.date_time = datetime.now()

    def __str__(self):
        return f"{self.date_time} - {self.transaction_type} of ${self.amount} on account #{self.account_number}"


class TransactionHistory:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_last_n_transactions(self, n):
        return self.transactions[-n:]

    def get_all_transactions_of_type(self, transaction_type):
        return [transaction for transaction in self.transactions if transaction.transaction_type == transaction_type]


class BankAccount:
    def __init__(self, accountNumber, accountHolderName, balance=0.0):
        self.accountNumber = accountNumber
        self.accountHolderName = accountHolderName
        self.balance = balance
        self.transaction_history = TransactionHistory()

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Account: #{self.accountNumber} Deposited ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "deposit", self.accountNumber))
        else:
            print("Invalid deposit amount.\n")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Withdrew ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "withdrawal", self.accountNumber))
        else:
            print("Invalid withdrawal amount or insufficient funds.\n")


class SavingsAccount(BankAccount):
    def __init__(self, accountNumber, accountHolderName, balance=0.0, minBalance=100.0):
        super().__init__(accountNumber, accountHolderName, balance)
        self.minBalance = minBalance

    def withdraw(self, amount):
        if amount > 0 and (self.balance - amount) >= self.minBalance:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Withdrew ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "withdrawal", self.accountNumber))
        else:
            print("Invalid withdrawal amount or would violate minimum balance for savings account.\n")


class CheckingAccount(BankAccount):
    def __init__(self, accountNumber, accountHolderName, balance=0.0):
        super().__init__(accountNumber, accountHolderName, balance)


class User:
    def __init__(self, username, checking_account=None, savings_account=None):
        self.username = username
        self.checking_account = checking_account
        self.savings_account = savings_account

    def transfer_to_user_savings(self, amount, user):
        print(f"User: {self.username} transferring ${amount} to User: {user.username}'s savings account.\n")
        if self.checking_account.balance >= amount:
            self.checking_account.withdraw(amount)
            user.savings_account.deposit(amount)
            self.checking_account.transaction_history.add_transaction(Transaction(amount, "transfer", user.savings_account.accountNumber))
            user.savings_account.transaction_history.add_transaction(Transaction(amount, "deposit", user.savings_account.accountNumber))
        else:
            print("Insufficient funds for transfer.\n")

    def transfer_to_user_checking(self, amount, user):
        print(f"User: {self.username} transferring ${amount} to User: {user.username}'s checking account.\n")
        if self.savings_account.balance >= amount:
            self.savings_account.withdraw(amount)
            user.checking_account.deposit(amount)
            self.savings_account.transaction_history.add_transaction(Transaction(amount, "transfer", user.checking_account.accountNumber))
            user.checking_account.transaction_history.add_transaction(Transaction(amount, "deposit", user.checking_account.accountNumber))
        else:
            print("Insufficient funds for transfer.\n")


if __name__ == "__main__":

    user1 = User("user1")
    user2 = User("user2")

    user1.create_checking_account(123, "user1", 1000)
    user1.create_savings_account(456, "user1", 500)

    user2.create_checking_account(789, "user2", 2000)
    user2.create_savings_account(101, "user2", 1000)

    user1.deposit_to_checking(100)
    user1.deposit_to_savings(50)

    user1.withdraw_from_checking(200)
    user1.withdraw_from_savings(100)


    user2.transfer_to_user_savings(50, user1)
    user2.transfer_to_user_checking(50, user1)

    print(f"User1 Checking Balance: {user1.checking_account.balance}")
    print(f"User1 Savings Balance: {user1.savings_account.balance}")

    print(f"User2 Checking Balance: {user2.checking_account.balance}")
    print(f"User2 Savings Balance: {user2.savings_account.balance}")

