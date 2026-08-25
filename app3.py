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
        "stock": 10
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "category": "Accessories",
        "price": 1200,
        "stock": 25
    },
    {
        "id": 3,
        "name": "Keyboard",
        "category": "Accessories",
        "price": 2500,
        "stock": 15
    }
]

orders = []

next_product_id = 4
next_order_id = 1001


# ============================================================
# Home Endpoint
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "application": "Product Management API",
        "status": "running",
        "version": "1.0"
    })


# ============================================================
# Get All Products
# ============================================================

@app.route("/products", methods=["GET"])
def get_products():

    return jsonify({
        "count": len(products),
        "products": products
    })


# ============================================================
# Get Product By ID
# ============================================================

@app.route("/products/<int:product_id>",
           methods=["GET"])
def get_product(product_id):

    for product in products:

        if product["id"] == product_id:

            return jsonify(product)

    return jsonify({
        "error": "Product not found"
    }), 404


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

    if price <= 0:

        return jsonify({
            "error": "Price must be greater than zero"
        }), 400

    if stock < 0:

        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    product = {
        "id": next_product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock
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

@app.route("/products/<int:product_id>",
           methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON request body is required"
        }), 400

    for product in products:

        if product["id"] == product_id:

            if "name" in data:
                product["name"] = data["name"]

            if "category" in data:
                product["category"] = data["category"]

            if "price" in data:

                if data["price"] <= 0:

                    return jsonify({
                        "error":
                        "Price must be greater than zero"
                    }), 400

                product["price"] = data["price"]

            if "stock" in data:

                if data["stock"] < 0:

                    return jsonify({
                        "error":
                        "Stock cannot be negative"
                    }), 400

                product["stock"] = data["stock"]

            return jsonify({
                "message": "Product updated successfully",
                "product": product
            })

    return jsonify({
        "error": "Product not found"
    }), 404


# ============================================================
# Delete Product
# ============================================================

@app.route("/products/<int:product_id>",
           methods=["DELETE"])
def delete_product(product_id):

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            return jsonify({
                "message":
                "Product deleted successfully"
            })

    return jsonify({
        "error": "Product not found"
    }), 404


# ============================================================
# Search Products
# ============================================================

@app.route("/products/search",
           methods=["GET"])
def search_products():

    keyword = request.args.get(
        "q",
        ""
    ).lower()

    if not keyword:

        return jsonify({
            "error":
            "Search keyword is required"
        }), 400

    results = []

    for product in products:

        name = product["name"].lower()

        category = product["category"].lower()

        if (
            keyword in name
            or keyword in category
        ):

            results.append(product)

    return jsonify({
        "query": keyword,
        "count": len(results),
        "results": results
    })


# ============================================================
# Filter Products By Category
# ============================================================

@app.route(
    "/products/category/<category>",
    methods=["GET"]
)
def products_by_category(category):

    results = []

    for product in products:

        if (
            product["category"].lower()
            == category.lower()
        ):

            results.append(product)

    return jsonify({
        "category": category,
        "count": len(results),
        "products": results
    })


# ============================================================
# Low Stock Products
# ============================================================

@app.route("/products/low-stock",
           methods=["GET"])
def low_stock():

    threshold = request.args.get(
        "threshold",
        default=5,
        type=int
    )

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

    if new_stock < 0:

        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    for product in products:

        if product["id"] == product_id:

            product["stock"] = new_stock

            return jsonify({
                "message": "Stock updated",
                "product": product
            })

    return jsonify({
        "error": "Product not found"
    }), 404


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

    product_id = data.get("product_id")

    quantity = data.get("quantity")

    if not customer:

        return jsonify({
            "error": "Customer name is required"
        }), 400

    if product_id is None:

        return jsonify({
            "error": "Product ID is required"
        }), 400

    if quantity is None:

        return jsonify({
            "error": "Quantity is required"
        }), 400

    if quantity <= 0:

        return jsonify({
            "error":
            "Quantity must be greater than zero"
        }), 400

    selected_product = None

    for product in products:

        if product["id"] == product_id:

            selected_product = product
            break

    if selected_product is None:

        return jsonify({
            "error": "Product not found"
        }), 404

    if selected_product["stock"] < quantity:

        return jsonify({
            "error": "Insufficient stock"
        }), 400

    total = (
        selected_product["price"]
        * quantity
    )

    selected_product["stock"] -= quantity

    order = {
        "id": next_order_id,
        "customer": customer,
        "product_id": product_id,
        "product_name":
            selected_product["name"],
        "quantity": quantity,
        "total": total,
        "status": "Pending",
        "created_at":
            datetime.now().isoformat()
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

    return jsonify({
        "count": len(orders),
        "orders": orders
    })


# ============================================================
# Get Order By ID
# ============================================================

@app.route("/orders/<int:order_id>",
           methods=["GET"])
def get_order(order_id):

    for order in orders:

        if order["id"] == order_id:

            return jsonify(order)

    return jsonify({
        "error": "Order not found"
    }), 404


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
            "allowed":
                allowed_statuses
        }), 400

    for order in orders:

        if order["id"] == order_id:

            order["status"] = status

            return jsonify({
                "message":
                    "Order status updated",
                "order": order
            })

    return jsonify({
        "error": "Order not found"
    }), 404


# ============================================================
# Cancel Order
# ============================================================

@app.route(
    "/orders/<int:order_id>",
    methods=["DELETE"]
)
def cancel_order(order_id):

    for order in orders:

        if order["id"] == order_id:

            if order["status"] == "Delivered":

                return jsonify({
                    "error":
                    "Delivered order cannot be cancelled"
                }), 400

            order["status"] = "Cancelled"

            return jsonify({
                "message":
                    "Order cancelled successfully",
                "order": order
            })

    return jsonify({
        "error": "Order not found"
    }), 404


# ============================================================
# Statistics
# ============================================================

@app.route("/statistics", methods=["GET"])
def statistics():

    total_products = len(products)

    total_stock = 0

    inventory_value = 0

    for product in products:

        total_stock += product["stock"]

        inventory_value += (
            product["price"]
            * product["stock"]
        )

    total_orders = len(orders)

    completed_orders = 0

    cancelled_orders = 0

    revenue = 0

    for order in orders:

        if order["status"] == "Delivered":

            completed_orders += 1

            revenue += order["total"]

        elif order["status"] == "Cancelled":

            cancelled_orders += 1

    return jsonify({

        "products": {
            "total": total_products,
            "total_stock": total_stock,
            "inventory_value":
                inventory_value
        },

        "orders": {
            "total": total_orders,
            "completed":
                completed_orders,
            "cancelled":
                cancelled_orders,
            "revenue": revenue
        }
    })


# ============================================================
# API Information
# ============================================================

@app.route("/api/info", methods=["GET"])
def api_info():

    return jsonify({

        "name":
            "Product Management REST API",

        "endpoints": [
            "GET /",
            "GET /products",
            "GET /products/<id>",
            "POST /products",
            "PUT /products/<id>",
            "DELETE /products/<id>",
            "GET /products/search?q=keyword",
            "GET /products/category/<category>",
            "GET /products/low-stock",
            "PATCH /products/<id>/stock",
            "POST /orders",
            "GET /orders",
            "GET /orders/<id>",
            "PATCH /orders/<id>/status",
            "DELETE /orders/<id>",
            "GET /statistics"
        ]
    })


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(404)
def handle_404(error):

    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def handle_405(error):

    return jsonify({
        "error": "HTTP method not allowed"
    }), 405


@app.errorhandler(500)
def handle_500(error):

    return jsonify({
        "error": "Internal server error"
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
