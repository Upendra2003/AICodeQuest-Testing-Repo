from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

students = [
    {
        "id": 1,
        "name": "Rahul",
        "department": "CSE",
        "year": 3,
        "attendance": []
    },
    {
        "id": 2,
        "name": "Priya",
        "department": "AIDS",
        "year": 2,
        "attendance": []
    },
    {
        "id": 3,
        "name": "Arjun",
        "department": "ECE",
        "year": 4,
        "attendance": []
    }
]

next_student_id = 4


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "application": "Student Attendance API",
        "status": "running",
        "version": "1.0"
    })


# --------------------------------------------------
# Get All Students
# --------------------------------------------------

@app.route("/students", methods=["GET"])
def get_students():

    return jsonify({
        "count": len(students),
        "students": students
    })


# --------------------------------------------------
# Get Student By ID
# --------------------------------------------------

@app.route("/students/<int:student_id>",
           methods=["GET"])
def get_student(student_id):

    for student in students:

        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({
        "error": "Student not found"
    }), 404


# --------------------------------------------------
# Add Student
# --------------------------------------------------

@app.route("/students", methods=["POST"])
def add_student():

    global next_student_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    name = data.get("name")
    department = data.get("department")
    year = data.get("year")

    if not name:
        return jsonify({
            "error": "Student name is required"
        }), 400

    if not department:
        return jsonify({
            "error": "Department is required"
        }), 400

    if year is None:
        return jsonify({
            "error": "Year is required"
        }), 400

    student = {
        "id": next_student_id,
        "name": name,
        "department": department,
        "year": year,
        "attendance": []
    }

    students.append(student)
    next_student_id += 1

    return jsonify({
        "message": "Student added successfully",
        "student": student
    }), 201


# --------------------------------------------------
# Delete Student
# --------------------------------------------------

@app.route("/students/<int:student_id>",
           methods=["DELETE"])
def delete_student(student_id):

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            return jsonify({
                "message": "Student deleted successfully"
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# --------------------------------------------------
# Search Students
# --------------------------------------------------

@app.route("/students/search")
def search_students():

    keyword = request.args.get("q", "").lower()

    if not keyword:
        return jsonify({
            "error": "Search keyword is required"
        }), 400

    results = []

    for student in students:

        name = student["name"].lower()
        department = student["department"].lower()

        if (
            keyword in name
            or keyword in department
        ):
            results.append(student)

    return jsonify({
        "query": keyword,
        "count": len(results),
        "results": results
    })


# --------------------------------------------------
# Mark Attendance
# --------------------------------------------------

@app.route("/attendance", methods=["POST"])
def mark_attendance():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    student_id = data.get("student_id")
    status = data.get("status")

    if student_id is None:
        return jsonify({
            "error": "Student ID is required"
        }), 400

    if status not in ["Present", "Absent"]:
        return jsonify({
            "error":
            "Status must be Present or Absent"
        }), 400

    for student in students:

        if student["id"] == student_id:

            record = {
                "date": datetime.now().strftime(
                    "%Y-%m-%d"
                ),
                "status": status
            }

            student["attendance"].append(record)

            return jsonify({
                "message":
                "Attendance marked successfully",
                "student": student
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# --------------------------------------------------
# Get Student Attendance
# --------------------------------------------------

@app.route(
    "/attendance/<int:student_id>",
    methods=["GET"]
)
def get_attendance(student_id):

    for student in students:

        if student["id"] == student_id:

            return jsonify({
                "student_id": student["id"],
                "student_name": student["name"],
                "attendance":
                    student["attendance"]
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# --------------------------------------------------
# Attendance Percentage
# --------------------------------------------------

@app.route(
    "/attendance/<int:student_id>/percentage",
    methods=["GET"]
)
def attendance_percentage(student_id):

    for student in students:

        if student["id"] == student_id:

            records = student["attendance"]

            if not records:
                return jsonify({
                    "student_id": student_id,
                    "percentage": 0
                })

            present = sum(
                1
                for record in records
                if record["status"] == "Present"
            )

            percentage = (
                present / len(records)
            ) * 100

            return jsonify({
                "student_id": student_id,
                "student_name":
                    student["name"],
                "total_days":
                    len(records),
                "present_days":
                    present,
                "attendance_percentage":
                    round(percentage, 2)
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# --------------------------------------------------
# Department Students
# --------------------------------------------------

@app.route(
    "/students/department/<department>",
    methods=["GET"]
)
def department_students(department):

    results = []

    for student in students:

        if (
            student["department"].lower()
            == department.lower()
        ):
            results.append(student)

    return jsonify({
        "department": department,
        "count": len(results),
        "students": results
    })


# --------------------------------------------------
# Attendance Summary
# --------------------------------------------------

@app.route("/attendance/summary",
           methods=["GET"])
def attendance_summary():

    total_present = 0
    total_absent = 0

    for student in students:

        for record in student["attendance"]:

            if record["status"] == "Present":
                total_present += 1

            elif record["status"] == "Absent":
                total_absent += 1

    total_records = (
        total_present + total_absent
    )

    percentage = 0

    if total_records > 0:
        percentage = (
            total_present / total_records
        ) * 100

    return jsonify({
        "total_students": len(students),
        "total_attendance_records":
            total_records,
        "present": total_present,
        "absent": total_absent,
        "overall_percentage":
            round(percentage, 2)
    })


# --------------------------------------------------
# Reset Student Attendance
# --------------------------------------------------

@app.route(
    "/attendance/<int:student_id>",
    methods=["DELETE"]
)
def reset_attendance(student_id):

    for student in students:

        if student["id"] == student_id:

            student["attendance"] = []

            return jsonify({
                "message":
                "Attendance records cleared"
            })

    return jsonify({
        "error": "Student not found"
    }), 404


# --------------------------------------------------
# API Information
# --------------------------------------------------

@app.route("/api/info")
def api_info():

    return jsonify({
        "name": "Student Attendance API",
        "endpoints": [
            "GET /",
            "GET /students",
            "GET /students/<id>",
            "POST /students",
            "DELETE /students/<id>",
            "GET /students/search?q=name",
            "POST /attendance",
            "GET /attendance/<id>",
            "GET /attendance/<id>/percentage",
            "GET /students/department/<department>",
            "GET /attendance/summary",
            "DELETE /attendance/<id>"
        ]
    })


# --------------------------------------------------
# Error Handlers
# --------------------------------------------------

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "error": "Method not allowed"
    }), 405


# --------------------------------------------------
# Start Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
