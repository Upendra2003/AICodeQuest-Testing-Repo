from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert Martin",
        "available": True
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "available": True
    },
    {
        "id": 3,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "available": False
    }
]

borrowers = []
next_book_id = 4
next_borrower_id = 1


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "application": "Library Management API",
        "status": "running",
        "books": len(books),
        "borrowers": len(borrowers)
    })


# --------------------------------------------------
# Get All Books
# --------------------------------------------------

@app.route("/books", methods=["GET"])
def get_books():

    return jsonify({
        "count": len(books),
        "books": books
    })


# --------------------------------------------------
# Get Single Book
# --------------------------------------------------

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    for book in books:

        if book["id"] == book_id:
            return jsonify(book)

    return jsonify({
        "error": "Book not found"
    }), 404


# --------------------------------------------------
# Add Book
# --------------------------------------------------

@app.route("/books", methods=["POST"])
def add_book():

    global next_book_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({
            "error": "Title and author are required"
        }), 400

    book = {
        "id": next_book_id,
        "title": title,
        "author": author,
        "available": True
    }

    books.append(book)
    next_book_id += 1

    return jsonify({
        "message": "Book added successfully",
        "book": book
    }), 201


# --------------------------------------------------
# Delete Book
# --------------------------------------------------

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    for book in books:

        if book["id"] == book_id:

            if not book["available"]:
                return jsonify({
                    "error":
                    "Borrowed book cannot be deleted"
                }), 400

            books.remove(book)

            return jsonify({
                "message": "Book deleted successfully"
            })

    return jsonify({
        "error": "Book not found"
    }), 404


# --------------------------------------------------
# Search Books
# --------------------------------------------------

@app.route("/books/search", methods=["GET"])
def search_books():

    keyword = request.args.get("q", "").lower()

    if not keyword:
        return jsonify({
            "error": "Search keyword is required"
        }), 400

    results = []

    for book in books:

        if (
            keyword in book["title"].lower()
            or keyword in book["author"].lower()
        ):
            results.append(book)

    return jsonify({
        "query": keyword,
        "count": len(results),
        "results": results
    })


# --------------------------------------------------
# Register Borrower
# --------------------------------------------------

@app.route("/borrowers", methods=["POST"])
def register_borrower():

    global next_borrower_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "Name and email are required"
        }), 400

    borrower = {
        "id": next_borrower_id,
        "name": name,
        "email": email,
        "borrowed_books": []
    }

    borrowers.append(borrower)
    next_borrower_id += 1

    return jsonify({
        "message": "Borrower registered",
        "borrower": borrower
    }), 201


# --------------------------------------------------
# Get Borrowers
# --------------------------------------------------

@app.route("/borrowers", methods=["GET"])
def get_borrowers():

    return jsonify({
        "count": len(borrowers),
        "borrowers": borrowers
    })


# --------------------------------------------------
# Borrow Book
# --------------------------------------------------

@app.route(
    "/borrow/<int:book_id>/<int:borrower_id>",
    methods=["POST"]
)
def borrow_book(book_id, borrower_id):

    selected_book = None
    selected_borrower = None

    for book in books:

        if book["id"] == book_id:
            selected_book = book
            break

    for borrower in borrowers:

        if borrower["id"] == borrower_id:
            selected_borrower = borrower
            break

    if selected_book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    if selected_borrower is None:
        return jsonify({
            "error": "Borrower not found"
        }), 404

    if not selected_book["available"]:
        return jsonify({
            "error": "Book is already borrowed"
        }), 400

    selected_book["available"] = False

    selected_borrower["borrowed_books"].append({
        "book_id": book_id,
        "borrowed_at": datetime.now().isoformat()
    })

    return jsonify({
        "message": "Book borrowed successfully",
        "book": selected_book,
        "borrower": selected_borrower
    })


# --------------------------------------------------
# Return Book
# --------------------------------------------------

@app.route(
    "/return/<int:book_id>/<int:borrower_id>",
    methods=["POST"]
)
def return_book(book_id, borrower_id):

    selected_book = None
    selected_borrower = None

    for book in books:

        if book["id"] == book_id:
            selected_book = book
            break

    for borrower in borrowers:

        if borrower["id"] == borrower_id:
            selected_borrower = borrower
            break

    if selected_book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    if selected_borrower is None:
        return jsonify({
            "error": "Borrower not found"
        }), 404

    borrowed = selected_borrower["borrowed_books"]

    matching = [
        item for item in borrowed
        if item["book_id"] == book_id
    ]

    if not matching:
        return jsonify({
            "error":
            "This borrower does not have the book"
        }), 400

    selected_book["available"] = True

    selected_borrower["borrowed_books"] = [
        item for item in borrowed
        if item["book_id"] != book_id
    ]

    return jsonify({
        "message": "Book returned successfully",
        "book": selected_book
    })


# --------------------------------------------------
# Library Statistics
# --------------------------------------------------

@app.route("/statistics", methods=["GET"])
def statistics():

    total = len(books)

    available = sum(
        1 for book in books
        if book["available"]
    )

    borrowed = total - available

    return jsonify({
        "total_books": total,
        "available_books": available,
        "borrowed_books": borrowed,
        "registered_borrowers": len(borrowers)
    })


# --------------------------------------------------
# Error Handlers
# --------------------------------------------------

@app.errorhandler(404)
def handle_not_found(error):

    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def handle_method_error(error):

    return jsonify({
        "error": "Method not allowed"
    }), 405


# --------------------------------------------------
# Start Server
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
