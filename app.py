from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  
SPREADSHEET_TITLE = "QR Code Links"  
WORKSHEET_NAME = "Sheet1"

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(credentials)
sheet = client.open(SPREADSHEET_TITLE).worksheet(WORKSHEET_NAME)

@app.route("/api/save", methods=["POST"])
def save_data():
    try:
        data = request.get_json()
        asn = data.get("asn")
        affiliate = data.get("affiliate")
        client_short = data.get("client")

        if not all([asn, affiliate, client_short]):
            return jsonify({"error": "Missing required fields"}), 400

        timestamp = datetime.utcnow().isoformat()
        sheet.append_row([asn, affiliate, client_short, timestamp])

        print("✅ Data saved to Google Sheet")
        return jsonify({"success": True}), 200

    except Exception as e:
        print("❌ Error saving to Google Sheet:", e)
        return jsonify({"error": str(e)}), 500

from flask import jsonify

@app.get("/")
def index():
    return "QR backend is running", 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

from flask import Flask, request, jsonify  # you already have this import
# ...

@app.get("/")
def index():
    return "QR backend is running", 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)
