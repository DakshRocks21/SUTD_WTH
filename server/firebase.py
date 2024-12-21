from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate("private.json")
firebase_admin.initialize_app(cred)

# Root endpoint
@app.route("/", methods=["GET", "POST"])
def home():
    return "Hello, World!", 200
    

@app.route("/api/esp_data", methods=["POST"])
def add_data():
    print(request.json)
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid or missing data"}), 400
        
        # Push data to Firebase under "esp_data" node
        #/data/()
        
        return jsonify({"message": "Data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to add Model data
@app.route("/api/model", methods=["POST"])
def add_model():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid or missing data"}), 400

        # Push data to Firebase under "model" node
        ref = db.reference('model')
        ref.push(data)

        return jsonify({"message": "Model data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
