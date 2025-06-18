from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


DB_FILE = "qrdata.db"

# Create DB and table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asn TEXT NOT NULL,
            affiliate TEXT NOT NULL,
            client TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/api/save", methods=["POST"])
def save_data():
    try:
        data = request.get_json()
        print("📦 Received data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        asn = data.get("asn")
        affiliate = data.get("affiliate")
        client = data.get("client")

        if not all([asn, affiliate, client]):
            return jsonify({"error": "Missing required fields"}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO qr_codes (asn, affiliate, client) VALUES (?, ?, ?)",
                       (asn, affiliate, client))
        conn.commit()
        conn.close()

        print("✅ Data saved to database")
        return jsonify({"success": True}), 200

    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    print("🔥 Flask is starting...")
    app.run(debug=True, port=5050)

