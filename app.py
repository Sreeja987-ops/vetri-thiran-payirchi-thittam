from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from gemini_utils import get_home_plan, get_party_plan, get_jewelry_plan

app = Flask(__name__)
CORS(app)

# Create uploads folder
os.makedirs("static/uploads", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html") if os.path.exists("templates/index.html") else jsonify({"message": "PocketSmart AI Running"})

@app.route("/generate-home", methods=["POST"])
def generate_home():
    data = request.get_json()
    budget = data.get("budget", "10000")
    style = data.get("style", "modern")
    room_details = data.get("room_details", "")
    result = get_home_plan(budget, style, room_details)
    return jsonify({"result": result})

@app.route("/generate-party", methods=["POST"])
def generate_party():
    data = request.get_json()
    event_type = data.get("event_type", "birthday")
    budget = data.get("budget", "5000")
    guests = data.get("guests", 10)
    result = get_party_plan(event_type, budget, guests)
    return jsonify({"result": result})

@app.route("/generate-jewelry", methods=["POST"])
def generate_jewelry():
    data = request.get_json()
    budget = data.get("budget", "5000")
    occasion = data.get("occasion", "wedding")
    outfit = data.get("outfit", "")
    
    # Image upload support
    image_path = None
    if 'outfit_image' in request.files:
        file = request.files['outfit_image']
        if file.filename:
            image_path = os.path.join("static/uploads", file.filename)
            file.save(image_path)
    
    result = get_jewelry_plan(outfit, budget, occasion, image_path)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
