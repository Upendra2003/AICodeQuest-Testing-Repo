from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "task-manager-secret-key"

DATABASE = "tasks.db"


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_db_connection():
    """
    Create a connection with the SQLite database.
    Row factory allows us to access columns by name.
    """
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------

def init_db():
    """
    Create the tasks table if it does not already exist.
    """
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending',
            due_date TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.route("/")
def index():
    """
    Display all tasks.

    Supports:
    - Search
    - Status filtering
    - Priority filtering
    """

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")

    connection = get_db_connection()

    query = "SELECT * FROM tasks WHERE 1=1"
    parameters = []

    if search:
        query += """
            AND (
                title LIKE ?
                OR description LIKE ?
            )
        """

        search_value = f"%{search}%"
        parameters.extend([search_value, search_value])

    if status:
        query += " AND status = ?"
        parameters.append(status)

    if priority:
        query += " AND priority = ?"
        parameters.append(priority)

    query += """
        ORDER BY
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
            END,
            id DESC
    """

    tasks = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        tasks=tasks,
        search=search,
        status=status,
        priority=priority
    )


# ---------------------------------------------------------
# ADD TASK
# ---------------------------------------------------------

@app.route("/add", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")

        if not title:
            flash("Task title is required.", "danger")
            return redirect(url_for("add_task"))

        if not priority:
            priority = "Medium"

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO tasks
            (
                title,
                description,
                priority,
                status,
                due_date,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            description,
            priority,
            "Pending",
            due_date,
            created_at
        ))

        connection.commit()
        connection.close()

        flash("Task added successfully!", "success")

        return redirect(url_for("index"))

    return render_template("add_task.html")


# ---------------------------------------------------------
# EDIT TASK
# ---------------------------------------------------------

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")
        status = request.form.get("status")
        due_date = request.form.get("due_date")

        if not title:
            connection.close()
            flash("Task title cannot be empty.", "danger")
            return redirect(
                url_for("edit_task", task_id=task_id)
            )

        connection.execute("""
            UPDATE tasks
            SET
                title = ?,
                description = ?,
                priority = ?,
                status = ?,
                due_date = ?
            WHERE id = ?
        """, (
            title,
            description,
            priority,
            status,
            due_date,
            task_id
        ))

        connection.commit()
        connection.close()

        flash("Task updated successfully!", "success")

        return redirect(url_for("index"))

    connection.close()

    return render_template(
        "edit_task.html",
        task=task
    )


# ---------------------------------------------------------
# DELETE TASK
# ---------------------------------------------------------

@app.route("/delete/<int:task_id>")
def delete_task(task_id):

    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        flash("Task does not exist.", "danger")
        return redirect(url_for("index"))

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    flash("Task deleted successfully!", "success")

    return redirect(url_for("index"))


# ---------------------------------------------------------
# MARK TASK AS COMPLETED
# ---------------------------------------------------------

@app.route("/complete/<int:task_id>")
def complete_task(task_id):

    connection = get_db_connection()

    connection.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()

    flash("Task marked as completed!", "success")

    return redirect(url_for("index"))


# ---------------------------------------------------------
# MARK TASK AS PENDING
# ---------------------------------------------------------

@app.route("/pending/<int:task_id>")
def pending_task(task_id):

    connection = get_db_connection()

    connection.execute("""
        UPDATE tasks
        SET status = 'Pending'
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()

    flash("Task marked as pending.", "info")

    return redirect(url_for("index"))


# ---------------------------------------------------------
# TASK DETAILS
# ---------------------------------------------------------

@app.route("/task/<int:task_id>")
def task_details(task_id):

    connection = get_db_connection()

    task = connection.execute("""
        SELECT *
        FROM tasks
        WHERE id = ?
    """, (task_id,)).fetchone()

    connection.close()

    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    return render_template(
        "task_details.html",
        task=task
    )


# ---------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------

@app.route("/statistics")
def statistics():

    connection = get_db_connection()

    total = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
    """).fetchone()["count"]

    completed = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE status = 'Completed'
    """).fetchone()["count"]

    pending = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE status = 'Pending'
    """).fetchone()["count"]

    high_priority = connection.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
        WHERE priority = 'High'
    """).fetchone()["count"]

    connection.close()

    completion_rate = 0

    if total > 0:
        completion_rate = round(
            (completed / total) * 100,
            2
        )

    statistics_data = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high_priority,
        "completion_rate": completion_rate
    }

    return render_template(
        "statistics.html",
        statistics=statistics_data
    )


# ---------------------------------------------------------
# ERROR HANDLERS
# ---------------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "500.html"
    ), 500


# ---------------------------------------------------------
# CONTEXT PROCESSOR
# ---------------------------------------------------------

@app.context_processor
def inject_current_year():

    return {
        "current_year": datetime.now().year
    }


# ---------------------------------------------------------
# APPLICATION START
# ---------------------------------------------------------

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
