class BankAccount:
    def __init__(self, accountNumber, accountHolderName, balance=0.0):
        self.accountNumber = accountNumber
        self.accountHolderName = accountHolderName
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount.")

class SavingsAccount(BankAccount):
    def __init__(self, accountNumber, accountHolderName, balance=0.0, minBalance=100.0):
        super().__init__(accountNumber, accountHolderName, balance)
        self.minBalance = minBalance

class CheckingAccount(BankAccount):
    def __init__(self, accountNumber, accountHolderName, balance=0.0):
        super().__init__(accountNumber, accountHolderName, balance)