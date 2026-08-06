from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# -------------------------------
# Sample Data
# -------------------------------

quizzes = [
    {
        "id": 1,
        "title": "Python Basics",
        "category": "Programming",
        "questions": [
            {
                "id": 1,
                "question": "Which keyword is used to define a function?",
                "options": ["for", "while", "def", "class"],
                "answer": "def"
            },
            {
                "id": 2,
                "question": "Which data type stores True or False?",
                "options": ["int", "bool", "float", "list"],
                "answer": "bool"
            }
        ]
    }
]

results = []

next_quiz_id = 2
next_question_id = 3


# -------------------------------
# Helper Functions
# -------------------------------

def get_quiz(quiz_id):
    for quiz in quizzes:
        if quiz["id"] == quiz_id:
            return quiz
    return None


def get_question(quiz, question_id):
    for question in quiz["questions"]:
        if question["id"] == question_id:
            return question
    return None


# -------------------------------
# Home
# -------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Online Quiz System",
        "status": "Running",
        "quizzes": len(quizzes)
    })


# -------------------------------
# Get All Quizzes
# -------------------------------

@app.route("/quizzes", methods=["GET"])
def all_quizzes():
    return jsonify(quizzes)


# -------------------------------
# Get Single Quiz
# -------------------------------

@app.route("/quizzes/<int:quiz_id>", methods=["GET"])
def single_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify(quiz)


# -------------------------------
# Create Quiz
# -------------------------------

@app.route("/quizzes", methods=["POST"])
def create_quiz():

    global next_quiz_id

    data = request.get_json()

    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    quiz = {
        "id": next_quiz_id,
        "title": data["title"],
        "category": data.get("category", "General"),
        "questions": []
    }

    quizzes.append(quiz)

    next_quiz_id += 1

    return jsonify(quiz), 201


# -------------------------------
# Add Question
# -------------------------------

@app.route("/quizzes/<int:quiz_id>/questions", methods=["POST"])
def add_question(quiz_id):

    global next_question_id

    quiz = get_quiz(quiz_id)

    if quiz is None:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.get_json()

    required = ["question", "options", "answer"]

    for item in required:
        if item not in data:
            return jsonify({"error": f"{item} is required"}), 400

    question = {
        "id": next_question_id,
        "question": data["question"],
        "options": data["options"],
        "answer": data["answer"]
    }

    quiz["questions"].append(question)

    next_question_id += 1

    return jsonify(question), 201


# -------------------------------
# Submit Quiz
# -------------------------------

@app.route("/quizzes/<int:quiz_id>/submit", methods=["POST"])
def submit_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.get_json()

    user = data.get("user")

    answers = data.get("answers", {})

    score = 0

    total = len(quiz["questions"])

    for question in quiz["questions"]:

        qid = str(question["id"])

        if qid in answers:

            if answers[qid] == question["answer"]:
                score += 1

    percentage = 0

    if total > 0:
        percentage = round(score / total * 100, 2)

    result = {
        "user": user,
        "quiz": quiz["title"],
        "score": score,
        "total": total,
        "percentage": percentage,
        "submitted_at": datetime.now().isoformat()
    }

    results.append(result)

    return jsonify(result)


# -------------------------------
# Leaderboard
# -------------------------------

@app.route("/leaderboard")
def leaderboard():

    sorted_results = sorted(
        results,
        key=lambda x: x["percentage"],
        reverse=True
    )

    return jsonify(sorted_results)


# -------------------------------
# Quiz Statistics
# -------------------------------

@app.route("/statistics")
def statistics():

    total_quizzes = len(quizzes)

    total_questions = 0

    for quiz in quizzes:
        total_questions += len(quiz["questions"])

    total_attempts = len(results)

    average_score = 0

    if total_attempts > 0:
        average_score = round(
            sum(r["percentage"] for r in results) / total_attempts,
            2
        )

    return jsonify({
        "quizzes": total_quizzes,
        "questions": total_questions,
        "attempts": total_attempts,
        "average_percentage": average_score
    })


# -------------------------------
# Search Quiz
# -------------------------------

@app.route("/search")
def search():

    title = request.args.get("title", "").lower()

    found = []

    for quiz in quizzes:

        if title in quiz["title"].lower():
            found.append(quiz)

    return jsonify(found)


# -------------------------------
# Delete Quiz
# -------------------------------

@app.route("/quizzes/<int:quiz_id>", methods=["DELETE"])
def delete_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:
        return jsonify({"error": "Quiz not found"}), 404

    quizzes.remove(quiz)

    return jsonify({
        "message": "Quiz deleted successfully"
    })


# -------------------------------
# Error Handlers
# -------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error"
    }), 500


# -------------------------------
# Run Application
# -------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
