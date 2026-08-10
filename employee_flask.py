from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------------------
# Employee Data
# -----------------------------------------

employees = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "department": "Engineering",
        "position": "Software Engineer",
        "salary": 75000
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "department": "HR",
        "position": "HR Manager",
        "salary": 65000
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "department": "Engineering",
        "position": "Senior Developer",
        "salary": 95000
    }
]

next_employee_id = 4


# -----------------------------------------
# Helper Function
# -----------------------------------------

def find_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


# -----------------------------------------
# Home Endpoint
# -----------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "application": "Employee Management REST API",
        "version": "1.0",
        "status": "running"
    })


# -----------------------------------------
# Get All Employees
# -----------------------------------------

@app.route("/employees", methods=["GET"])
def get_employees():

    return jsonify({
        "count": len(employees),
        "employees": employees
    })


# -----------------------------------------
# Get Employee By ID
# -----------------------------------------

@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):

    employee = find_employee(employee_id)

    if employee is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    return jsonify(employee)


# -----------------------------------------
# Create New Employee
# -----------------------------------------

@app.route("/employees", methods=["POST"])
def create_employee():

    global next_employee_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    required_fields = [
        "name",
        "department",
        "position",
        "salary"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    employee = {
        "id": next_employee_id,
        "name": data["name"],
        "department": data["department"],
        "position": data["position"],
        "salary": data["salary"]
    }

    employees.append(employee)

    next_employee_id += 1

    return jsonify({
        "message": "Employee created successfully",
        "employee": employee
    }), 201


# -----------------------------------------
# Update Employee
# -----------------------------------------

@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):

    employee = find_employee(employee_id)

    if employee is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    employee["name"] = data.get(
        "name",
        employee["name"]
    )

    employee["department"] = data.get(
        "department",
        employee["department"]
    )

    employee["position"] = data.get(
        "position",
        employee["position"]
    )

    employee["salary"] = data.get(
        "salary",
        employee["salary"]
    )

    return jsonify({
        "message": "Employee updated successfully",
        "employee": employee
    })


# -----------------------------------------
# Delete Employee
# -----------------------------------------

@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):

    employee = find_employee(employee_id)

    if employee is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    employees.remove(employee)

    return jsonify({
        "message": "Employee deleted successfully",
        "employee_id": employee_id
    })


# -----------------------------------------
# Search Employees
# -----------------------------------------

@app.route("/employees/search", methods=["GET"])
def search_employees():

    name = request.args.get("name", "")

    if not name:
        return jsonify({
            "error": "name parameter is required"
        }), 400

    name = name.lower()

    results = []

    for employee in employees:

        if name in employee["name"].lower():
            results.append(employee)

    return jsonify({
        "count": len(results),
        "employees": results
    })


# -----------------------------------------
# Filter By Department
# -----------------------------------------

@app.route("/departments/<department>", methods=["GET"])
def employees_by_department(department):

    results = []

    for employee in employees:

        if employee["department"].lower() == department.lower():
            results.append(employee)

    return jsonify({
        "department": department,
        "count": len(results),
        "employees": results
    })


# -----------------------------------------
# Get Highest Paid Employee
# -----------------------------------------

@app.route("/employees/highest-paid", methods=["GET"])
def highest_paid():

    if len(employees) == 0:
        return jsonify({
            "error": "No employees available"
        }), 404

    highest = employees[0]

    for employee in employees:

        if employee["salary"] > highest["salary"]:
            highest = employee

    return jsonify(highest)


# -----------------------------------------
# Salary Statistics
# -----------------------------------------

@app.route("/statistics/salary", methods=["GET"])
def salary_statistics():

    if len(employees) == 0:
        return jsonify({
            "error": "No employees available"
        }), 404

    total_salary = 0

    for employee in employees:
        total_salary += employee["salary"]

    average_salary = total_salary / len(employees)

    return jsonify({
        "total_employees": len(employees),
        "total_salary": total_salary,
        "average_salary": round(average_salary, 2)
    })


# -----------------------------------------
# Department Statistics
# -----------------------------------------

@app.route("/statistics/departments", methods=["GET"])
def department_statistics():

    departments = {}

    for employee in employees:

        department = employee["department"]

        if department not in departments:
            departments[department] = 0

        departments[department] += 1

    return jsonify({
        "departments": departments
    })


# -----------------------------------------
# Increase Salary
# -----------------------------------------

@app.route(
    "/employees/<int:employee_id>/salary",
    methods=["PATCH"]
)
def increase_salary(employee_id):

    employee = find_employee(employee_id)

    if employee is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    data = request.get_json()

    if not data or "percentage" not in data:
        return jsonify({
            "error": "percentage is required"
        }), 400

    percentage = data["percentage"]

    if percentage < 0:
        return jsonify({
            "error": "Percentage cannot be negative"
        }), 400

    old_salary = employee["salary"]

    increase = old_salary * percentage / 100

    employee["salary"] = old_salary + increase

    return jsonify({
        "message": "Salary updated successfully",
        "old_salary": old_salary,
        "new_salary": employee["salary"]
    })


# -----------------------------------------
# API Information
# -----------------------------------------

@app.route("/api/info", methods=["GET"])
def api_info():

    return jsonify({
        "name": "Employee Management API",
        "version": "1.0",
        "available_operations": [
            "Create employee",
            "Read employee",
            "Update employee",
            "Delete employee",
            "Search employee",
            "Department filtering",
            "Salary statistics"
        ]
    })


# -----------------------------------------
# Error Handling
# -----------------------------------------

@app.errorhandler(404)
def handle_not_found(error):

    return jsonify({
        "error": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):

    return jsonify({
        "error": "HTTP method is not allowed"
    }), 405


@app.errorhandler(500)
def handle_server_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500


# -----------------------------------------
# Start Application
# -----------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
