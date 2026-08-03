import java.util.ArrayList;
import java.util.Scanner;

class BankAccount {
    int accountNumber;
    String holderName;
    double balance;

    BankAccount(int accountNumber, String holderName, double balance) {
        this.accountNumber = accountNumber;
        this.holderName = holderName;
        this.balance = balance;
    }

    void deposit(double amount) {
        balance += amount;
        System.out.println("Amount deposited successfully.");
    }

    void withdraw(double amount) {
        if (amount > balance) {
            System.out.println("Insufficient balance.");
        } else {
            balance -= amount;
            System.out.println("Withdrawal successful.");
        }
    }

    void display() {
        System.out.println("----------------------------------");
        System.out.println("Account Number : " + accountNumber);
        System.out.println("Holder Name    : " + holderName);
        System.out.println("Balance        : $" + balance);
    }
}

public class BankManagementSystem {

    static ArrayList<BankAccount> accounts = new ArrayList<>();
    static Scanner scanner = new Scanner(System.in);

    static BankAccount findAccount(int accountNumber) {
        for (BankAccount account : accounts) {
            if (account.accountNumber == accountNumber) {
                return account;
            }
        }
        return null;
    }

    static void createAccount() {
        System.out.print("Enter Account Number: ");
        int number = scanner.nextInt();
        scanner.nextLine();

        if (findAccount(number) != null) {
            System.out.println("Account already exists.");
            return;
        }

        System.out.print("Enter Holder Name: ");
        String name = scanner.nextLine();

        System.out.print("Enter Initial Balance: ");
        double balance = scanner.nextDouble();

        accounts.add(new BankAccount(number, name, balance));

        System.out.println("Account created successfully.");
    }

    static void depositMoney() {
        System.out.print("Enter Account Number: ");
        int number = scanner.nextInt();

        BankAccount account = findAccount(number);

        if (account == null) {
            System.out.println("Account not found.");
            return;
        }

        System.out.print("Enter Amount: ");
        double amount = scanner.nextDouble();

        account.deposit(amount);
    }

    static void withdrawMoney() {
        System.out.print("Enter Account Number: ");
        int number = scanner.nextInt();

        BankAccount account = findAccount(number);

        if (account == null) {
            System.out.println("Account not found.");
            return;
        }

        System.out.print("Enter Amount: ");
        double amount = scanner.nextDouble();

        account.withdraw(amount);
    }

    static void searchAccount() {
        System.out.print("Enter Account Number: ");
        int number = scanner.nextInt();

        BankAccount account = findAccount(number);

        if (account == null) {
            System.out.println("Account not found.");
        } else {
            account.display();
        }
    }

    static void displayAllAccounts() {

        if (accounts.isEmpty()) {
            System.out.println("No accounts available.");
            return;
        }

        System.out.println("\n===== ALL ACCOUNTS =====");

        for (BankAccount account : accounts) {
            account.display();
        }
    }

    static void deleteAccount() {

        System.out.print("Enter Account Number: ");
        int number = scanner.nextInt();

        BankAccount account = findAccount(number);

        if (account == null) {
            System.out.println("Account not found.");
            return;
        }

        accounts.remove(account);

        System.out.println("Account deleted successfully.");
    }

    static void showStatistics() {

        System.out.println("\n===== BANK STATISTICS =====");

        System.out.println("Total Accounts: " + accounts.size());

        double totalBalance = 0;

        for (BankAccount account : accounts) {
            totalBalance += account.balance;
        }

        System.out.println("Total Balance : $" + totalBalance);

        if (!accounts.isEmpty()) {
            System.out.println("Average Balance: $" +
                    (totalBalance / accounts.size()));
        }
    }

    public static void main(String[] args) {

        int choice;

        while (true) {

            System.out.println("\n==============================");
            System.out.println(" BANK MANAGEMENT SYSTEM");
            System.out.println("==============================");
            System.out.println("1. Create Account");
            System.out.println("2. Deposit Money");
            System.out.println("3. Withdraw Money");
            System.out.println("4. Search Account");
            System.out.println("5. Display All Accounts");
            System.out.println("6. Delete Account");
            System.out.println("7. Bank Statistics");
            System.out.println("8. Exit");

            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {

                case 1:
                    createAccount();
                    break;

                case 2:
                    depositMoney();
                    break;

                case 3:
                    withdrawMoney();
                    break;

                case 4:
                    searchAccount();
                    break;

                case 5:
                    displayAllAccounts();
                    break;

                case 6:
                    deleteAccount();
                    break;

                case 7:
                    showStatistics();
                    break;

                case 8:
                    System.out.println("Thank you for using the Bank Management System.");
                    System.exit(0);

                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }
}
