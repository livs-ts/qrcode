from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import traceback
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# --- Google Sheets config ---
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  # Make sure this exists on Render

SHEET_ID = "1nF_L4iCsf5IBz8XnxcJAqLa9kWN6hgsFrfBMhL5oEC0"  # Your sheet ID
SHEET_TAB = "Sheet1"  # Tab name exactly as in the sheet

# Google Sheets client
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
gclient = gspread.authorize(credentials)

def get_ws():
    """Return the worksheet handle by sheet ID and tab name."""
    return gclient.open_by_key(SHEET_ID).worksheet(SHEET_TAB)

@app.post("/api/save")
def save_data():
    try:
        data = request.get_json(force=True) or {}
        print("📦 Received data:", data)

        asn = data.get("asn")
        affiliate = data.get("affiliate")
        client_short = data.get("client")

        if not all([asn, affiliate, client_short]):
            return jsonify(error="Missing required fields"), 400

        ws = get_ws()
        timestamp = datetime.utcnow().isoformat()
        ws.append_row([asn, affiliate, client_short, timestamp])

        print("✅ Appended to Google Sheet")
        return jsonify(success=True), 200

    except Exception as e:
        print("❌ Error saving to Google Sheet:", e)
        traceback.print_exc()
        return jsonify(error=str(e)), 500

@app.get("/")
def index():
    return "QR backend is running", 200

@app.get("/health")
def health():
    # Confirm which sheet we're using
    return jsonify(status="ok", sheet_id=SHEET_ID, sheet_tab=SHEET_TAB), 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)
