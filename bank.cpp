#include <iostream>
#include <vector>
#include <string>
#include <iomanip>

using namespace std;

// =====================================================
// Transaction Class
// =====================================================

class Transaction {
private:
    string type;
    double amount;
    string description;

public:
    Transaction(string transactionType,
                double transactionAmount,
                string transactionDescription) {

        type = transactionType;
        amount = transactionAmount;
        description = transactionDescription;
    }

    void display() const {
        cout << left
             << setw(15) << type
             << setw(15) << fixed << setprecision(2) << amount
             << description << endl;
    }
};


// =====================================================
// Bank Account Class
// =====================================================

class BankAccount {
private:
    int accountNumber;
    string holderName;
    string accountType;
    double balance;

    vector<Transaction> transactions;

public:

    BankAccount(int number,
                string name,
                string type,
                double initialBalance) {

        accountNumber = number;
        holderName = name;
        accountType = type;
        balance = initialBalance;
    }

    int getAccountNumber() const {
        return accountNumber;
    }

    string getHolderName() const {
        return holderName;
    }

    string getAccountType() const {
        return accountType;
    }

    double getBalance() const {
        return balance;
    }

    // ---------------------------------------------
    // Deposit Money
    // ---------------------------------------------

    bool deposit(double amount) {

        if (amount <= 0) {
            return false;
        }

        balance += amount;

        transactions.push_back(
            Transaction(
                "DEPOSIT",
                amount,
                "Money deposited"
            )
        );

        return true;
    }

    // ---------------------------------------------
    // Withdraw Money
    // ---------------------------------------------

    bool withdraw(double amount) {

        if (amount <= 0) {
            return false;
        }

        if (amount > balance) {
            return false;
        }

        balance -= amount;

        transactions.push_back(
            Transaction(
                "WITHDRAW",
                amount,
                "Money withdrawn"
            )
        );

        return true;
    }

    // ---------------------------------------------
    // Display Account
    // ---------------------------------------------

    void displayAccount() const {

        cout << "\n----------------------------------------\n";
        cout << "Account Number : " << accountNumber << endl;
        cout << "Holder Name    : " << holderName << endl;
        cout << "Account Type   : " << accountType << endl;

        cout << "Balance        : $"
             << fixed
             << setprecision(2)
             << balance
             << endl;

        cout << "----------------------------------------\n";
    }

    // ---------------------------------------------
    // Display Transactions
    // ---------------------------------------------

    void statement() const {

        cout << "\n========================================\n";
        cout << "          ACCOUNT STATEMENT\n";
        cout << "========================================\n";

        cout << left
             << setw(15) << "TYPE"
             << setw(15) << "AMOUNT"
             << "DESCRIPTION"
             << endl;

        cout << "----------------------------------------\n";

        if (transactions.empty()) {

            cout << "No transactions available.\n";
            return;
        }

        for (const auto &transaction : transactions) {
            transaction.display();
        }

        cout << "----------------------------------------\n";
        cout << "Current Balance: $"
             << fixed
             << setprecision(2)
             << balance
             << endl;
    }
};


// =====================================================
// Bank Management Class
// =====================================================

class Bank {
private:
    vector<BankAccount> accounts;
    int nextAccountNumber;

public:

    Bank() {
        nextAccountNumber = 1001;
    }

    // ---------------------------------------------
    // Find Account
    // ---------------------------------------------

    BankAccount* findAccount(int accountNumber) {

        for (auto &account : accounts) {

            if (account.getAccountNumber()
                == accountNumber) {

                return &account;
            }
        }

        return nullptr;
    }

    // ---------------------------------------------
    // Create Account
    // ---------------------------------------------

    void createAccount() {

        string name;
        string type;
        double initialDeposit;

        cin.ignore();

        cout << "\nEnter account holder name: ";
        getline(cin, name);

        cout << "Enter account type: ";
        getline(cin, type);

        cout << "Enter initial deposit: ";
        cin >> initialDeposit;

        if (initialDeposit < 0) {

            cout << "Invalid initial deposit.\n";
            return;
        }

        BankAccount account(
            nextAccountNumber,
            name,
            type,
            initialDeposit
        );

        accounts.push_back(account);

        cout << "\nAccount created successfully!\n";

        cout << "Account Number: "
             << nextAccountNumber
             << endl;

        nextAccountNumber++;
    }

    // ---------------------------------------------
    // Display All Accounts
    // ---------------------------------------------

    void displayAccounts() const {

        if (accounts.empty()) {

            cout << "\nNo accounts available.\n";
            return;
        }

        cout << "\n========== ALL ACCOUNTS ==========\n";

        for (const auto &account : accounts) {
            account.displayAccount();
        }
    }

    // ---------------------------------------------
    // Search Account
    // ---------------------------------------------

    void searchAccount() {

        int number;

        cout << "\nEnter account number: ";
        cin >> number;

        BankAccount *account = findAccount(number);

        if (account == nullptr) {

            cout << "Account not found.\n";
            return;
        }

        account->displayAccount();
    }

    // ---------------------------------------------
    // Deposit
    // ---------------------------------------------

    void depositMoney() {

        int number;
        double amount;

        cout << "\nEnter account number: ";
        cin >> number;

        BankAccount *account = findAccount(number);

        if (account == nullptr) {

            cout << "Account not found.\n";
            return;
        }

        cout << "Enter amount to deposit: ";
        cin >> amount;

        if (account->deposit(amount)) {

            cout << "Deposit successful.\n";

            cout << "New Balance: $"
                 << account->getBalance()
                 << endl;

        } else {

            cout << "Invalid deposit amount.\n";
        }
    }

    // ---------------------------------------------
    // Withdraw
    // ---------------------------------------------

    void withdrawMoney() {

        int number;
        double amount;

        cout << "\nEnter account number: ";
        cin >> number;

        BankAccount *account = findAccount(number);

        if (account == nullptr) {

            cout << "Account not found.\n";
            return;
        }

        cout << "Enter amount to withdraw: ";
        cin >> amount;

        if (account->withdraw(amount)) {

            cout << "Withdrawal successful.\n";

            cout << "Remaining Balance: $"
                 << account->getBalance()
                 << endl;

        } else {

            cout << "Withdrawal failed.\n";
            cout << "Check amount and available balance.\n";
        }
    }

    // ---------------------------------------------
    // Transfer Money
    // ---------------------------------------------

    void transferMoney() {

        int senderNumber;
        int receiverNumber;
        double amount;

        cout << "\nEnter sender account: ";
        cin >> senderNumber;

        cout << "Enter receiver account: ";
        cin >> receiverNumber;

        if (senderNumber == receiverNumber) {

            cout << "Sender and receiver cannot be same.\n";
            return;
        }

        BankAccount *sender =
            findAccount(senderNumber);

        BankAccount *receiver =
            findAccount(receiverNumber);

        if (sender == nullptr ||
            receiver == nullptr) {

            cout << "One or both accounts not found.\n";
            return;
        }

        cout << "Enter transfer amount: ";
        cin >> amount;

        if (amount <= 0) {

            cout << "Invalid transfer amount.\n";
            return;
        }

        if (sender->getBalance() < amount) {

            cout << "Insufficient balance.\n";
            return;
        }

        sender->withdraw(amount);
        receiver->deposit(amount);

        cout << "\nTransfer successful.\n";

        cout << "Transferred: $"
             << amount
             << endl;
    }

    // ---------------------------------------------
    // Account Statement
    // ---------------------------------------------

    void showStatement() {

        int number;

        cout << "\nEnter account number: ";
        cin >> number;

        BankAccount *account = findAccount(number);

        if (account == nullptr) {

            cout << "Account not found.\n";
            return;
        }

        account->statement();
    }

    // ---------------------------------------------
    // Total Bank Balance
    // ---------------------------------------------

    void totalBankBalance() const {

        double total = 0;

        for (const auto &account : accounts) {
            total += account.getBalance();
        }

        cout << "\nTotal money held by bank: $"
             << fixed
             << setprecision(2)
             << total
             << endl;
    }

    // ---------------------------------------------
    // Account Statistics
    // ---------------------------------------------

    void statistics() const {

        if (accounts.empty()) {

            cout << "\nNo accounts available.\n";
            return;
        }

        double total = 0;

        double highestBalance =
            accounts[0].getBalance();

        string richestCustomer =
            accounts[0].getHolderName();

        for (const auto &account : accounts) {

            total += account.getBalance();

            if (account.getBalance()
                > highestBalance) {

                highestBalance =
                    account.getBalance();

                richestCustomer =
                    account.getHolderName();
            }
        }

        double average =
            total / accounts.size();

        cout << "\n========== BANK STATISTICS ==========\n";

        cout << "Total Accounts : "
             << accounts.size()
             << endl;

        cout << "Total Balance  : $"
             << fixed
             << setprecision(2)
             << total
             << endl;

        cout << "Average Balance: $"
             << average
             << endl;

        cout << "Highest Balance: $"
             << highestBalance
             << endl;

        cout << "Top Customer   : "
             << richestCustomer
             << endl;
    }

    // ---------------------------------------------
    // Display Menu
    // ---------------------------------------------

    void menu() const {

        cout << "\n========================================\n";
        cout << "        BANK ACCOUNT MANAGEMENT\n";
        cout << "========================================\n";
        cout << "1.  Create Account\n";
        cout << "2.  Display Accounts\n";
        cout << "3.  Search Account\n";
        cout << "4.  Deposit Money\n";
        cout << "5.  Withdraw Money\n";
        cout << "6.  Transfer Money\n";
        cout << "7.  Account Statement\n";
        cout << "8.  Total Bank Balance\n";
        cout << "9.  Bank Statistics\n";
        cout << "10. Exit\n";
        cout << "========================================\n";
    }
};


// =====================================================
// Main Function
// =====================================================

int main() {

    Bank bank;

    int choice;

    cout << "Welcome to the Bank Management System!\n";

    while (true) {

        bank.menu();

        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {

            case 1:
                bank.createAccount();
                break;

            case 2:
                bank.displayAccounts();
                break;

            case 3:
                bank.searchAccount();
                break;

            case 4:
                bank.depositMoney();
                break;

            case 5:
                bank.withdrawMoney();
                break;

            case 6:
                bank.transferMoney();
                break;

            case 7:
                bank.showStatement();
                break;

            case 8:
                bank.totalBankBalance();
                break;

            case 9:
                bank.statistics();
                break;

            case 10:

                cout << "\nThank you for using "
                     << "the Bank Management System.\n";

                return 0;

            default:

                cout << "\nInvalid choice.\n";
                cout << "Please select an option "
                     << "from 1 to 10.\n";
        }
    }

    return 0;
}
