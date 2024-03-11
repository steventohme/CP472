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


class LoanAccount(BankAccount):
    def __init__(self, accountNumber, accountHolderName, loan_amount, interest_rate, loan_duration, balance=0.0):
        super().__init__(accountNumber, accountHolderName, balance)
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.loan_duration = loan_duration
        self.monthly_payment = (loan_amount * interest_rate * (1 + interest_rate) ** loan_duration) / ((1 + interest_rate) ** loan_duration - 1)

    def make_payment(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Made a payment of ${amount}. Remaining balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "payment", self.accountNumber))
        else:
            print("Invalid payment amount or insufficient funds.\n")

    def calculate_remaining_balance(self):
        return self.loan_amount - self.balance


class CreditCardAccount(BankAccount):
    def __init__(self, accountNumber, accountHolderName, credit_limit, interest_rate, balance=0.0):
        super().__init__(accountNumber, accountHolderName, balance)
        self.credit_limit = credit_limit
        self.interest_rate = interest_rate

    def make_purchase(self, amount):
        if amount > 0 and (self.balance + amount) <= self.credit_limit:
            self.balance += amount
            print(f"Account: #{self.accountNumber} Made a purchase of ${amount}. Remaining credit: ${self.credit_limit - self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "purchase", self.accountNumber))
        else:
            print("Invalid purchase amount or would exceed credit limit.\n")

    def make_payment(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Made a payment of ${amount}. Remaining balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "payment", self.accountNumber))
        else:
            print("Invalid payment amount or insufficient funds.\n")

    def calculate_remaining_credit(self):
        return self.credit_limit - self.balance


class User:
    def __init__(self, username, checking_account=None, savings_account=None, loan_account=None, credit_card_account=None):
        self.username = username
        self.checking_account = checking_account
        self.savings_account = savings_account
        self.loan_account = loan_account
        self.credit_card_account = credit_card_account
    
    def create_checking_account(self, accountNumber, accountHolderName, balance):
        self.checking_account = CheckingAccount(accountNumber, accountHolderName, balance)
        print(f"User: {self.username} created checking account: #{accountNumber} with balance: ${balance}.\n")
    
    def create_savings_account(self, accountNumber, accountHolderName, balance):
        self.savings_account = SavingsAccount(accountNumber, accountHolderName, balance)
        print(f"User: {self.username} created savings account: #{accountNumber} with balance: ${balance}.\n")
    
    def create_loan_account(self, accountNumber, accountHolderName, loan_amount, interest_rate, loan_duration, balance):
        self.loan_account = LoanAccount(accountNumber, accountHolderName, loan_amount, interest_rate, loan_duration, balance)
        print(f"User: {self.username} created loan account: #{accountNumber} with loan amount: ${loan_amount}.\n")
    
    def create_credit_card_account(self, accountNumber, accountHolderName, credit_limit, interest_rate, balance):
        self.credit_card_account = CreditCardAccount(accountNumber, accountHolderName, credit_limit, interest_rate, balance)
        print(f"User: {self.username} created credit card account: #{accountNumber} with credit limit: ${credit_limit}.\n")
    
    def deposit_to_checking(self, amount):
        self.checking_account.deposit(amount)
    
    def deposit_to_savings(self, amount):
        self.savings_account.deposit(amount)
    
    def withdraw_from_checking(self, amount):
        self.checking_account.withdraw(amount)
    
    def withdraw_from_savings(self, amount):
        self.savings_account.withdraw(amount)
    
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

    print(f"User1 Checking Transactions: {user1.checking_account.transaction_history.transactions}")
    print(f"User1 Savings Transactions: {user1.savings_account.transaction_history.transactions}")


    user1.create_loan_account(789, "user1", 10000, 0.05, 12, 0)
    user1.loan_account.make_payment(1000)
    print(f"Remaining Loan Balance: {user1.loan_account.calculate_remaining_balance()}")

    user1.create_credit_card_account(101, "user1", 5000, 0.1, 0)
    user1.credit_card_account.make_purchase(1000)
    user1.credit_card_account.make_payment(500)

    print(f"Remaining Credit: {user1.credit_card_account.calculate_remaining_credit()}")

