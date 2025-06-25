from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# Dodaj backend do path
sys.path.append('backend')
from database_utils import get_all, get_one

app = Flask(__name__)
CORS(app)

@app.route("/api/test")
def test():
    return jsonify({"status": "OK", "message": "Test endpoint works"})

@app.route("/api/test-db")
def test_db():
    try:
        result = get_one("SELECT 1 as test_value")
        return jsonify({"db_status": "OK", "result": result})
    except Exception as e:
        return jsonify({"db_status": "ERROR", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 