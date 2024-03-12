import java.util.ArrayList;
import java.util.List;
import java.time.LocalDateTime;

class Transaction {
    private double amount;
    private String transactionType;
    private int accountNumber;
    private LocalDateTime dateTime;

    public Transaction(double amount, String transactionType, int accountNumber) {
        this.amount = amount;
        this.transactionType = transactionType;
        this.accountNumber = accountNumber;
        this.dateTime = LocalDateTime.now();
    }

    public String toString() {
        return dateTime + " - " + transactionType + " of $" + amount + " on account " + accountNumber;
    }
}

class TransactionHistory {
    private List<Transaction> transactions;

    public TransactionHistory() {
        this.transactions = new ArrayList<>();
    }

    public void addTransaction(Transaction transaction) {
        transactions.add(transaction);
    }

    public String toString() {
        List<String> transactionStrings = new ArrayList<>();
        for (Transaction transaction : transactions) {
            transactionStrings.add(transaction.toString());
        }
        return String.join(", ", transactionStrings);
    }
}

class User {
    private String username;
    private CheckingAccount checkingAccount;
    private SavingsAccount savingsAccount;
    private LoanAccount loanAccount;
    private CreditCardAccount creditCardAccount;

    public User(String username) {
        this.username = username;
    }

    public void createCheckingAccount(int accountNumber, String accountHolderName, double balance) {
        checkingAccount = new CheckingAccount(accountNumber, accountHolderName, balance);
        System.out.println("User: " + username + " created checking account: " + checkingAccount);
    }

    public void createSavingsAccount(int accountNumber, String accountHolderName, double balance, double minBalance) {
        savingsAccount = new SavingsAccount(accountNumber, accountHolderName, balance, minBalance);
        System.out.println("User: " + username + " created savings account: " + savingsAccount);
    }

    public void createLoanAccount(int accountNumber, String accountHolderName, double loanAmount, double interestRate, int loanDuration) {
        loanAccount = new LoanAccount(accountNumber, accountHolderName, loanAmount, interestRate, loanDuration);
        System.out.println("User: " + username + " created loan account: " + loanAccount);
    }

    public void createCreditCardAccount(int accountNumber, String accountHolderName, double creditLimit, double interestRate, double balance) {
        creditCardAccount = new CreditCardAccount(accountNumber, accountHolderName, creditLimit, interestRate, balance);
        System.out.println("User: " + username + " created credit card account: " + creditCardAccount);
    }

    public void depositToChecking(double amount) {
        checkingAccount.deposit(amount);
    }

    public void depositToSavings(double amount) {
        savingsAccount.deposit(amount);
    }

    public void withdrawFromChecking(double amount) {
        checkingAccount.withdraw(amount);
    }

    public void withdrawFromSavings(double amount) {
        savingsAccount.withdraw(amount);
    }

    public void transferToUserSavings(double amount, User user) {
        System.out.println("User: " + username + " transferring $" + amount + " to User: " + user.getUsername() + "'s savings account.\n");
        if (checkingAccount.getBalance() >= amount) {
            checkingAccount.withdraw(amount);
            user.getSavingsAccount().deposit(amount);
            checkingAccount.getTransactionHistory().addTransaction(new Transaction(amount, "transfer", user.getSavingsAccount().getAccountNumber()));
            user.getSavingsAccount().getTransactionHistory().addTransaction(new Transaction(amount, "deposit", user.getSavingsAccount().getAccountNumber()));
        } else {
            System.out.println("Insufficient funds for transfer.\n");
        }
    }

    public void transferToUserChecking(double amount, User user) {
        System.out.println("User: " + username + " transferring $" + amount + " to User: " + user.getUsername() + "'s checking account.\n");
        if (savingsAccount.getBalance() >= amount) {
            savingsAccount.withdraw(amount);
            user.getCheckingAccount().deposit(amount);
            savingsAccount.getTransactionHistory().addTransaction(new Transaction(amount, "transfer", user.getCheckingAccount().getAccountNumber()));
            user.getCheckingAccount().getTransactionHistory().addTransaction(new Transaction(amount, "deposit", user.getCheckingAccount().getAccountNumber()));
        } else {
            System.out.println("Insufficient funds for transfer.\n");
        }
    }

    public String getUsername() {
        return username;
    }

    public CheckingAccount getCheckingAccount() {
        return checkingAccount;
    }

    public SavingsAccount getSavingsAccount() {
        return savingsAccount;
    }

    public LoanAccount getLoanAccount() {
        return loanAccount;
    }

    public CreditCardAccount getCreditCardAccount() {
        return creditCardAccount;
    }
}

class BankAccount {
    private int accountNumber;
    private String accountHolderName;
    private double balance;
    protected TransactionHistory transactionHistory;

    public BankAccount(int accountNumber, String accountHolderName, double balance) {
        this.accountNumber = accountNumber;
        this.accountHolderName = accountHolderName;
        this.balance = balance;
        this.transactionHistory = new TransactionHistory();
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Account: " + accountNumber + " - Deposit of $" + amount);
            transactionHistory.addTransaction(new Transaction(amount, "deposit", accountNumber));
        } else {
            System.out.println("Invalid deposit amount.\n");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Account: " + accountNumber + " - Withdrawal of $" + amount);
            transactionHistory.addTransaction(new Transaction(amount, "withdrawal", accountNumber));
        } else {
            System.out.println("Invalid withdrawal amount or insufficient funds.\n");
        }
    }

    public int getAccountNumber() {
        return accountNumber;
    }

    public String getAccountHolderName() {
        return accountHolderName;
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public TransactionHistory getTransactionHistory() {
        return transactionHistory;
    }

    public String toString() {
        return accountNumber + " - " + accountHolderName;
    }
}

class SavingsAccount extends BankAccount {
    private double minBalance;

    public SavingsAccount(int accountNumber, String accountHolderName, double balance, double minBalance) {
        super(accountNumber, accountHolderName, balance);
        this.minBalance = minBalance;
    }

    public void withdraw(double amount) {
        if (amount > 0 && (getBalance() - amount) >= minBalance) {
            super.withdraw(amount);
        } else {
            System.out.println("Invalid withdrawal amount or would violate minimum balance for savings account.\n");
        }
    }
}

class CheckingAccount extends BankAccount {
    public CheckingAccount(int accountNumber, String accountHolderName, double balance) {
        super(accountNumber, accountHolderName, balance);
    }
}

class LoanAccount extends BankAccount {
    private double loanAmount;
    private double interestRate;
    private int loanDuration;
    private double monthlyPayment;

    public LoanAccount(int accountNumber, String accountHolderName, double loanAmount, double interestRate, int loanDuration) {
        super(accountNumber, accountHolderName, 0);
        this.loanAmount = loanAmount;
        this.interestRate = interestRate;
        this.loanDuration = loanDuration;
        this.monthlyPayment = (loanAmount * interestRate * Math.pow(1 + interestRate, loanDuration)) / (Math.pow(1 + interestRate, loanDuration) - 1);
    }

    public void makeMonthlyPaymentChecking(User user) {
        user.withdrawFromChecking(monthlyPayment);
        setBalance(getBalance() - monthlyPayment);
        System.out.println("Account: " + getAccountNumber() + " - Payment of $" + monthlyPayment);
        transactionHistory.addTransaction(new Transaction(monthlyPayment, "payment", user.getCheckingAccount().getAccountNumber()));
        System.out.println("Remaining Balance: " + calculateRemainingBalance() + "\n");
    }


    public void makeMonthlyPaymentSavings(User user) {
        user.withdrawFromSavings(monthlyPayment);
        setBalance(getBalance() - monthlyPayment);
        System.out.println("Account: " + getAccountNumber() + " - Payment of $" + monthlyPayment);
        transactionHistory.addTransaction(new Transaction(monthlyPayment, "payment", user.getSavingsAccount().getAccountNumber()));
        System.out.println("Remaining Balance: " + calculateRemainingBalance() + "\n");
    }

    public double calculateRemainingBalance() {
        return loanAmount - getBalance();
    }
}

class CreditCardAccount extends BankAccount {
    private double creditLimit;
    private double interestRate;

    public CreditCardAccount(int accountNumber, String accountHolderName, double creditLimit, double interestRate, double balance) {
        super(accountNumber, accountHolderName, balance);
        this.creditLimit = creditLimit;
        this.interestRate = interestRate;
    }

    public void makePurchase(double amount) {
        if (amount > 0 && (getBalance() + amount) <= creditLimit) {
            super.deposit(amount);
            System.out.println("Account: " + getAccountNumber() + " - Purchase of $" + amount);
            transactionHistory.addTransaction(new Transaction(amount, "purchase", getAccountNumber()));
        } else {
            System.out.println("Invalid purchase amount or would exceed credit limit.\n");
        }
    }

    public void makePaymentSavings(double amount, User user) {
        user.withdrawFromSavings(amount);
        setBalance(getBalance() - amount);
        System.out.println("Account: " + getAccountNumber() + " - Payment of $" + amount);
        transactionHistory.addTransaction(new Transaction(amount, "payment", user.getSavingsAccount().getAccountNumber()));
        System.out.println("Remaining Credit: " + calculateRemainingCredit() + "\n");
    }

    public void makePaymentChecking(double amount, User user) {
        user.withdrawFromChecking(amount);
        setBalance(getBalance() - amount);
        System.out.println("Account: " + getAccountNumber() + " - Payment of $" + amount);
        transactionHistory.addTransaction(new Transaction(amount, "payment", user.getCheckingAccount().getAccountNumber()));
        System.out.println("Remaining Credit: " + calculateRemainingCredit() + "\n");
    }

    public void handleReturn(double amount) {
        super.withdraw(amount);
        System.out.println("Account: " + getAccountNumber() + " - Return of $" + amount);
        transactionHistory.addTransaction(new Transaction(amount, "return", getAccountNumber()));
    }

    public double calculateRemainingCredit() {
        return creditLimit - getBalance();
    }
}

class Store {
    private String storeName;
    private User storeOwner;

    public Store(String storeName, User storeOwner) {
        this.storeName = storeName;
        this.storeOwner = storeOwner;
    }

    public void sellItem(String item, double price, User buyer) {
        System.out.println("Store: " + storeName + " selling item: " + item + " for $" + price + " to User: " + buyer.getUsername() + ".\n");
        if (buyer.getCreditCardAccount().getBalance() >= price) {
            buyer.getCreditCardAccount().makePurchase(price);
            storeOwner.getCheckingAccount().deposit(price);;
        } else {
            System.out.println("Insufficient funds for purchase.\n");
        }
    }

    public void refundItem(String item, double price, User buyer) {
        System.out.println("Store: " + storeName + " refunding item: " + item + " for $" + price + " to User: " + buyer.getUsername() + ".\n");
        if (buyer.getCreditCardAccount().getBalance() >= price) {
            buyer.getCreditCardAccount().handleReturn(price);
            storeOwner.getCreditCardAccount().makePurchase(price);
        } else {
            System.out.println("Insufficient funds for refund.\n");
        }
    }
}

public class banking {
    public static void main(String[] args) {
        User user1 = new User("Alice");
        User user2 = new User("Bob");

        user1.createCheckingAccount(123, "Alice", 5000);
        user1.createSavingsAccount(456, "Alice", 10000, 100);
        user2.createCheckingAccount(789, "Bob", 3000);
        user2.createSavingsAccount(101112, "Bob", 8000, 100);

        user1.createLoanAccount(131415, "Alice", 20000, 0.05, 5);

        user2.createCreditCardAccount(161718, "Bob", 5000, 0.18, 0);

        user1.depositToChecking(1000);

        user2.withdrawFromSavings(500);

        user1.transferToUserSavings(500, user2);

        user2.transferToUserChecking(300, user1);

        user1.getLoanAccount().makeMonthlyPaymentChecking(user1);

        user2.getCreditCardAccount().makePurchase(200);

        user2.getCreditCardAccount().makePaymentChecking(200, user2);

        Store store = new Store("Alice's Store", user1);

        store.sellItem("Item1", 100, user2);

        store.refundItem("Item1", 100, user2);
    }
}


