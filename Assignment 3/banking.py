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

    def __str__(self):
        return ", ".join([str(transaction) for transaction in self.transactions])
    
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
    
    def create_loan_account(self, accountNumber, accountHolderName, loan_amount, interest_rate, loan_duration):
        self.loan_account = LoanAccount(accountNumber, accountHolderName, loan_amount, interest_rate, loan_duration)
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
    def __init__(self, accountNumber, accountHolderName, loan_amount, interest_rate, loan_duration):
        super().__init__(accountNumber, accountHolderName)
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.loan_duration = loan_duration
        self.monthly_payment = (loan_amount * interest_rate * (1 + interest_rate) ** loan_duration) / ((1 + interest_rate) ** loan_duration - 1)
    
    def make_monthly_payment_checking(self, user:User):
        user.withdraw_from_checking(self.monthly_payment)
        self.balance -= self.monthly_payment
        print(f"Account: #{user.checking_account.accountNumber} Made a monthly payment of ${self.monthly_payment}. Remaining balance: ${user.checking_account.balance}\n")
        self.transaction_history.add_transaction(Transaction(self.monthly_payment, "payment", user.checking_account.accountNumber))
        print(f"Remaining Balance: {self.calculate_remaining_balance()}\n")
    
    def make_monthly_payment_savings(self, user:User):
        user.withdraw_from_savings(self.monthly_payment)
        self.balance -= self.monthly_payment
        print(f"Account: #{user.savings_account.accountNumber} Made a monthly payment of ${self.monthly_payment}. Remaining balance: ${user.savings_account.balance}\n")
        self.transaction_history.add_transaction(Transaction(self.monthly_payment, "payment", user.savings_account.accountNumber))
        print(f"Remaining Balance: {self.calculate_remaining_balance()}\n")

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

    def make_payment_savings(self, amount, user: User):
        user.withdraw_from_savings(amount)
        self.balance -= amount
        print(f"Account: #{user.savings_account.accountNumber} Made a payment of ${amount}. Remaining balance: ${user.savings_account.balance}\n")
        self.transaction_history.add_transaction(Transaction(amount, "payment", user.savings_account.accountNumber))
        print(f"Remaining Credit: {self.calculate_remaining_credit()}\n")
    
    def make_payment_checking(self, amount, user: User):
        user.withdraw_from_checking(amount)
        self.balance -= amount
        print(f"Account: #{user.checking_account.accountNumber} Made a payment of ${amount}. Remaining balance: ${user.checking_account.balance}\n")
        self.transaction_history.add_transaction(Transaction(amount, "payment", user.checking_account.accountNumber))
        print(f"Remaining Credit: {self.calculate_remaining_credit()}\n")
    
    def handleReturn(self, amount):
        self.balance -= amount
        print(f"Account: #{self.accountNumber} Returned an item for ${amount}. Remaining credit: ${self.credit_limit - self.balance}\n")
        self.transaction_history.add_transaction(Transaction(amount, "return", self.accountNumber))
        print(f"Remaining Credit: {self.calculate_remaining_credit()}\n")

    def calculate_remaining_credit(self):
        return self.credit_limit - self.balance


class Store:
    def __init__(self, storeName:str, storeOwner: User):
        self.storeName = storeName
        self.storeOwner = storeOwner
    
    def sellItem(self, item:str, price:float, buyer: User):
        print(f"Store: {self.storeName} selling item: {item} for ${price} to User: {buyer.username}.\n")
        if buyer.credit_card_account.calculate_remaining_credit() >= price:
            buyer.credit_card_account.make_purchase(price)
            self.storeOwner.checking_account.deposit(price)
        else:
            print("Insufficient funds for purchase.\n")
    
    def refundItem(self, item:str, price:float, buyer: User):
        print(f"Store: {self.storeName} refunding item: {item} for ${price} to User: {buyer.username}.\n")
        if buyer.credit_card_account.balance >= price:
            buyer.credit_card_account.handleReturn(price)
            self.storeOwner.credit_card_account.make_purchase(price)
        else:
            print("Insufficient funds for refund.\n")
    
if __name__ == "__main__":
    # Create two users
    user1 = User("Alice")
    user2 = User("Bob")

    # Create checking and savings accounts for both users
    user1.create_checking_account(123, "Alice", 5000)
    user1.create_savings_account(456, "Alice", 10000)
    user2.create_checking_account(789, "Bob", 3000)
    user2.create_savings_account(101112, "Bob", 8000)

    # Create a loan account for user1
    user1.create_loan_account(131415, "Alice", 20000, 0.05, 5,)

    # Create a credit card account for user1 and user2
    user1.create_credit_card_account(141516, "Alice", 10000, 0.15, 0)
    user2.create_credit_card_account(161718, "Bob", 5000, 0.18, 0)

    # User1 deposits to checking account
    user1.deposit_to_checking(1000)

    # User2 withdraws from savings account
    user2.withdraw_from_savings(500)

    # User1 transfers to user2's savings account
    user1.transfer_to_user_savings(500, user2)

    # User2 transfers to user1's checking account
    user2.transfer_to_user_checking(300, user1)

    # User1 makes a monthly payment to loan account from checking account
    user1.loan_account.make_monthly_payment_checking(user1)

    # User2 makes a purchase using credit card account
    user2.credit_card_account.make_purchase(200)

    # User2 makes a payment to credit card account from checking account
    user2.credit_card_account.make_payment_checking(200, user2)

    # Create a store owned by user1
    store = Store("Alice's Store", user1)

    # User2 buys an item from the store
    store.sellItem("Item1", 100, user2)

    # The store refunds the item to user2
    store.refundItem("Item1", 100, user2)

