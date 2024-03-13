from datetime import datetime
import unittest

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
    
    def create_checking_account(self, accountNumber, balance):
        self.checking_account = CheckingAccount(self, accountNumber, balance)
        print(f"User: {self.username} created checking account: #{accountNumber} with balance: ${balance}.\n")
    
    def create_savings_account(self, accountNumber, balance):
        self.savings_account = SavingsAccount(self, accountNumber, balance)
        print(f"User: {self.username} created savings account: #{accountNumber} with balance: ${balance}.\n")
    
    def create_loan_account(self, accountNumber, loan_amount, interest_rate, loan_duration):
        self.loan_account = LoanAccount(self, accountNumber, loan_amount, interest_rate, loan_duration)
        print(f"User: {self.username} created loan account: #{accountNumber} with loan amount: ${loan_amount}.\n")
    
    def create_credit_card_account(self, accountNumber, credit_limit, interest_rate, balance):
        self.credit_card_account = CreditCardAccount(self, accountNumber, credit_limit, interest_rate, balance)
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
    def __init__(self, user: User, accountNumber: int, balance:float=0.0):
        self.user = user
        self.accountNumber = accountNumber
        self.balance = balance
        self.transaction_history = TransactionHistory()

    def deposit(self, amount:float):
        if amount > 0:
            self.balance += amount
            print(f"Account: #{self.accountNumber} Deposited ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "deposit", self.accountNumber))
        else:
            print("Invalid deposit amount.\n")

    def withdraw(self, amount:float):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Withdrew ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "withdrawal", self.accountNumber))
        else:
            print("Invalid withdrawal amount or insufficient funds.\n")


class SavingsAccount(BankAccount):
    def __init__(self, user:User, accountNumber:int, balance:float=0.0, minBalance:float=100.0):
        super().__init__(user, accountNumber, balance)
        self.minBalance = minBalance

    def withdraw(self, amount:float):
        if amount > 0 and (self.balance - amount) >= self.minBalance:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Withdrew ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "withdrawal", self.accountNumber))
        else:
            print("Invalid withdrawal amount or would violate minimum balance for savings account.\n")

class CheckingAccount(BankAccount):
    def __init__(self, user:User, accountNumber:int, balance:float=0.0, insufficient_funds_fee:float=0.35):
        super().__init__(user, accountNumber, balance)
        self.insufficient_funds_fee = insufficient_funds_fee

    def withdraw(self, amount:float):
        if amount > 0 and (self.balance - amount) >= 0:
            self.balance -= amount
            print(f"Account: #{self.accountNumber} Withdrew ${amount}. New balance: ${self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "withdrawal", self.accountNumber))
        else:
            print("Invalid withdrawal amount or insufficient funds.\n")
            self.balance -= self.insufficient_funds_fee
            print(f"Account: #{self.accountNumber} Charged an insufficient funds fee of ${self.insufficient_funds_fee}. New balance: ${self.balance}\n")


class LoanAccount(BankAccount):
    def __init__(self, user:User, accountNumber:int, loan_amount:float, interest_rate:float, loan_duration:int):
        super().__init__(user, accountNumber)
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
    def __init__(self, user: User, accountNumber, credit_limit:float, interest_rate:float, balance=0.0):
        super().__init__(user, accountNumber, balance)
        self.credit_limit = credit_limit
        self.interest_rate = interest_rate

    def make_purchase(self, amount):
        if amount > 0 and (self.balance + amount) <= self.credit_limit:
            self.balance += amount
            print(f"Account: #{self.accountNumber} Made a purchase of ${amount}. Remaining credit: ${self.credit_limit - self.balance}\n")
            self.transaction_history.add_transaction(Transaction(amount, "purchase", self.accountNumber))
        else:
            print("Invalid purchase amount or would exceed credit limit.\n")

    def make_payment_savings(self, amount:float):
        self.user.withdraw_from_savings(amount)
        self.balance -= amount
        print(f"Account: #{self.user.savings_account.accountNumber} Made a payment of ${amount}. Remaining balance: ${self.user.savings_account.balance}\n")
        self.transaction_history.add_transaction(Transaction(amount, "payment", self.user.savings_account.accountNumber))
        print(f"Remaining Credit: {self.calculate_remaining_credit()}\n")
    
    def make_payment_checking(self, amount:float):
        self.user.withdraw_from_checking(amount)
        self.balance -= amount
        print(f"Account: #{self.user.checking_account.accountNumber} Made a payment of ${amount}. Remaining balance: ${self.user.checking_account.balance}\n")
        self.transaction_history.add_transaction(Transaction(amount, "payment", self.user.checking_account.accountNumber))
        print(f"Remaining Credit: {self.calculate_remaining_credit()}\n")
    
    def handleReturn(self, amount:float):
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
    


class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        self.user1 = User("User1")
        self.user2 = User("User2")
        self.user1.create_checking_account("123", 500)
        self.user1.create_savings_account("456", 1000)
        self.user2.create_checking_account("789", 500)
        self.user2.create_savings_account("012", 1000)

    def testTransaction(self):
        # Test Transaction
        transaction = Transaction(100, "deposit", "123")
        self.assertEqual(transaction.amount, 100)
        self.assertEqual(transaction.transaction_type, "deposit")
        self.assertEqual(transaction.account_number, "123")

    def testTransactionHistory(self):
        transaction_history = TransactionHistory()
        transaction = Transaction(100, "deposit", "123")
        transaction_history.add_transaction(transaction)
        self.assertEqual(len(transaction_history.transactions), 1)

    def testCheckingAccount(self):
        self.user1.deposit_to_checking(100)
        self.assertEqual(self.user1.checking_account.balance, 600)
        self.user1.withdraw_from_checking(50)
        self.assertEqual(self.user1.checking_account.balance, 550)

    def testSavingsAccount(self):
        self.user1.deposit_to_savings(100)
        self.assertEqual(self.user1.savings_account.balance, 1100)
        self.user1.withdraw_from_savings(50)
        self.assertEqual(self.user1.savings_account.balance, 1050)

    def testTransfer(self):
        self.user1.transfer_to_user_checking(100, self.user2)
        self.assertEqual(self.user1.checking_account.balance, 500)
        self.assertEqual(self.user2.checking_account.balance, 600)

    def testLoanAccount(self):
        self.user1.create_loan_account("345", 5000, 0.05, 12)
        self.user1.loan_account.make_monthly_payment_checking(self.user1)
        self.assertLess(self.user1.loan_account.balance, 5000)

    def testCreditCardAccount(self):
        self.user1.create_credit_card_account("678", 2000, 0.18, 0)
        self.user1.credit_card_account.make_purchase(100)
        self.assertEqual(self.user1.credit_card_account.balance, 100)

    def testStore(self):
        store = Store("Store1", self.user1)
        self.user2.create_credit_card_account("678", 2000, 0.18, 200)
        store.sellItem("Item1", 50, self.user2)
        self.assertEqual(self.user2.credit_card_account.balance, 250)

if __name__ == "__main__":
    unittest.main()

