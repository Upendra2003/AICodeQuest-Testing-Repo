from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# =====================================================
# Sample Menu
# =====================================================

menu = [
    {
        "id": 1,
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 250,
        "available": True
    },
    {
        "id": 2,
        "name": "Veg Burger",
        "category": "Burger",
        "price": 150,
        "available": True
    },
    {
        "id": 3,
        "name": "Pasta Alfredo",
        "category": "Pasta",
        "price": 220,
        "available": True
    }
]

orders = []

next_menu_id = 4
next_order_id = 1001


# =====================================================
# Helper Functions
# =====================================================

def find_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item

    return None


def find_order(order_id):
    for order in orders:
        if order["id"] == order_id:
            return order

    return None


# =====================================================
# Home
# =====================================================

@app.route("/")
def home():

    return jsonify({
        "application": "Restaurant Ordering API",
        "version": "1.0",
        "status": "running"
    })


# =====================================================
# Get Menu
# =====================================================

@app.route("/menu", methods=["GET"])
def get_menu():

    return jsonify({
        "count": len(menu),
        "items": menu
    })


# =====================================================
# Get Single Menu Item
# =====================================================

@app.route("/menu/<int:item_id>", methods=["GET"])
def get_menu_item(item_id):

    item = find_item(item_id)

    if item is None:
        return jsonify({
            "error": "Menu item not found"
        }), 404

    return jsonify(item)


# =====================================================
# Add Menu Item
# =====================================================

@app.route("/menu", methods=["POST"])
def add_menu_item():

    global next_menu_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    required = [
        "name",
        "category",
        "price"
    ]

    for field in required:

        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    if data["price"] <= 0:
        return jsonify({
            "error": "Price must be greater than zero"
        }), 400

    item = {
        "id": next_menu_id,
        "name": data["name"],
        "category": data["category"],
        "price": data["price"],
        "available": True
    }

    menu.append(item)

    next_menu_id += 1

    return jsonify({
        "message": "Menu item added",
        "item": item
    }), 201


# =====================================================
# Update Menu Item
# =====================================================

@app.route("/menu/<int:item_id>", methods=["PUT"])
def update_menu_item(item_id):

    item = find_item(item_id)

    if item is None:
        return jsonify({
            "error": "Menu item not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    item["name"] = data.get(
        "name",
        item["name"]
    )

    item["category"] = data.get(
        "category",
        item["category"]
    )

    item["price"] = data.get(
        "price",
        item["price"]
    )

    item["available"] = data.get(
        "available",
        item["available"]
    )

    return jsonify({
        "message": "Menu item updated",
        "item": item
    })


# =====================================================
# Delete Menu Item
# =====================================================

@app.route("/menu/<int:item_id>", methods=["DELETE"])
def delete_menu_item(item_id):

    item = find_item(item_id)

    if item is None:
        return jsonify({
            "error": "Menu item not found"
        }), 404

    menu.remove(item)

    return jsonify({
        "message": "Menu item deleted"
    })


# =====================================================
# Search Menu
# =====================================================

@app.route("/menu/search", methods=["GET"])
def search_menu():

    keyword = request.args.get(
        "name",
        ""
    ).lower()

    results = []

    for item in menu:

        if keyword in item["name"].lower():
            results.append(item)

    return jsonify({
        "count": len(results),
        "results": results
    })


# =====================================================
# Filter By Category
# =====================================================

@app.route("/menu/category/<category>", methods=["GET"])
def category_menu(category):

    results = []

    for item in menu:

        if item["category"].lower() == category.lower():
            results.append(item)

    return jsonify({
        "category": category,
        "count": len(results),
        "items": results
    })


# =====================================================
# Create Order
# =====================================================

@app.route("/orders", methods=["POST"])
def create_order():

    global next_order_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    customer = data.get("customer")
    item_ids = data.get("items")

    if not customer:
        return jsonify({
            "error": "Customer name is required"
        }), 400

    if not item_ids:
        return jsonify({
            "error": "At least one item is required"
        }), 400

    order_items = []
    total = 0

    for item_id in item_ids:

        item = find_item(item_id)

        if item is None:
            return jsonify({
                "error":
                f"Item {item_id} does not exist"
            }), 404

        if not item["available"]:
            return jsonify({
                "error":
                f"{item['name']} is unavailable"
            }), 400

        order_items.append({
            "id": item["id"],
            "name": item["name"],
            "price": item["price"]
        })

        total += item["price"]

    order = {
        "id": next_order_id,
        "customer": customer,
        "items": order_items,
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


# =====================================================
# Get All Orders
# =====================================================

@app.route("/orders", methods=["GET"])
def get_orders():

    return jsonify({
        "count": len(orders),
        "orders": orders
    })


# =====================================================
# Get Single Order
# =====================================================

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order)


# =====================================================
# Update Order Status
# =====================================================

@app.route("/orders/<int:order_id>/status",
           methods=["PATCH"])
def update_order_status(order_id):

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "error": "Status is required"
        }), 400

    valid_statuses = [
        "Pending",
        "Preparing",
        "Ready",
        "Delivered",
        "Cancelled"
    ]

    status = data["status"]

    if status not in valid_statuses:
        return jsonify({
            "error": "Invalid status",
            "valid_statuses": valid_statuses
        }), 400

    order["status"] = status

    return jsonify({
        "message": "Order status updated",
        "order": order
    })


# =====================================================
# Cancel Order
# =====================================================

@app.route("/orders/<int:order_id>",
           methods=["DELETE"])
def cancel_order(order_id):

    order = find_order(order_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    if order["status"] == "Delivered":
        return jsonify({
            "error":
            "Delivered orders cannot be cancelled"
        }), 400

    order["status"] = "Cancelled"

    return jsonify({
        "message": "Order cancelled",
        "order": order
    })


# =====================================================
# Sales Statistics
# =====================================================

@app.route("/statistics", methods=["GET"])
def statistics():

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

    average_order = 0

    if completed_orders > 0:
        average_order = (
            revenue / completed_orders
        )

    return jsonify({
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "revenue": round(revenue, 2),
        "average_order_value":
            round(average_order, 2)
    })


# =====================================================
# Popular Items
# =====================================================

@app.route("/statistics/popular",
           methods=["GET"])
def popular_items():

    item_count = {}

    for order in orders:

        if order["status"] == "Cancelled":
            continue

        for item in order["items"]:

            item_id = item["id"]

            if item_id not in item_count:
                item_count[item_id] = {
                    "name": item["name"],
                    "orders": 0
                }

            item_count[item_id]["orders"] += 1

    result = list(item_count.values())

    result.sort(
        key=lambda x: x["orders"],
        reverse=True
    )

    return jsonify(result)


# =====================================================
# API Information
# =====================================================

@app.route("/api/info", methods=["GET"])
def api_info():

    return jsonify({
        "name": "Restaurant Ordering API",
        "endpoints": [
            "GET /menu",
            "POST /menu",
            "GET /menu/<id>",
            "PUT /menu/<id>",
            "DELETE /menu/<id>",
            "GET /menu/search",
            "GET /menu/category/<category>",
            "POST /orders",
            "GET /orders",
            "GET /orders/<id>",
            "PATCH /orders/<id>/status",
            "DELETE /orders/<id>",
            "GET /statistics",
            "GET /statistics/popular"
        ]
    })


# =====================================================
# Error Handlers
# =====================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Requested resource not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "error": "HTTP method not allowed"
    }), 405


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500


# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
