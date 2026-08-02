from flask import Flask, request, jsonify
from datetime import datetime
import statistics

app = Flask(__name__)

# -----------------------------
# Sample Data
# -----------------------------
students = [
    {
        "id": 1,
        "name": "Alice",
        "age": 20,
        "department": "Computer Science",
        "marks": [85, 90, 88],
        "joined": "2025-08-10"
    },
    {
        "id": 2,
        "name": "Bob",
        "age": 21,
        "department": "Mechanical",
        "marks": [75, 80, 78],
        "joined": "2025-09-01"
    }
]

next_student_id = 3


# -----------------------------
# Utility Functions
# -----------------------------
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def calculate_average(marks):
    if not marks:
        return 0
    return round(sum(marks) / len(marks), 2)


def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    else:
        return "D"


# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "application": "Student Management System",
        "version": "2.0",
        "time": datetime.now().isoformat()
    })


# -----------------------------
# List Students
# -----------------------------
@app.route("/students", methods=["GET"])
def list_students():
    return jsonify(students)


# -----------------------------
# Get Student
# -----------------------------
@app.route("/students/<int:student_id>", methods=["GET"])
def student_details(student_id):
    student = get_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    average = calculate_average(student["marks"])
    grade = calculate_grade(average)

    result = dict(student)
    result["average"] = average
    result["grade"] = grade

    return jsonify(result)


# -----------------------------
# Add Student
# -----------------------------
@app.route("/students", methods=["POST"])
def add_student():
    global next_student_id

    data = request.get_json()

    required = ["name", "age", "department"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_student = {
        "id": next_student_id,
        "name": data["name"],
        "age": data["age"],
        "department": data["department"],
        "marks": data.get("marks", []),
        "joined": datetime.now().strftime("%Y-%m-%d")
    }

    students.append(new_student)
    next_student_id += 1

    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201


# -----------------------------
# Update Student
# -----------------------------
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = get_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    student["name"] = data.get("name", student["name"])
    student["age"] = data.get("age", student["age"])
    student["department"] = data.get("department", student["department"])

    return jsonify(student)


# -----------------------------
# Delete Student
# -----------------------------
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = get_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    students.remove(student)

    return jsonify({
        "message": "Student removed successfully"
    })


# -----------------------------
# Add Marks
# -----------------------------
@app.route("/students/<int:student_id>/marks", methods=["POST"])
def add_marks(student_id):
    student = get_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()

    mark = data.get("mark")

    if mark is None:
        return jsonify({"error": "mark is required"}), 400

    student["marks"].append(mark)

    return jsonify({
        "message": "Mark added",
        "marks": student["marks"]
    })


# -----------------------------
# Department Report
# -----------------------------
@app.route("/departments/<department>", methods=["GET"])
def department_report(department):

    filtered = [
        student
        for student in students
        if student["department"].lower() == department.lower()
    ]

    return jsonify({
        "department": department,
        "count": len(filtered),
        "students": filtered
    })


# -----------------------------
# Statistics
# -----------------------------
@app.route("/statistics", methods=["GET"])
def statistics_page():

    all_marks = []

    for student in students:
        all_marks.extend(student["marks"])

    if all_marks:
        stats = {
            "highest": max(all_marks),
            "lowest": min(all_marks),
            "average": round(statistics.mean(all_marks), 2),
            "total_marks": len(all_marks)
        }
    else:
        stats = {
            "highest": 0,
            "lowest": 0,
            "average": 0,
            "total_marks": 0
        }

    return jsonify(stats)


# -----------------------------
# Search Student
# -----------------------------
@app.route("/search")
def search_student():

    keyword = request.args.get("name", "").lower()

    result = [
        student
        for student in students
        if keyword in student["name"].lower()
    ]

    return jsonify(result)


# -----------------------------
# Server Information
# -----------------------------
@app.route("/server")
def server():

    return jsonify({
        "framework": "Flask",
        "python": "3.x",
        "status": "Running",
        "students": len(students),
        "current_time": datetime.now().isoformat()
    })


# -----------------------------
# Error Handling
# -----------------------------
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "message": "Resource not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "message": "Internal server error"
    }), 500


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
