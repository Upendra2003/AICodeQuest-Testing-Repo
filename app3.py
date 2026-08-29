from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ============================================================
# In-Memory Data
# ============================================================

products = [
    {
        "id": 1,
        "name": "Laptop",
        "category": "Electronics",
        "price": 75000,
        "stock": 10,
        "rating": 4.5,
        "supplier": "TechWorld",
        "description": "High-performance laptop for work and study",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "category": "Accessories",
        "price": 1200,
        "stock": 25,
        "rating": 4.2,
        "supplier": "MouseHub",
        "description": "Ergonomic wireless mouse with USB receiver",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": 3,
        "name": "Keyboard",
        "category": "Accessories",
        "price": 2500,
        "stock": 15,
        "rating": 4.6,
        "supplier": "KeyTech",
        "description": "Mechanical keyboard with RGB lighting",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": 4,
        "name": "Monitor",
        "category": "Electronics",
        "price": 18000,
        "stock": 8,
        "rating": 4.7,
        "supplier": "DisplayPro",
        "description": "27-inch full HD monitor",
        "created_at": datetime.now().isoformat()
    }
]

orders = []

next_product_id = 5
next_order_id = 1001


# ============================================================
# Utility Functions
# ============================================================

def find_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product

    return None


def find_order(order_id):
    for order in orders:
        if order["id"] == order_id:
            return order

    return None


def calculate_discount(total, discount):
    if discount <= 0:
        return total

    discount_amount = total * (discount / 100)
    return round(total - discount_amount, 2)


# ============================================================
# Home Endpoint
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "application": "Product Management API",
        "status": "running",
        "version": "2.0",
        "message": "Welcome to the Product Management API"
    })


# ============================================================
# Health Check
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "products_loaded": len(products),
        "orders_created": len(orders)
    })


# ============================================================
# Get All Products
# ============================================================

@app.route("/products", methods=["GET"])
def get_products():

    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({
            "error": "Page and limit must be integers"
        }), 400

    if page <= 0 or limit <= 0:
        return jsonify({
            "error": "Page and limit must be greater than zero"
        }), 400

    sort_by = request.args.get("sort", "id")
    order = request.args.get("order", "asc").lower()

    allowed_sort_fields = [
        "id",
        "name",
        "price",
        "stock",
        "rating"
    ]

    if sort_by not in allowed_sort_fields:
        return jsonify({
            "error": "Invalid sort field",
            "allowed": allowed_sort_fields
        }), 400

    if order not in ["asc", "desc"]:
        return jsonify({
            "error": "Order must be asc or desc"
        }), 400

    sorted_products = sorted(
        products,
        key=lambda item: item[sort_by],
        reverse=(order == "desc")
    )

    start = (page - 1) * limit
    end = start + limit

    selected_products = sorted_products[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(products),
        "sort": sort_by,
        "order": order,
        "products": selected_products
    })


# ============================================================
# Get Product By ID
# ============================================================

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    product = find_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)


# ============================================================
# Create Product
# ============================================================

@app.route("/products", methods=["POST"])
def create_product():

    global next_product_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON request body is required"
        }), 400

    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    stock = data.get("stock")
    rating = data.get("rating", 0)
    supplier = data.get("supplier", "Unknown")
    description = data.get(
        "description",
        "No description available"
    )

    if not name:
        return jsonify({
            "error": "Product name is required"
        }), 400

    if not category:
        return jsonify({
            "error": "Category is required"
        }), 400

    if price is None:
        return jsonify({
            "error": "Price is required"
        }), 400

    if stock is None:
        return jsonify({
            "error": "Stock is required"
        }), 400

    if not isinstance(price, (int, float)):
        return jsonify({
            "error": "Price must be a number"
        }), 400

    if not isinstance(stock, int):
        return jsonify({
            "error": "Stock must be an integer"
        }), 400

    if price <= 0:
        return jsonify({
            "error": "Price must be greater than zero"
        }), 400

    if stock < 0:
        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    if not isinstance(rating, (int, float)):
        return jsonify({
            "error": "Rating must be a number"
        }), 400

    if rating < 0 or rating > 5:
        return jsonify({
            "error": "Rating must be between 0 and 5"
        }), 400

    product = {
        "id": next_product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "rating": rating,
        "supplier": supplier,
        "description": description,
        "created_at": datetime.now().isoformat()
    }

    products.append(product)
    next_product_id += 1

    return jsonify({
        "message": "Product created successfully",
        "product": product
    }), 201


# ============================================================
# Update Product
# ============================================================

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON request body is required"
        }), 400

    product = find_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    if "name" in data:

        if not data["name"]:
            return jsonify({
                "error": "Name cannot be empty"
            }), 400

        product["name"] = data["name"]

    if "category" in data:

        if not data["category"]:
            return jsonify({
                "error": "Category cannot be empty"
            }), 400

        product["category"] = data["category"]

    if "description" in data:
        product["description"] = data["description"]

    if "supplier" in data:
        product["supplier"] = data["supplier"]

    if "price" in data:

        if not isinstance(data["price"], (int, float)):
            return jsonify({
                "error": "Price must be a number"
            }), 400

        if data["price"] <= 0:
            return jsonify({
                "error": "Price must be greater than zero"
            }), 400

        product["price"] = data["price"]

    if "stock" in data:

        if not isinstance(data["stock"], int):
            return jsonify({
                "error": "Stock must be an integer"
            }), 400

        if data["stock"] < 0:
            return jsonify({
                "error": "Stock cannot be negative"
            }), 400

        product["stock"] = data["stock"]

    if "rating" in data:

        if data["rating"] < 0 or data["rating"] > 5:
            return jsonify({
                "error": "Rating must be between 0 and 5"
            }), 400

        product["rating"] = data["rating"]

    product["updated_at"] = datetime.now().isoformat()

    return jsonify({
        "message": "Product updated successfully",
        "product": product
    })


# ============================================================
# Delete Product
# ============================================================

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    product = find_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    products.remove(product)

    return jsonify({
        "message": "Product deleted successfully",
        "deleted_product": product["name"]
    })


# ============================================================
# Search Products
# ============================================================

@app.route("/products/search", methods=["GET"])
def search_products():

    keyword = request.args.get("q", "").lower()

    if not keyword:
        return jsonify({
            "error": "Search keyword is required"
        }), 400

    results = []

    for product in products:

        searchable_text = (
            product["name"] + " " +
            product["category"] + " " +
            product["supplier"] + " " +
            product["description"]
        ).lower()

        if keyword in searchable_text:
            results.append(product)

    return jsonify({
        "query": keyword,
        "count": len(results),
        "results": results
    })


# ============================================================
# Filter Products By Category
# ============================================================

@app.route("/products/category/<category>", methods=["GET"])
def products_by_category(category):

    results = []

    for product in products:

        if product["category"].lower() == category.lower():
            results.append(product)

    return jsonify({
        "category": category,
        "count": len(results),
        "products": results
    })


# ============================================================
# Featured Products
# ============================================================

@app.route("/products/featured", methods=["GET"])
def featured_products():

    minimum_rating = request.args.get(
        "rating",
        default=4.5,
        type=float
    )

    results = []

    for product in products:

        if product["rating"] >= minimum_rating:
            results.append(product)

    results.sort(
        key=lambda product: product["rating"],
        reverse=True
    )

    return jsonify({
        "minimum_rating": minimum_rating,
        "count": len(results),
        "products": results
    })


# ============================================================
# Low Stock Products
# ============================================================

@app.route("/products/low-stock", methods=["GET"])
def low_stock():

    threshold = request.args.get(
        "threshold",
        default=5,
        type=int
    )

    if threshold < 0:
        return jsonify({
            "error": "Threshold cannot be negative"
        }), 400

    results = []

    for product in products:

        if product["stock"] <= threshold:
            results.append(product)

    return jsonify({
        "threshold": threshold,
        "count": len(results),
        "products": results
    })


# ============================================================
# Update Stock
# ============================================================

@app.route(
    "/products/<int:product_id>/stock",
    methods=["PATCH"]
)
def update_stock(product_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON request body is required"
        }), 400

    if "stock" not in data:
        return jsonify({
            "error": "Stock value is required"
        }), 400

    new_stock = data["stock"]

    if not isinstance(new_stock, int):
        return jsonify({
            "error": "Stock must be an integer"
        }), 400

    if new_stock < 0:
        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    product = find_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    old_stock = product["stock"]
    product["stock"] = new_stock
    product["updated_at"] = datetime.now().isoformat()

    return jsonify({
        "message": "Stock updated",
        "old_stock": old_stock,
        "new_stock": new_stock,
        "product": product
    })


# ============================================================
# Update Product Rating
# ============================================================

@app.route(
    "/products/<int:product_id>/rating",
    methods=["PATCH"]
)
def update_rating(product_id):

    data = request.get_json()

    if not data or "rating" not in data:
        return jsonify({
            "error": "Rating value is required"
        }), 400

    rating = data["rating"]

    if not isinstance(rating, (int, float)):
        return jsonify({
            "error": "Rating must be a number"
        }), 400

    if rating < 0 or rating > 5:
        return jsonify({
            "error": "Rating must be between 0 and 5"
        }), 400

    product = find_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    product["rating"] = rating
    product["updated_at"] = datetime.now().isoformat()

    return jsonify({
        "message": "Product rating updated",
        "product": product
    })


# ============================================================
# Create Order
# ============================================================

@app.route("/orders", methods=["POST"])
def create_order():

    global next_order_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON request body is required"
        }), 400

    customer = data.get("customer")
    email = data.get("email")
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    discount = data.get("discount", 0)

    if not customer:
        return jsonify({
            "error": "Customer name is required"
        }), 400

    if not email:
        return jsonify({
            "error": "Customer email is required"
        }), 400

    if product_id is None:
        return jsonify({
            "error": "Product ID is required"
        }), 400

    if quantity is None:
        return jsonify({
            "error": "Quantity is required"
        }), 400

    if not isinstance(quantity, int):
        return jsonify({
            "error": "Quantity must be an integer"
        }), 400

    if quantity <= 0:
        return jsonify({
            "error": "Quantity must be greater than zero"
        }), 400

    if not isinstance(discount, (int, float)):
        return jsonify({
            "error": "Discount must be a number"
        }), 400

    if discount < 0 or discount > 100:
        return jsonify({
            "error": "Discount must be between 0 and 100"
        }), 400

    selected_product = find_product(product_id)

    if selected_product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    if selected_product["stock"] < quantity:
        return jsonify({
            "error": "Insufficient stock",
            "available_stock": selected_product["stock"]
        }), 400

    subtotal = selected_product["price"] * quantity
    total = calculate_discount(subtotal, discount)
    discount_amount = round(subtotal - total, 2)

    selected_product["stock"] -= quantity

    order = {
        "id": next_order_id,
        "customer": customer,
        "email": email,
        "product_id": product_id,
        "product_name": selected_product["name"],
        "quantity": quantity,
        "subtotal": subtotal,
        "discount_percent": discount,
        "discount_amount": discount_amount,
        "total": total,
        "status": "Pending",
        "created_at": datetime.now().isoformat()
    }

    orders.append(order)

    next_order_id += 1

    return jsonify({
        "message": "Order created successfully",
        "order": order
    }), 201


# ============================================================
# Get All Orders
# ============================================================

@app.route("/orders", methods=["GET"])
def get_orders():

    status = request.args.get("status")

    if status:

        filtered_orders = []

        for order in orders:

            if order["status"].lower() == status.lower():
                filtered_orders.append(order)

    else:
        filtered_orders = orders

    return jsonify({
        "count": len(filtered_orders),
        "orders": filtered_orders
    })


# ============================================================
# Get Order By ID
# ============================================================

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order)


# ============================================================
# Order Summary
# ============================================================

@app.route(
    "/orders/<int:order_id>/summary",
    methods=["GET"]
)
def order_summary(order_id):

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify({
        "order_id": order["id"],
        "customer": order["customer"],
        "product": order["product_name"],
        "quantity": order["quantity"],
        "subtotal": order["subtotal"],
        "discount": order["discount_amount"],
        "final_total": order["total"],
        "status": order["status"]
    })


# ============================================================
# Update Order Status
# ============================================================

@app.route(
    "/orders/<int:order_id>/status",
    methods=["PATCH"]
)
def update_order_status(order_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status",
            "allowed": allowed_statuses
        }), 400

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    if order["status"] == "Delivered":
        return jsonify({
            "error": "Delivered order cannot change status"
        }), 400

    order["status"] = status
    order["updated_at"] = datetime.now().isoformat()

    return jsonify({
        "message": "Order status updated",
        "order": order
    })


# ============================================================
# Cancel Order
# ============================================================

@app.route(
    "/orders/<int:order_id>",
    methods=["DELETE"]
)
def cancel_order(order_id):

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    if order["status"] == "Delivered":
        return jsonify({
            "error": "Delivered order cannot be cancelled"
        }), 400

    if order["status"] == "Cancelled":
        return jsonify({
            "error": "Order is already cancelled"
        }), 400

    product = find_product(order["product_id"])

    if product:
        product["stock"] += order["quantity"]

    order["status"] = "Cancelled"
    order["cancelled_at"] = datetime.now().isoformat()

    return jsonify({
        "message": "Order cancelled successfully",
        "order": order
    })


# ============================================================
# Inventory Summary
# ============================================================

@app.route("/inventory/summary", methods=["GET"])
def inventory_summary():

    total_products = len(products)
    total_stock = 0
    inventory_value = 0
    out_of_stock = 0
    low_stock_items = 0

    for product in products:

        total_stock += product["stock"]

        inventory_value += (
            product["price"] * product["stock"]
        )

        if product["stock"] == 0:
            out_of_stock += 1

        elif product["stock"] <= 5:
            low_stock_items += 1

    return jsonify({
        "total_products": total_products,
        "total_units": total_stock,
        "inventory_value": inventory_value,
        "out_of_stock": out_of_stock,
        "low_stock": low_stock_items
    })


# ============================================================
# Statistics
# ============================================================

@app.route("/statistics", methods=["GET"])
def statistics():

    total_products = len(products)

    total_stock = 0
    inventory_value = 0
    average_rating = 0

    for product in products:

        total_stock += product["stock"]

        inventory_value += (
            product["price"] *
            product["stock"]
        )

        average_rating += product["rating"]

    if total_products > 0:
        average_rating = round(
            average_rating / total_products,
            2
        )

    total_orders = len(orders)

    completed_orders = 0
    cancelled_orders = 0
    pending_orders = 0
    processing_orders = 0
    shipped_orders = 0

    revenue = 0

    for order in orders:

        if order["status"] == "Delivered":

            completed_orders += 1
            revenue += order["total"]

        elif order["status"] == "Cancelled":

            cancelled_orders += 1

        elif order["status"] == "Pending":

            pending_orders += 1

        elif order["status"] == "Processing":

            processing_orders += 1

        elif order["status"] == "Shipped":

            shipped_orders += 1

    return jsonify({

        "products": {
            "total": total_products,
            "total_stock": total_stock,
            "inventory_value": inventory_value,
            "average_rating": average_rating
        },

        "orders": {
            "total": total_orders,
            "completed": completed_orders,
            "cancelled": cancelled_orders,
            "pending": pending_orders,
            "processing": processing_orders,
            "shipped": shipped_orders,
            "revenue": revenue
        }
    })


# ============================================================
# API Information
# ============================================================

@app.route("/api/info", methods=["GET"])
def api_info():

    return jsonify({

        "name": "Product Management REST API",
        "version": "2.0",

        "endpoints": [

            "GET /",
            "GET /health",

            "GET /products",
            "GET /products?page=1&limit=5",
            "GET /products?sort=price&order=desc",

            "GET /products/<id>",
            "POST /products",
            "PUT /products/<id>",
            "DELETE /products/<id>",

            "GET /products/search?q=keyword",
            "GET /products/category/<category>",
            "GET /products/featured",
            "GET /products/low-stock",

            "PATCH /products/<id>/stock",
            "PATCH /products/<id>/rating",

            "POST /orders",
            "GET /orders",
            "GET /orders?status=Pending",
            "GET /orders/<id>",
            "GET /orders/<id>/summary",
            "PATCH /orders/<id>/status",
            "DELETE /orders/<id>",

            "GET /inventory/summary",
            "GET /statistics",
            "GET /api/info"
        ]
    })


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(404)
def handle_404(error):

    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested API endpoint does not exist"
    }), 404


@app.errorhandler(405)
def handle_405(error):

    return jsonify({
        "error": "HTTP method not allowed",
        "message": "This endpoint does not support the requested method"
    }), 405


@app.errorhandler(400)
def handle_400(error):

    return jsonify({
        "error": "Bad request",
        "message": "The request could not be processed"
    }), 400


@app.errorhandler(500)
def handle_500(error):

    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on the server"
    }), 500


# ============================================================
# Start Server
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
