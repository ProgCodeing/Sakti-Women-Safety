from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def safety_score(distance, time, companion):
    score = 100

    # Distance penalty
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

    url = f"http://router.project-osrm.org/route/v1/foot/{start};{end}?alternatives=true&overview=full&geometries=geojson"

    res = requests.get(url).json()

    best_route = None
    best_score = -999

    for r in res["routes"]:
        dist = r["distance"]
        score = safety_score(dist, time, companion)

        if score > best_score:
            best_score = score
            best_route = r

    return jsonify({
        "geometry": best_route["geometry"],
        "score": best_score,
        "distance": best_route["distance"]
    })


if __name__ == "__main__":
    app.run()
