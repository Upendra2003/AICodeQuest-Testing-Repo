from flask import Flask, request, jsonify
from datetime import datetime
import logging

app = Flask(__name__)

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(level=logging.INFO)

# -------------------------------------------------------
# In-memory database
# -------------------------------------------------------
tasks = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "id": 2,
        "title": "Build REST API",
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
]

next_id = 3


# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------
def find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def validate_task(data):
    if not data:
        return False, "JSON body is required"

    title = data.get("title")

    if not title:
        return False, "title is required"

    if len(title.strip()) < 3:
        return False, "title must contain at least 3 characters"

    return True, ""


# -------------------------------------------------------
# Routes
# -------------------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Flask Task API",
        "version": "1.0",
        "status": "running"
    })


@app.route("/about")
def about():
    return jsonify({
        "application": "Task Manager",
        "author": "OpenAI",
        "language": "Python",
        "framework": "Flask"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "time": datetime.now().isoformat()
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = find_task(task_id)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json()

    valid, message = validate_task(data)

    if not valid:
        return jsonify({"error": message}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    tasks.append(task)
    next_id += 1

    logging.info("Task created: %s", task)

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = find_task(task_id)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    if "title" in data:
        task["title"] = data["title"]

    if "completed" in data:
        task["completed"] = bool(data["completed"])

    logging.info("Task updated: %s", task)

    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = find_task(task_id)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)

    logging.info("Task deleted: %s", task)

    return jsonify({
        "message": "Task deleted successfully"
    })


@app.route("/stats")
def stats():
    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending = total - completed

    return jsonify({
        "total_tasks": total,
        "completed": completed,
        "pending": pending
    })


# -------------------------------------------------------
# Error Handlers
# -------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_server(error):
    return jsonify({
        "error": "Internal server error"
    }), 500


# -------------------------------------------------------
# Before Request
# -------------------------------------------------------
@app.before_request
def before_request():
    logging.info(
        "%s %s",
        request.method,
        request.path
    )


# -------------------------------------------------------
# After Request
# -------------------------------------------------------
@app.after_request
def after_request(response):
    response.headers["X-App-Name"] = "Flask Task API"
    return response


# -------------------------------------------------------
# Main
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
