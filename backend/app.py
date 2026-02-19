from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def safety_score(distance, time, companion):
    score = 100

    score -= distance * 0.01

    if time == "night":
        score -= 20

    if companion == "alone":
        score -= 15
    elif companion == "female":
        score += 10
    elif companion == "male":
        score += 5

    return score


@app.route("/")
def home():
    return "Backend Working!"


@app.route("/route", methods=["POST"])
def route():
    data = request.json
    start = data["start"]
    end = data["end"]
    time = data["time"]
    companion = data["companion"]

    url = f"http://router.project-osrm.org/route/v1/foot/{start};{end}?alternatives=true&overview=false"

    res = requests.get(url).json()

    best = None
    best_score = -999

    for r in res["routes"]:
        dist = r["distance"]
        score = safety_score(dist, time, companion)

        if score > best_score:
            best_score = score
            best = r

    return jsonify({
        "best_distance": best["distance"],
        "score": best_score
    })


if __name__ == "__main__":
    app.run()
