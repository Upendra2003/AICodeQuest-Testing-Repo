from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

movies = [
    {
        "id": 1,
        "title": "Inception",
        "genre": "Sci-Fi",
        "year": 2010,
        "rating": 9.0,
        "watched": True,
        "added_on": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "id": 2,
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "year": 2014,
        "rating": 9.5,
        "watched": False,
        "added_on": datetime.now().strftime("%Y-%m-%d")
    }
]

next_id = 3


def find_movie(movie_id):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None


@app.route("/")
def home():
    return jsonify({
        "application": "Movie Collection API",
        "version": "1.0",
        "movies": len(movies)
    })


@app.route("/movies", methods=["GET"])
def get_movies():
    return jsonify(movies)


@app.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = find_movie(movie_id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify(movie)


@app.route("/movies", methods=["POST"])
def add_movie():
    global next_id

    data = request.get_json()

    required = ["title", "genre", "year", "rating"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    movie = {
        "id": next_id,
        "title": data["title"],
        "genre": data["genre"],
        "year": data["year"],
        "rating": data["rating"],
        "watched": False,
        "added_on": datetime.now().strftime("%Y-%m-%d")
    }

    movies.append(movie)
    next_id += 1

    return jsonify(movie), 201


@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):

    movie = find_movie(movie_id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    data = request.get_json()

    movie["title"] = data.get("title", movie["title"])
    movie["genre"] = data.get("genre", movie["genre"])
    movie["year"] = data.get("year", movie["year"])
    movie["rating"] = data.get("rating", movie["rating"])

    return jsonify(movie)


@app.route("/movies/<int:movie_id>/watch", methods=["PATCH"])
def mark_watched(movie_id):

    movie = find_movie(movie_id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    movie["watched"] = True

    return jsonify({
        "message": "Movie marked as watched",
        "movie": movie
    })


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):

    movie = find_movie(movie_id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    movies.remove(movie)

    return jsonify({
        "message": "Movie deleted successfully"
    })


@app.route("/movies/search")
def search_movie():

    keyword = request.args.get("title", "").lower()

    result = []

    for movie in movies:
        if keyword in movie["title"].lower():
            result.append(movie)

    return jsonify(result)


@app.route("/movies/genre/<genre>")
def movies_by_genre(genre):

    result = []

    for movie in movies:
        if movie["genre"].lower() == genre.lower():
            result.append(movie)

    return jsonify(result)


@app.route("/movies/top-rated")
def top_rated():

    if not movies:
        return jsonify([])

    highest = max(movie["rating"] for movie in movies)

    result = []

    for movie in movies:
        if movie["rating"] == highest:
            result.append(movie)

    return jsonify(result)


@app.route("/statistics")
def statistics():

    total = len(movies)
    watched = 0
    total_rating = 0

    genres = {}

    for movie in movies:

        if movie["watched"]:
            watched += 1

        total_rating += movie["rating"]

        genre = movie["genre"]

        if genre in genres:
            genres[genre] += 1
        else:
            genres[genre] = 1

    average_rating = 0

    if total > 0:
        average_rating = round(total_rating / total, 2)

    return jsonify({
        "total_movies": total,
        "watched_movies": watched,
        "unwatched_movies": total - watched,
        "average_rating": average_rating,
        "genre_distribution": genres
    })


@app.route("/recommendations")
def recommendations():

    recommendations = []

    for movie in movies:
        if movie["rating"] >= 8.5 and not movie["watched"]:
            recommendations.append(movie)

    return jsonify(recommendations)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal Server Error"
    }), 500


@app.before_request
def before_request():
    print(f"Incoming Request: {request.method} {request.path}")


@app.after_request
def after_request(response):
    response.headers["X-Powered-By"] = "Flask Movie API"
    return response


if __name__ == "__main__":
    app.run(debug=True)
