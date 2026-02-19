from flask import Flask, request, jsonify

app = Flask(__name__)

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
        "route": f"Safe route from {start} to {end} (traveling {friend})"
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
