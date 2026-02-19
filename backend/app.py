from flask import Flask, request, jsonify 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend Working!"

@app.route("/route", methods=["POST"])
def route():
    data = request.json

    start = data.get("start")
    end = data.get("end")
    friend = data.get("friend")

    return jsonify({
    "routes":[
        "Safest Route (well-lit streets)",
        "Fastest Route (shortest time)",
        "Balanced Route"
    ]
})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
