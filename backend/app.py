from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)


# ===== HOME =====
@app.route("/")
def home():
    return "Women Safety Route Finder Backend Running!"


# ===== SAFETY SCORE LOGIC =====
def safety_score(friend, time_of_day, area_type):
    score = 70

    # Traveling alone
    if friend == "alone":
        score -= 20
    elif friend == "female":
        score += 10
    elif friend == "male":
        score += 5

    # Night time
    if time_of_day == "night":
        score -= 15

    # Area type
    if area_type == "main_road":
        score += 10
    elif area_type == "isolated":
        score -= 20

    # Keep between 0-100
    return max(0, min(100, score))


# ===== ROUTE FINDER =====
@app.route("/route", methods=["POST"])
def route():

    data = request.json

    start = data.get("start", "Unknown")
    end = data.get("end", "Unknown")
    friend = data.get("friend", "alone")

    # Simulated AI info
    time_of_day = random.choice(["day", "night"])
    area_type = random.choice(["main_road", "isolated"])

    score = safety_score(friend, time_of_day, area_type)

    routes = [
        {
            "name": "Safest Route",
            "info": "Well-lit main roads",
            "score": score
        },
        {
            "name": "Fastest Route",
            "info": "Shortest time",
            "score": score - 10
        },
        {
            "name": "Balanced Route",
            "info": "Good safety + speed",
            "score": score - 5
        }
    ]

    return jsonify({
        "start": start,
        "end": end,
        "routes": routes,
        "ai_note": f"Traveling {friend}, {time_of_day} time, {area_type} detected"
    })


# ===== RUN SERVER =====
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
