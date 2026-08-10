from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data
books = [
    {
        "id": 1,
        "title": "Python Basics",
        "author": "John Smith",
        "price": 450
    },
    {
        "id": 2,
        "title": "Flask Web Development",
        "author": "Jane Doe",
        "price": 650
    }
]

next_id = 3


# Helper function
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


# --------------------------
# GET /
# Home Endpoint
# --------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Book Management REST API",
        "status": "Running"
    })


# --------------------------
# GET /books
# Get all books
# --------------------------
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)


# --------------------------
# GET /books/<id>
# Get one book
# --------------------------
@app.route("/books/<int:book_id>", methods=["GET"])
def get_single_book(book_id):

    book = get_book(book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book)


# --------------------------
# POST /books
# Create new book
# --------------------------
@app.route("/books", methods=["POST"])
def add_book():

    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data required"}), 400

    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    if "author" not in data:
        return jsonify({"error": "Author is required"}), 400

    if "price" not in data:
        return jsonify({"error": "Price is required"}), 400

    book = {
        "id": next_id,
        "title": data["title"],
        "author": data["author"],
        "price": data["price"]
    }

    books.append(book)
    next_id += 1

    return jsonify(book), 201


# --------------------------
# PUT /books/<id>
# Update existing book
# --------------------------
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    book = get_book(book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["price"] = data.get("price", book["price"])

    return jsonify({
        "message": "Book updated successfully",
        "book": book
    })


# --------------------------
# DELETE /books/<id>
# Delete book
# --------------------------
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    book = get_book(book_id)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)

    return jsonify({
        "message": "Book deleted successfully"
    })


# --------------------------
# GET /search
# Search books by title
# Example:
# /search?title=python
# --------------------------
@app.route("/search", methods=["GET"])
def search_book():

    keyword = request.args.get("title", "").lower()

    result = []

    for book in books:
        if keyword in book["title"].lower():
            result.append(book)

    return jsonify(result)


# --------------------------
# GET /statistics
# API Statistics
# --------------------------
@app.route("/statistics", methods=["GET"])
def statistics():

    total_books = len(books)

    total_price = 0

    for book in books:
        total_price += book["price"]

    average_price = 0

    if total_books > 0:
        average_price = total_price / total_books

    return jsonify({
        "total_books": total_books,
        "average_price": average_price
    })


# --------------------------
# Error Handler
# --------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


# --------------------------
# Run Server
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
