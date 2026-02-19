from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)

# ===== Crime data =====
with open("backend/crime_data.json") as f:
    CRIME_DATA = json.load(f)

# ===== USERS =====
users={"tanmay":"1234"}

@app.route("/")
def home():
    return "Women Safety Route Finder Backend Running!"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if users.get(data["user"])==data["pass"]:
        return jsonify({"status":"ok"})
    return jsonify({"status":"fail"})

# ===== SAFETY SCORE =====
def safety_score(friend, time_of_day, area_type, start):
    score = 70
    if friend=="alone": score-=20
    if friend=="female": score+=10
    if friend=="male": score+=5

    if time_of_day=="night": score-=15
    if area_type=="main_road": score+=10
    if area_type=="isolated": score-=20

    # City crime adjustment
    city_score = CRIME_DATA.get(start.split()[0],70)
    score = (score+city_score)//2
    return max(0,min(100,score))

@app.route("/route", methods=["POST"])
def route():
    data = request.json
    start = data.get("start","Unknown")
    end = data.get("end","Unknown")
    friend = data.get("friend","alone")

    time_of_day = random.choice(["day","night"])
    area_type = random.choice(["main_road","isolated"])

    score = safety_score(friend,time_of_day,area_type,start)

    routes = [
        {"name":"Safest Route","info":"Well-lit main roads","score":score},
        {"name":"Fastest Route","info":"Shortest time","score":max(0,score-10)},
        {"name":"Balanced Route","info":"Balanced safety+speed","score":max(0,score-5)}
    ]

    crime_alert = f"{start}: {random.choice(['No recent crimes','Minor incident reported','Crowded area caution'])}"

    return jsonify({
        "start": start,
        "end": end,
        "routes": routes,
        "ai_note": f"Traveling {friend}, {time_of_day} time, {area_type} area",
        "crime_alert": crime_alert
    })

# ===== PANIC SIMULATION =====
@app.route("/panic", methods=["POST"])
def panic():
    data = request.json
    location = data.get("location","Unknown")
    return jsonify({"msg":f"Emergency alert sent for location {location}"})

if __name__=="__main__":
    import os
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
