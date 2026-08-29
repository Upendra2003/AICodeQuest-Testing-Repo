from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# ============================================================
# Sample Data
# ============================================================

quizzes = [
    {
        "id": 1,
        "title": "Python Basics",
        "category": "Programming",
        "difficulty": "Easy",
        "duration": 10,
        "creator": "Admin",
        "questions": [
            {
                "id": 1,
                "question": "Which keyword is used to define a function?",
                "options": ["for", "while", "def", "class"],
                "answer": "def",
                "marks": 2
            },
            {
                "id": 2,
                "question": "Which data type stores True or False?",
                "options": ["int", "bool", "float", "list"],
                "answer": "bool",
                "marks": 2
            }
        ]
    },
    {
        "id": 2,
        "title": "Computer Networks",
        "category": "Networking",
        "difficulty": "Medium",
        "duration": 15,
        "creator": "Admin",
        "questions": [
            {
                "id": 3,
                "question": "Which protocol is used to transfer web pages?",
                "options": ["FTP", "HTTP", "SMTP", "SSH"],
                "answer": "HTTP",
                "marks": 2
            }
        ]
    }
]

results = []

next_quiz_id = 3
next_question_id = 4


# ============================================================
# Helper Functions
# ============================================================

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


def calculate_total_marks(quiz):

    total = 0

    for question in quiz["questions"]:
        total += question.get("marks", 1)

    return total


# ============================================================
# Home
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Online Quiz System",
        "status": "Running",
        "version": "2.0",
        "total_quizzes": len(quizzes),
        "total_attempts": len(results)
    })


# ============================================================
# Health Check
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "service": "quiz-api",
        "timestamp": datetime.now().isoformat()
    })


# ============================================================
# Get All Quizzes
# ============================================================

@app.route("/quizzes", methods=["GET"])
def all_quizzes():

    category = request.args.get("category")
    difficulty = request.args.get("difficulty")

    output = []

    for quiz in quizzes:

        if category:
            if quiz["category"].lower() != category.lower():
                continue

        if difficulty:
            if quiz["difficulty"].lower() != difficulty.lower():
                continue

        quiz_copy = quiz.copy()

        quiz_copy["question_count"] = len(
            quiz["questions"]
        )

        quiz_copy["total_marks"] = calculate_total_marks(
            quiz
        )

        output.append(quiz_copy)

    return jsonify({
        "count": len(output),
        "quizzes": output
    })


# ============================================================
# Get Single Quiz
# ============================================================

@app.route("/quizzes/<int:quiz_id>", methods=["GET"])
def single_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:
        return jsonify({
            "error": "Quiz not found"
        }), 404

    return jsonify(quiz)


# ============================================================
# Create Quiz
# ============================================================

@app.route("/quizzes", methods=["POST"])
def create_quiz():

    global next_quiz_id

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body is required"
        }), 400

    if "title" not in data:

        return jsonify({
            "error": "Title is required"
        }), 400

    title = data["title"].strip()

    if len(title) < 3:

        return jsonify({
            "error": "Title must contain at least 3 characters"
        }), 400

    difficulty = data.get(
        "difficulty",
        "Easy"
    )

    allowed_difficulty = [
        "Easy",
        "Medium",
        "Hard"
    ]

    if difficulty not in allowed_difficulty:

        return jsonify({
            "error": "Invalid difficulty",
            "allowed": allowed_difficulty
        }), 400

    duration = data.get(
        "duration",
        10
    )

    if duration <= 0:

        return jsonify({
            "error": "Duration must be greater than zero"
        }), 400

    quiz = {
        "id": next_quiz_id,
        "title": title,
        "category": data.get(
            "category",
            "General"
        ),
        "difficulty": difficulty,
        "duration": duration,
        "creator": data.get(
            "creator",
            "Unknown"
        ),
        "questions": []
    }

    quizzes.append(quiz)

    next_quiz_id += 1

    return jsonify({
        "message": "Quiz created successfully",
        "quiz": quiz
    }), 201


# ============================================================
# Update Quiz
# ============================================================

@app.route(
    "/quizzes/<int:quiz_id>",
    methods=["PUT"]
)
def update_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:

        return jsonify({
            "error": "Quiz not found"
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body is required"
        }), 400

    if "title" in data:
        quiz["title"] = data["title"]

    if "category" in data:
        quiz["category"] = data["category"]

    if "creator" in data:
        quiz["creator"] = data["creator"]

    if "duration" in data:

        if data["duration"] <= 0:

            return jsonify({
                "error": "Duration must be positive"
            }), 400

        quiz["duration"] = data["duration"]

    if "difficulty" in data:

        allowed = [
            "Easy",
            "Medium",
            "Hard"
        ]

        if data["difficulty"] not in allowed:

            return jsonify({
                "error": "Invalid difficulty"
            }), 400

        quiz["difficulty"] = data["difficulty"]

    return jsonify({
        "message": "Quiz updated successfully",
        "quiz": quiz
    })


# ============================================================
# Add Question
# ============================================================

@app.route(
    "/quizzes/<int:quiz_id>/questions",
    methods=["POST"]
)
def add_question(quiz_id):

    global next_question_id

    quiz = get_quiz(quiz_id)

    if quiz is None:

        return jsonify({
            "error": "Quiz not found"
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body is required"
        }), 400

    required = [
        "question",
        "options",
        "answer"
    ]

    for item in required:

        if item not in data:

            return jsonify({
                "error": f"{item} is required"
            }), 400

    if len(data["options"]) < 2:

        return jsonify({
            "error": "At least two options are required"
        }), 400

    if data["answer"] not in data["options"]:

        return jsonify({
            "error": "Answer must be one of the options"
        }), 400

    marks = data.get("marks", 1)

    if marks <= 0:

        return jsonify({
            "error": "Marks must be greater than zero"
        }), 400

    question = {
        "id": next_question_id,
        "question": data["question"],
        "options": data["options"],
        "answer": data["answer"],
        "marks": marks
    }

    quiz["questions"].append(question)

    next_question_id += 1

    return jsonify({
        "message": "Question added successfully",
        "question": question
    }), 201


# ============================================================
# Get Questions
# ============================================================

@app.route(
    "/quizzes/<int:quiz_id>/questions",
    methods=["GET"]
)
def get_questions(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:

        return jsonify({
            "error": "Quiz not found"
        }), 404

    questions = []

    for question in quiz["questions"]:

        safe_question = {
            "id": question["id"],
            "question": question["question"],
            "options": question["options"],
            "marks": question["marks"]
        }

        questions.append(safe_question)

    return jsonify({
        "quiz": quiz["title"],
        "count": len(questions),
        "questions": questions
    })


# ============================================================
# Random Question
# ============================================================

@app.route(
    "/quizzes/<int:quiz_id>/random-question",
    methods=["GET"]
)
def random_question(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:

        return jsonify({
            "error": "Quiz not found"
        }), 404

    if not quiz["questions"]:

        return jsonify({
            "error": "Quiz has no questions"
        }), 400

    question = random.choice(
        quiz["questions"]
    )

    return jsonify({
        "id": question["id"],
        "question": question["question"],
        "options": question["options"],
        "marks": question["marks"]
    })


# ============================================================
# Submit Quiz
# ============================================================

@app.route(
    "/quizzes/<int:quiz_id>/submit",
    methods=["POST"]
)
def submit_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:

        return jsonify({
            "error": "Quiz not found"
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body is required"
        }), 400

    user = data.get(
        "user",
        "Anonymous"
    )

    answers = data.get(
        "answers",
        {}
    )

    if not isinstance(answers, dict):

        return jsonify({
            "error": "Answers must be an object"
        }), 400

    score = 0
    total_marks = calculate_total_marks(
        quiz
    )

    correct_answers = 0
    incorrect_answers = 0

    details = []

    for question in quiz["questions"]:

        qid = str(question["id"])

        submitted_answer = answers.get(
            qid
        )

        correct = (
            submitted_answer ==
            question["answer"]
        )

        if correct:

            score += question["marks"]
            correct_answers += 1

        else:

            incorrect_answers += 1

        details.append({
            "question_id": question["id"],
            "submitted_answer": submitted_answer,
            "correct": correct
        })

    percentage = 0

    if total_marks > 0:

        percentage = round(
            score / total_marks * 100,
            2
        )

    passed = percentage >= 40

    result = {
        "user": user,
        "quiz": quiz["title"],
        "score": score,
        "total_marks": total_marks,
        "percentage": percentage,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "status": "Passed" if passed else "Failed",
        "submitted_at": datetime.now().isoformat(),
        "details": details
    }

    results.append(result)

    return jsonify(result)


# ============================================================
# User Results
# ============================================================

@app.route(
    "/results/<username>",
    methods=["GET"]
)
def user_results(username):

    user_results = []

    for result in results:

        if result["user"].lower() == username.lower():

            user_results.append(result)

    return jsonify({
        "user": username,
        "attempts": len(user_results),
        "results": user_results
    })


# ============================================================
# Leaderboard
# ============================================================

@app.route("/leaderboard")
def leaderboard():

    limit = request.args.get(
        "limit",
        default=10,
        type=int
    )

    if limit <= 0:

        return jsonify({
            "error": "Limit must be positive"
        }), 400

    sorted_results = sorted(
        results,
        key=lambda x: x["percentage"],
        reverse=True
    )

    leaderboard_data = []

    position = 1

    for result in sorted_results[:limit]:

        leaderboard_data.append({
            "rank": position,
            "user": result["user"],
            "quiz": result["quiz"],
            "percentage": result["percentage"],
            "status": result["status"]
        })

        position += 1

    return jsonify({
        "count": len(leaderboard_data),
        "leaderboard": leaderboard_data
    })


# ============================================================
# Quiz Statistics
# ============================================================

@app.route("/statistics")
def statistics():

    total_quizzes = len(quizzes)

    total_questions = 0
    total_marks = 0

    for quiz in quizzes:

        total_questions += len(
            quiz["questions"]
        )

        total_marks += calculate_total_marks(
            quiz
        )

    total_attempts = len(results)

    average_score = 0
    passed_attempts = 0
    failed_attempts = 0

    if total_attempts > 0:

        average_score = round(
            sum(
                r["percentage"]
                for r in results
            ) / total_attempts,
            2
        )

        for result in results:

            if result["status"] == "Passed":
                passed_attempts += 1
            else:
                failed_attempts += 1

    return jsonify({
        "quizzes": total_quizzes,
        "questions": total_questions,
        "available_marks": total_marks,
        "attempts": total_attempts,
        "average_percentage": average_score,
        "passed_attempts": passed_attempts,
        "failed_attempts": failed_attempts
    })


# ============================================================
# Search Quiz
# ============================================================

@app.route("/search")
def search():

    title = request.args.get(
        "title",
        ""
    ).lower()

    category = request.args.get(
        "category",
        ""
    ).lower()

    found = []

    for quiz in quizzes:

        title_match = (
            title in quiz["title"].lower()
        )

        category_match = True

        if category:

            category_match = (
                category
                in quiz["category"].lower()
            )

        if title_match and category_match:

            found.append(quiz)

    return jsonify({
        "query": title,
        "count": len(found),
        "results": found
    })


# ============================================================
# Delete Quiz
# ============================================================

@app.route(
    "/quizzes/<int:quiz_id>",
    methods=["DELETE"]
)
def delete_quiz(quiz_id):

    quiz = get_quiz(quiz_id)

    if quiz is None:

        return jsonify({
            "error": "Quiz not found"
        }), 404

    quizzes.remove(quiz)

    return jsonify({
        "message": "Quiz deleted successfully",
        "deleted_quiz": quiz["title"]
    })


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(404)
def page_not_found(e):

    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested resource does not exist"
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):

    return jsonify({
        "error": "HTTP method not allowed"
    }), 405


@app.errorhandler(500)
def internal_error(e):

    return jsonify({
        "error": "Internal server error"
    }), 500


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
