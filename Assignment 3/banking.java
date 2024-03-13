import java.util.ArrayList;
import java.util.Date;
import java.util.List;

class Transaction {
    private double amount;
    private String transactionType;
    private String accountNumber;
    private Date dateTime;

    public Transaction(double amount, String transactionType, String accountNumber) {
        this.amount = amount;
        this.transactionType = transactionType;
        this.accountNumber = accountNumber;
        this.dateTime = new Date();
    }

    public String toString() {
        return dateTime + " - " + transactionType + " of $" + amount + " on account " + accountNumber;
    }

    public double getAmount() {
        return amount;
    }

    public String getTransactionType() {
        return transactionType;
    }

    public String getAccountNumber() {
        return accountNumber;
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

    public List<Transaction> getTransactions() {
        return transactions;
    }
}

class User {
    private String username;
    private CheckingAccount checkingAccount;
    private SavingsAccount savingsAccount;
    private LoanAccount loanAccount;
    private CreditCardAccount creditCardAccount;

    public User(String username, CheckingAccount checkingAccount, SavingsAccount savingsAccount,
            LoanAccount loanAccount, CreditCardAccount creditCardAccount) {
        this.username = username;
        this.checkingAccount = checkingAccount;
        this.savingsAccount = savingsAccount;
        this.loanAccount = loanAccount;
        this.creditCardAccount = creditCardAccount;
    }

    public void createCheckingAccount(String accountNumber, double balance, double insufficientFundsFee) {
        this.checkingAccount = new CheckingAccount(this, accountNumber, balance, insufficientFundsFee);
        System.out.println("User: " + this.username + " created checking account: " + accountNumber);
    }

    public void createSavingsAccount(String accountNumber, double balance, double minBalance) {
        this.savingsAccount = new SavingsAccount(this, accountNumber, balance, minBalance);
        System.out.println("User: " + this.username + " created savings account: " + accountNumber);
    }

    public void createLoanAccount(String accountNumber, double loanAmount, double interestRate, int loanDuration) {
        this.loanAccount = new LoanAccount(this, accountNumber, loanAmount, interestRate, loanDuration);
        System.out.println("User: " + this.username + " created loan account: " + accountNumber);
    }

    public void createCreditCardAccount(String accountNumber, double creditLimit, double interestRate, double balance) {
        this.creditCardAccount = new CreditCardAccount(this, accountNumber, creditLimit, interestRate, balance);
        System.out.println("User: " + this.username + " created credit card account: " + accountNumber);
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
        System.out.println("User: " + this.username + " transferring $" + amount + " to User: " + user.getUsername()
                + "'s savings account.\n");
        if (this.checkingAccount.getBalance() >= amount) {
            this.checkingAccount.withdraw(amount);
            user.getSavingsAccount().deposit(amount);
            this.checkingAccount.getTransactionHistory()
                    .addTransaction(new Transaction(amount, "transfer", user.getSavingsAccount().getAccountNumber()));
            user.getSavingsAccount().getTransactionHistory()
                    .addTransaction(new Transaction(amount, "deposit", user.getSavingsAccount().getAccountNumber()));
        } else {
            System.out.println("Insufficient funds for transfer.\n");
        }
    }

    public void transferToUserChecking(double amount, User user) {
        System.out.println("User: " + this.username + " transferring $" + amount + " to User: " + user.getUsername()
                + "'s checking account.\n");
        if (this.savingsAccount.getBalance() >= amount) {
            this.savingsAccount.withdraw(amount);
            user.getCheckingAccount().deposit(amount);
            this.savingsAccount.getTransactionHistory()
                    .addTransaction(new Transaction(amount, "transfer", user.getCheckingAccount().getAccountNumber()));
            user.getCheckingAccount().getTransactionHistory()
                    .addTransaction(new Transaction(amount, "deposit", user.getCheckingAccount().getAccountNumber()));
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
    private User user;
    protected String accountNumber;
    protected double balance;
    protected TransactionHistory transactionHistory;

    public BankAccount(User user, String accountNumber, double balance) {
        this.user = user;
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.transactionHistory = new TransactionHistory();
    }

    public void deposit(double amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.println("Account: " + this.accountNumber + " - Deposited $" + amount);
            this.transactionHistory.addTransaction(new Transaction(amount, "deposit", this.accountNumber));
        } else {
            System.out.println("Invalid deposit amount.\n");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= this.balance) {
            this.balance -= amount;
            System.out.println("Account: " + this.accountNumber + " - Withdrew $" + amount);
            this.transactionHistory.addTransaction(new Transaction(amount, "withdrawal", this.accountNumber));
        } else {
            System.out.println("Invalid withdrawal amount or insufficient funds.\n");
        }
    }

    public double getBalance() {
        return balance;
    }

    public TransactionHistory getTransactionHistory() {
        return transactionHistory;
    }

    public User getUser() {
        return user;
    }

    public String getAccountNumber() {
        return accountNumber;
    }
}

class SavingsAccount extends BankAccount {
    private double minBalance;

    public SavingsAccount(User user, String accountNumber, double balance, double minBalance) {
        super(user, accountNumber, balance);
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
    private double insufficientFundsFee;

    public CheckingAccount(User user, String accountNumber, double balance, double insufficientFundsFee) {
        super(user, accountNumber, balance);
        this.insufficientFundsFee = insufficientFundsFee;
    }

    public void withdraw(double amount) {
        if (amount > 0 && (getBalance() - amount) >= 0) {
            super.withdraw(amount);
        } else {
            System.out.println("Invalid withdrawal amount or insufficient funds.\n");
            this.balance -= this.insufficientFundsFee;
            System.out.println("Account: " + this.accountNumber + " - Charged insufficient funds fee: $"
                    + this.insufficientFundsFee);
        }
    }
}

class LoanAccount extends BankAccount {
    private double loanAmount;
    private double interestRate;
    private int loanDuration;
    private double monthlyPayment;

    public LoanAccount(User user, String accountNumber, double loanAmount, double interestRate, int loanDuration) {
        super(user, accountNumber, 0);
        this.loanAmount = loanAmount;
        this.interestRate = interestRate;
        this.loanDuration = loanDuration;
        this.monthlyPayment = (loanAmount * interestRate * Math.pow(1 + interestRate, loanDuration))
                / (Math.pow(1 + interestRate, loanDuration) - 1);
    }

    public void makeMonthlyPaymentChecking(User user) {
        user.withdrawFromChecking(this.monthlyPayment);
        this.balance -= this.monthlyPayment;
        System.out.println("Account: " + this.accountNumber + " - Made monthly payment: $" + this.monthlyPayment);
        this.transactionHistory.addTransaction(
                new Transaction(this.monthlyPayment, "payment", user.getCheckingAccount().getAccountNumber()));
        System.out.println("Remaining Balance: " + calculateRemainingBalance() + "\n");
    }

    public void makeMonthlyPaymentSavings(User user) {
        user.withdrawFromSavings(this.monthlyPayment);
        this.balance -= this.monthlyPayment;
        System.out.println("Account: " + this.accountNumber + " - Made monthly payment: $" + this.monthlyPayment);
        this.transactionHistory.addTransaction(
                new Transaction(this.monthlyPayment, "payment", user.getSavingsAccount().getAccountNumber()));
        System.out.println("Remaining Balance: " + calculateRemainingBalance() + "\n");
    }

    public double calculateRemainingBalance() {
        return this.loanAmount - this.balance;
    }
}

class CreditCardAccount extends BankAccount {
    private double creditLimit;
    private double interestRate;

    public CreditCardAccount(User user, String accountNumber, double creditLimit, double interestRate, double balance) {
        super(user, accountNumber, balance);
        this.creditLimit = creditLimit;
        this.interestRate = interestRate;
    }

    public void makePurchase(double amount) {
        if (amount > 0 && (getBalance() + amount) <= creditLimit) {
            super.deposit(amount);
            System.out.println("Account: " + this.accountNumber + " - Made purchase: $" + amount);
            this.transactionHistory.addTransaction(new Transaction(amount, "purchase", this.accountNumber));
        } else {
            System.out.println("Invalid purchase amount or would exceed credit limit.\n");
        }
    }

    public void makePaymentSavings(double amount) {
        getUser().withdrawFromSavings(amount);
        this.balance -= amount;
        System.out.println("Account: " + this.accountNumber + " - Made payment: $" + amount);
        this.transactionHistory
                .addTransaction(new Transaction(amount, "payment", getUser().getSavingsAccount().getAccountNumber()));
        System.out.println("Remaining Credit: " + calculateRemainingCredit() + "\n");
    }

    public void makePaymentChecking(double amount) {
        getUser().withdrawFromChecking(amount);
        this.balance -= amount;
        System.out.println("Account: " + this.accountNumber + " - Made payment: $" + amount);
        this.transactionHistory
                .addTransaction(new Transaction(amount, "payment", getUser().getCheckingAccount().getAccountNumber()));
        System.out.println("Remaining Credit: " + calculateRemainingCredit() + "\n");
    }

    public void handleReturn(double amount) {
        this.balance -= amount;
        System.out.println("Account: " + this.accountNumber + " - Handled return: $" + amount);
        this.transactionHistory.addTransaction(new Transaction(amount, "return", this.accountNumber));
        System.out.println("Remaining Credit: " + calculateRemainingCredit() + "\n");
    }

    public double calculateRemainingCredit() {
        return this.creditLimit - this.balance;
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
        System.out.println("Store: " + this.storeName + " selling item: " + item + " for $" + price + " to User: "
                + buyer.getUsername() + ".\n");
        if (buyer.getCreditCardAccount().calculateRemainingCredit() >= price) {
            buyer.getCreditCardAccount().makePurchase(price);
            this.storeOwner.getCheckingAccount().deposit(price);
        } else {
            System.out.println("Insufficient funds for purchase.\n");
        }
    }

    public void refundItem(String item, double price, User buyer) {
        System.out.println("Store: " + this.storeName + " refunding item: " + item + " for $" + price + " to User: "
                + buyer.getUsername() + ".\n");
        if (buyer.getCreditCardAccount().getBalance() >= price) {
            buyer.getCreditCardAccount().handleReturn(price);
            this.storeOwner.getCreditCardAccount().makePurchase(price);
        } else {
            System.out.println("Insufficient funds for refund.\n");
        }
    }
}

public class banking {
    private User user1;
    private User user2;

    public void setUp() {
        user1 = new User("User1", null, null, null, null);
        user2 = new User("User2", null, null, null, null);
        user1.createCheckingAccount("123", 500, 0.35);
        user1.createSavingsAccount("456", 1000, 200);
        user2.createCheckingAccount("789", 500, 0.35);
        user2.createSavingsAccount("012", 1000, 200);
    }

    public void testTransaction() {
        Transaction transaction = new Transaction(100, "deposit", "123");
        assert transaction.getAmount() == 100;
        assert transaction.getTransactionType().equals("deposit");
        assert transaction.getAccountNumber().equals("123");
    }

    public void testTransactionHistory() {
        TransactionHistory transactionHistory = new TransactionHistory();
        Transaction transaction = new Transaction(100, "deposit", "123");
        transactionHistory.addTransaction(transaction);
        assert transactionHistory.getTransactions().size() == 1;
    }

    public void testCheckingAccount() {
        user1.depositToChecking(100);
        assert user1.getCheckingAccount().getBalance() == 600;
        user1.withdrawFromChecking(50);
        assert user1.getCheckingAccount().getBalance() == 550;
    }

    public void testSavingsAccount() {
        user1.depositToSavings(100);
        assert user1.getSavingsAccount().getBalance() == 1100;
        user1.withdrawFromSavings(50);
        assert user1.getSavingsAccount().getBalance() == 1050;
    }

    public void testTransfer() {
        user1.transferToUserChecking(100, user2);
        assert user1.getCheckingAccount().getBalance() == 500;
        assert user2.getCheckingAccount().getBalance() == 600;
    }

    public void testLoanAccount() {
        user1.createLoanAccount("345", 5000, 0.05, 12);
        user1.getLoanAccount().makeMonthlyPaymentChecking(user1);
        assert user1.getLoanAccount().getBalance() < 5000;
    }

    public void testCreditCardAccount() {
        user1.createCreditCardAccount("678", 2000, 0.18, 0);
        user1.getCreditCardAccount().makePurchase(100);
        assert user1.getCreditCardAccount().getBalance() == 100;
    }

    public void testStore() {
        Store store = new Store("Store1", user1);
        user2.createCreditCardAccount("678", 2000, 0.18, 200);
        store.sellItem("Item1", 50, user2);
        assert user2.getCreditCardAccount().getBalance() == 250;
    }

    public static void main(String[] args) {
        banking testBankingSystem = new banking();
        testBankingSystem.setUp();
        testBankingSystem.testTransaction();
        testBankingSystem.testTransactionHistory();
        testBankingSystem.testCheckingAccount();
        testBankingSystem.testSavingsAccount();
        testBankingSystem.testTransfer();
        testBankingSystem.testLoanAccount();
        testBankingSystem.testCreditCardAccount();
        testBankingSystem.testStore();
    }
}
