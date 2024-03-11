
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
            System.out.println("Account: #" + this.accountNumber + " Deposited $" + amount + ". New balance: $" + this.balance + "\n");
        } else {
            System.out.println("Invalid deposit amount.\n");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= this.balance) {
            this.balance -= amount;
            System.out.println("Account: #" + this.accountNumber + " Withdrew $" + amount + ". New balance: $" + this.balance + "\n");
        } else {
            System.out.println("Invalid withdrawal amount or insufficient funds.\n");
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
            System.out.println("Account: #" + this.accountNumber + " Withdrew $" + amount + ". New balance: $" + this.balance + "\n");
        } else {
            System.out.println("Invalid withdrawal amount or would violate minimum balance for savings account.\n");
        }
    }
}

class CheckingAccount extends BankAccount {
    public CheckingAccount(String accountNumber, String accountHolderName, double balance) {
        super(accountNumber, accountHolderName, balance);
    }
}

class User {
    private String username;
    private CheckingAccount checkingAccount;
    private SavingsAccount savingsAccount;

    public User(String username) {
        this.username = username;
    }

    public void createCheckingAccount(String accountNumber, String accountHolderName, double balance) {
        this.checkingAccount = new CheckingAccount(accountNumber, accountHolderName, balance);
    }

    public void createSavingsAccount(String accountNumber, String accountHolderName, double balance, double minBalance) {
        this.savingsAccount = new SavingsAccount(accountNumber, accountHolderName, balance, minBalance);
    }

    public void depositToChecking(double amount) {
        this.checkingAccount.deposit(amount);
    }

    public void depositToSavings(double amount) {
        this.savingsAccount.deposit(amount);
    }

    public void withdrawFromChecking(double amount) {
        this.checkingAccount.withdraw(amount);
    }

    public void withdrawFromSavings(double amount) {
        this.savingsAccount.withdraw(amount);
    }

    public void transferToUserSavings(double amount, User user) {
        System.out.println("User: " + this.username + " transferring $" + amount + " to User: " + user.username + "'s savings account.\n");
        this.withdrawFromChecking(amount);
        user.depositToSavings(amount);
    }

    public void transferToUserChecking(double amount, User user) {
        System.out.println("User: " + this.username + " transferring $" + amount + " to User: " + user.username + "'s checking account.\n");
        this.withdrawFromSavings(amount);
        user.depositToChecking(amount);
    }

    public CheckingAccount getCheckingAccount() {
        return this.checkingAccount;
    }

    public SavingsAccount getSavingsAccount() {
        return this.savingsAccount;
    }
}

public class banking {
    public static void main(String[] args) {
        User user1 = new User("user1");
        User user2 = new User("user2");

        user1.createCheckingAccount("123", "user1", 1000);
        user1.createSavingsAccount("456", "user1", 500, 100);

        user2.createCheckingAccount("789", "user2", 2000);
        user2.createSavingsAccount("101", "user2", 1000, 100);

        user1.depositToChecking(100);
        user1.depositToSavings(50);

        user1.withdrawFromChecking(200);
        user1.withdrawFromSavings(100);

        user2.transferToUserSavings(50, user1);
        user2.transferToUserChecking(50, user1);

        System.out.println("User1 Checking Balance: " + user1.getCheckingAccount().balance);
        System.out.println("User1 Savings Balance: " + user1.getSavingsAccount().balance);

        System.out.println("User2 Checking Balance: " + user2.getCheckingAccount().balance);
        System.out.println("User2 Savings Balance: " + user2.getSavingsAccount().balance);
    }
}