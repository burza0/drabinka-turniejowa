from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/test")
def test():
    return jsonify({"status": "OK", "message": "Minimal test works"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 