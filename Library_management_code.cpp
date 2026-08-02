#include <iostream>
#include <vector>
#include <string>
#include <iomanip>

using namespace std;

class Book {
public:
    int id;
    string title;
    string author;
    bool issued;

    Book(int bookId, string bookTitle, string bookAuthor) {
        id = bookId;
        title = bookTitle;
        author = bookAuthor;
        issued = false;
    }
};

class Library {
private:
    vector<Book> books;

public:
    void addBook() {
        int id;
        string title, author;

        cout << "\nEnter Book ID: ";
        cin >> id;
        cin.ignore();

        cout << "Enter Book Title: ";
        getline(cin, title);

        cout << "Enter Author Name: ";
        getline(cin, author);

        books.push_back(Book(id, title, author));

        cout << "\nBook added successfully.\n";
    }

    void displayBooks() {
        if (books.empty()) {
            cout << "\nNo books available.\n";
            return;
        }

        cout << "\n-------------------------------------------------------------\n";
        cout << left << setw(10) << "ID"
             << setw(25) << "Title"
             << setw(20) << "Author"
             << setw(10) << "Status" << endl;
        cout << "-------------------------------------------------------------\n";

        for (const auto &book : books) {
            cout << left
                 << setw(10) << book.id
                 << setw(25) << book.title
                 << setw(20) << book.author
                 << setw(10) << (book.issued ? "Issued" : "Available")
                 << endl;
        }
    }

    void searchBook() {
        int id;
        cout << "\nEnter Book ID to search: ";
        cin >> id;

        for (const auto &book : books) {
            if (book.id == id) {
                cout << "\nBook Found!\n";
                cout << "ID      : " << book.id << endl;
                cout << "Title   : " << book.title << endl;
                cout << "Author  : " << book.author << endl;
                cout << "Status  : "
                     << (book.issued ? "Issued" : "Available") << endl;
                return;
            }
        }

        cout << "\nBook not found.\n";
    }

    void issueBook() {
        int id;
        cout << "\nEnter Book ID to issue: ";
        cin >> id;

        for (auto &book : books) {
            if (book.id == id) {
                if (book.issued) {
                    cout << "\nBook is already issued.\n";
                } else {
                    book.issued = true;
                    cout << "\nBook issued successfully.\n";
                }
                return;
            }
        }

        cout << "\nBook not found.\n";
    }

    void returnBook() {
        int id;
        cout << "\nEnter Book ID to return: ";
        cin >> id;

        for (auto &book : books) {
            if (book.id == id) {
                if (!book.issued) {
                    cout << "\nBook was not issued.\n";
                } else {
                    book.issued = false;
                    cout << "\nBook returned successfully.\n";
                }
                return;
            }
        }

        cout << "\nBook not found.\n";
    }

    void deleteBook() {
        int id;
        cout << "\nEnter Book ID to delete: ";
        cin >> id;

        for (auto it = books.begin(); it != books.end(); ++it) {
            if (it->id == id) {
                books.erase(it);
                cout << "\nBook deleted successfully.\n";
                return;
            }
        }

        cout << "\nBook not found.\n";
    }

    void statistics() {
        int total = books.size();
        int issued = 0;

        for (const auto &book : books) {
            if (book.issued)
                issued++;
        }

        cout << "\n========= Library Statistics =========\n";
        cout << "Total Books     : " << total << endl;
        cout << "Issued Books    : " << issued << endl;
        cout << "Available Books : " << total - issued << endl;
    }
};

int main() {
    Library library;

    int choice;

    while (true) {
        cout << "\n=====================================\n";
        cout << "     LIBRARY MANAGEMENT SYSTEM\n";
        cout << "=====================================\n";
        cout << "1. Add Book\n";
        cout << "2. Display All Books\n";
        cout << "3. Search Book\n";
        cout << "4. Issue Book\n";
        cout << "5. Return Book\n";
        cout << "6. Delete Book\n";
        cout << "7. Library Statistics\n";
        cout << "8. Exit\n";
        cout << "Enter your choice: ";

        cin >> choice;

        switch (choice) {
            case 1:
                library.addBook();
                break;

            case 2:
                library.displayBooks();
                break;

            case 3:
                library.searchBook();
                break;

            case 4:
                library.issueBook();
                break;

            case 5:
                library.returnBook();
                break;

            case 6:
                library.deleteBook();
                break;

            case 7:
                library.statistics();
                break;

            case 8:
                cout << "\nThank you for using the Library Management System.\n";
                return 0;

            default:
                cout << "\nInvalid choice. Please try again.\n";
        }
    }

    return 0;
}
