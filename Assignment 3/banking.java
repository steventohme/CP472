

public class banking {
    
}


class BankAccount {
    protected String accountNumber;
    protected String accountHolderName;
    protected double balance;

    public BankAccount(String accountNumber, String accountHolderName, double balance) {
        this.accountNumber = accountNumber;
        this.accountHolderName = accountHolderName;
        this.balance = balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.println("Deposited $" + amount + ". New balance: $" + this.balance);
        } else {
            System.out.println("Invalid deposit amount.");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= this.balance) {
            this.balance -= amount;
            System.out.println("Withdrew $" + amount + ". New balance: $" + this.balance);
        } else {
            System.out.println("Invalid withdrawal amount or insufficient funds.");
        }
    }
}

class SavingsAccount extends BankAccount {
    private double minBalance;

    public SavingsAccount(String accountNumber, String accountHolderName, double balance, double minBalance) {
        super(accountNumber, accountHolderName, balance);
        this.minBalance = minBalance;
    }

    @Override
    public void withdraw(double amount) {
        if (amount > 0 && (this.balance - amount) >= this.minBalance) {
            this.balance -= amount;
            System.out.println("Withdrew $" + amount + ". New balance: $" + this.balance);
        } else {
            System.out.println("Invalid withdrawal amount or would violate minimum balance for savings account.");
        }
    }
}

class CheckingAccount extends BankAccount {
    public CheckingAccount(String accountNumber, String accountHolderName, double balance) {
        super(accountNumber, accountHolderName, balance);
    }
}