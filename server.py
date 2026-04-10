from flask import Flask, request, jsonify, render_template
import os
import json
import time
import random
import string
from datetime import datetime
app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "appointments.json")

os.makedirs(DATA_DIR, exist_ok=True)

# Load data
def load():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# Save data
def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

# Generate ID
def gen_id():
    return str(int(time.time())) + "-" + "".join(random.choices(string.ascii_lowercase, k=4))

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# API to save appointment
@app.route("/api/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    db = load()

    data["id"] = gen_id()
    data["created"] = datetime.now().isoformat()

    db.append(data)
    save(db)

    return jsonify({"success": True})

# Admin page (Doctor view)
@app.route("/admin")
def admin():
    data = load()
    return render_template("admin.html", data=data)

# Run server
if __name__ == "__main__":
    print("Server running → http://localhost:8080")
    app.run(debug=True)