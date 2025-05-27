from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DATABASE_URL")

def get_all(query):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

@app.route("/")
def home():
    return "Backend działa!"

@app.route("/api/wyniki")
def wyniki():
    rows = get_all("""
        SELECT w.nr_startowy, w.czas_przejazdu_s, w.status, 
               z.imie, z.nazwisko, z.kategoria
        FROM wyniki w
        LEFT JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
        ORDER BY w.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/zawodnicy")
def zawodnicy():
    rows = get_all("SELECT * FROM zawodnicy ORDER BY nr_startowy")
    return jsonify(rows)

@app.route("/api/kategorie")
def kategorie():
    rows = get_all("SELECT DISTINCT kategoria FROM zawodnicy WHERE kategoria IS NOT NULL")
    return jsonify([row["kategoria"] for row in rows])

@app.route("/api/drabinka")
def drabinka():
    zawodnicy = get_all("SELECT nr_startowy, imie, nazwisko, kategoria FROM zawodnicy ORDER BY nr_startowy")
    matches = []
    for i in range(0, len(zawodnicy), 2):
        team1 = zawodnicy[i]
        team2 = zawodnicy[i+1] if i+1 < len(zawodnicy) else None
        matches.append({"team1": team1, "team2": team2})
    return jsonify(matches)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

