from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin with Firestore
cred = credentials.Certificate("private.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# FirestoreHelper class to manage Firestore operations
class FirestoreHelper:
    def __init__(self):
        self.db = db

    def assign_table(self, mac_address):
        try:
            # Query MAC address from /data/esp_mac/log/<MAC ID>
            mac_doc_ref = self.db.document(f"data/esp_mac/log/{mac_address}")
            mac_doc = mac_doc_ref.get()
            
            SECTOR_ID = "1.1" # Default sector_id for now

            # If MAC address doesn't exist, assign it to the next available tableID in the given sectorID
            sector_ref = self.db.collection(f"data/{SECTOR_ID}/esp")
            all_tables = list(sector_ref.stream())
            next_table_id = len(all_tables)
            
            # Save the new MAC address entry in /data/esp_mac/log
            mac_doc_ref.set({"sectorID": SECTOR_ID, "tableID": next_table_id})

            # Create the table entry under the sector
            sector_ref.document(str(next_table_id)).set({"mac": mac_address})

            return {"sector_id": SECTOR_ID, "table_id": next_table_id}
        
        except Exception as e:
            return {"error": str(e)}

    def save_esp_data(self, sector_id, table_id, data):
        try:
            doc_path = f"data/{sector_id}/esp/{table_id}"
            doc_ref = self.db.document(doc_path)
            doc_ref.set({"occupied": data}, merge=True)
            return {"message": f"Data saved to {doc_path}"}
        except Exception as e:
            print("Error", str(e))
            return {"error": str(e)}
        
    def save_model_data(self, sector_id, empty):
        try:
            doc_path = f"data/{sector_id}" 
            doc_ref = self.db.document(doc_path)
            doc_ref.set({"model": empty}, merge=True)
            
            print("Data saved to {doc_path}")
            return {"message": f"Data saved to {doc_path}"}
        except Exception as e:
            print("Error", str(e))
            return {"error": str(e)}

firestore_helper = FirestoreHelper()

# Root endpoint
@app.route("/", methods=["GET", "POST"])
def home():
    return "Hello, World!", 200

@app.route("/api/esp_data", methods=["POST"])
def add_data():
    try:
        data = request.json
        if not data or "MAC" not in data or "data" not in data:
            return jsonify({"error": "Invalid or missing data"}), 400
        
        mac_address = data["MAC"]
        value = data["data"]
        
        if data.get("sectorID"):
            sector_id = data["sectorID"]
            table_id = data["tableID"]
            save_result = firestore_helper.save_esp_data(sector_id,table_id, value)
            return jsonify({"message": "Data added successfully"}), 201
        
        table_assignment = firestore_helper.assign_table(mac_address)
        
        if "error" in table_assignment:
            return jsonify({"error": table_assignment["error"]}), 500

        save_result = firestore_helper.save_esp_data(
            table_assignment["sector_id"], table_assignment["table_id"],  value
        )

        return jsonify({"message": "Data added successfully", **table_assignment}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to add Model data
@app.route("/api/model", methods=["POST"])
def add_model():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid or missing data"}), 400

        sectorID = data.get("SectorID")
        empty = data.get("empty")
        
        if not empty:
            return jsonify({"error": "Invalid or missing data"}), 400
        
        model_result= firestore_helper.save_model_data(sectorID, empty)
        
        if "error" in model_result:
            print(model_result["error"])
            return jsonify({"error": model_result["error"]}), 500

        return jsonify(model_result), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
