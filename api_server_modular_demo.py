"""
SKATECROSS QR System - Modular Architecture Demo (v32.0 Style)
Demonstracja modułowej struktury - wszystkie "moduły" w jednym pliku dla testów
"""

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
import qrcode
import base64
import io
from datetime import datetime

# ================== UTILS/DATABASE MODULE (Pseudo) ==================
print("📦 Ładuję utils/database.py...")

# Dane demo (normalnie byłoby w utils/database.py)
zawodnicy_data = [
    {"nr_startowy": 1, "imie": "Jan", "nazwisko": "Kowalski", "kategoria": "Senior", "plec": "M", "klub": "KTH Krynica", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 2, "imie": "Anna", "nazwisko": "Nowak", "kategoria": "Senior", "plec": "K", "klub": "UKS Boots", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 3, "imie": "Piotr", "nazwisko": "Wiśniewski", "kategoria": "Junior", "plec": "M", "klub": "KTH Krynica", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 4, "imie": "Maria", "nazwisko": "Wójcik", "kategoria": "Junior", "plec": "K", "klub": "UKS Boots", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 5, "imie": "Tomasz", "nazwisko": "Kowalczyk", "kategoria": "Senior", "plec": "M", "klub": "SKL Zakopane", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 6, "imie": "Katarzyna", "nazwisko": "Dąbrowska", "kategoria": "Junior", "plec": "K", "klub": "Roller Team", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 7, "imie": "Michał", "nazwisko": "Lewandowski", "kategoria": "Senior", "plec": "M", "klub": "Speed Demons", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 8, "imie": "Agnieszka", "nazwisko": "Zielińska", "kategoria": "Senior", "plec": "K", "klub": "Roller Team", "qr_code": None, "checked_in": False, "check_in_time": None},
]

grupy_startowe_data = [
    {"kategoria": "Senior", "plec": "M", "numer_grupy": 1, "nazwa": "Senior Mężczyźni", "status": "WAITING"},
    {"kategoria": "Senior", "plec": "K", "numer_grupy": 2, "nazwa": "Senior Kobiety", "status": "WAITING"},
    {"kategoria": "Junior", "plec": "M", "numer_grupy": 3, "nazwa": "Junior Mężczyźni", "status": "WAITING"},
    {"kategoria": "Junior", "plec": "K", "numer_grupy": 4, "nazwa": "Junior Kobiety", "status": "WAITING"},
]

# Funkcje utils (normalnie w utils/database.py)
def find_zawodnik_by_nr(nr_startowy):
    for zawodnik in zawodnicy_data:
        if zawodnik["nr_startowy"] == nr_startowy:
            return zawodnik
    return None

def update_zawodnik_qr(nr_startowy, qr_code):
    zawodnik = find_zawodnik_by_nr(nr_startowy)
    if zawodnik:
        zawodnik["qr_code"] = qr_code
        return True
    return False

def checkin_zawodnik(nr_startowy):
    zawodnik = find_zawodnik_by_nr(nr_startowy)
    if zawodnik:
        zawodnik["checked_in"] = True
        zawodnik["check_in_time"] = datetime.now().isoformat()
        return True
    return False

# ================== API/ZAWODNICY MODULE (Pseudo) ==================
print("📦 Ładuję api/zawodnicy.py...")

zawodnicy_bp = Blueprint('zawodnicy', __name__)

@zawodnicy_bp.route("/api/zawodnicy")
def get_zawodnicy():
    """Endpoint zawodników z api/zawodnicy.py"""
    return jsonify(zawodnicy_data)

# ================== API/QR_GENERATION MODULE (Pseudo) ==================
print("📦 Ładuję api/qr_generation.py...")

qr_generation_bp = Blueprint('qr_generation', __name__)

@qr_generation_bp.route("/api/qr/generate/<int:nr_startowy>", methods=['POST'])
def qr_generate_for_zawodnik(nr_startowy):
    """QR Generation z api/qr_generation.py"""
    try:
        zawodnik = find_zawodnik_by_nr(nr_startowy)
        if not zawodnik:
            return jsonify({"error": "Zawodnik nie istnieje"}), 404
        
        qr_data = f"SKATECROSS_QR_{nr_startowy}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        update_zawodnik_qr(nr_startowy, qr_data)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "qr_code": qr_data,
            "qr_image": f"data:image/png;base64,{img_str}",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd generowania QR: {str(e)}"
        }), 500

@qr_generation_bp.route("/api/qr/stats")
def qr_stats():
    """Statystyki QR z api/qr_generation.py"""
    total = len(zawodnicy_data)
    z_qr = len([z for z in zawodnicy_data if z.get("qr_code")])
    return jsonify({
        "total_zawodnikow": total,
        "z_qr_kodami": z_qr,
        "bez_qr_kodow": total - z_qr
    })

# ================== API/CENTRUM_STARTU MODULE (Pseudo) ==================
print("📦 Ładuję api/centrum_startu.py...")

centrum_startu_bp = Blueprint('centrum_startu', __name__)

@centrum_startu_bp.route("/api/grupy-startowe")
def get_grupy_startowe():
    """Grupy startowe z api/centrum_startu.py"""
    result = []
    for grupa in grupy_startowe_data:
        zawodnicy_w_grupie = [z for z in zawodnicy_data 
                              if z["kategoria"] == grupa["kategoria"] and z["plec"] == grupa["plec"]]
        
        grupa_info = grupa.copy()
        grupa_info["liczba_zawodnikow"] = len(zawodnicy_w_grupie)
        grupa_info["numery_startowe"] = ", ".join([str(z["nr_startowy"]) for z in zawodnicy_w_grupie])
        grupa_info["lista_zawodnikow"] = ", ".join([f"{z['imie']} {z['nazwisko']}" for z in zawodnicy_w_grupie])
        result.append(grupa_info)
    
    return jsonify(result)

@centrum_startu_bp.route("/api/qr/scan-result", methods=['POST'])
def qr_scan_result():
    """Skanowanie QR z api/centrum_startu.py"""
    try:
        data = request.json
        qr_code = data.get('qr_code', '').strip()
        
        if qr_code.startswith('SKATECROSS_QR_'):
            nr_startowy_str = qr_code.replace('SKATECROSS_QR_', '')
        else:
            nr_startowy_str = qr_code
        
        nr_startowy = int(nr_startowy_str)
        zawodnik = find_zawodnik_by_nr(nr_startowy)
        
        if not zawodnik:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Zawodnik z numerem {nr_startowy} nie istnieje"
            }), 404
        
        if zawodnik.get('checked_in'):
            return jsonify({
                "success": True,
                "action": "OSTRZEZENIE",
                "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} jest już w kolejce",
                "zawodnik": zawodnik
            })
        
        checkin_zawodnik(nr_startowy)
        
        return jsonify({
            "success": True,
            "action": "AKCEPTUJ",
            "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} dodany do kolejki",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "action": "ODRZUC",
            "message": f"Błąd skanowania: {str(e)}"
        }), 500

# ================== MAIN APP (Pseudo api/__init__.py + api_server.py) ==================
print("📦 Ładuję api/__init__.py i api_server.py...")

app = Flask(__name__)
CORS(app)

# Rejestracja blueprintów (normalnie w api/__init__.py)
print("🔗 Rejestruję blueprinty...")
app.register_blueprint(zawodnicy_bp)
app.register_blueprint(qr_generation_bp)
app.register_blueprint(centrum_startu_bp)

# System version
SYSTEM_VERSION = "1.0.0"
SYSTEM_NAME = "SKATECROSS QR System (Modular Demo v32.0)"
SYSTEM_FEATURES = ["QR Generation", "QR Printing", "Start Queue", "Scanner", "Modular Architecture", "Blueprinty"]

@app.route("/api/version")
def get_version():
    """Endpoint wersji z api_server.py"""
    return jsonify({
        "version": SYSTEM_VERSION,
        "name": SYSTEM_NAME,
        "features": SYSTEM_FEATURES,
        "status": "demo",
        "environment": "standalone",
        "database": "in-memory",
        "architecture": "modular_v32.0_demo",
        "modules": [
            "utils/database.py",
            "api/zawodnicy.py", 
            "api/qr_generation.py",
            "api/centrum_startu.py"
        ]
    })

@app.route("/")
def home():
    """Home endpoint"""
    return jsonify({
        "message": "🚀 SKATECROSS QR System - Modular Architecture Demo",
        "version": SYSTEM_VERSION,
        "status": "running",
        "architecture": "Blueprinty jako pseudo-moduły",
        "endpoints": [
            "/api/version",
            "/api/zawodnicy", 
            "/api/qr/generate/<nr>",
            "/api/qr/stats",
            "/api/grupy-startowe",
            "/api/qr/scan-result"
        ]
    })

if __name__ == "__main__":
    print("🚀 Uruchamiam SKATECROSS QR Backend (Modular Architecture Demo v32.0)")
    print("📊 Pseudo-moduły: zawodnicy_bp, qr_generation_bp, centrum_startu_bp")
    print("💾 Dane w pamięci (utils/database emulacja)")
    print("🌐 Serwer dostępny na http://localhost:5001")
    print("🏗️ Architektura: Blueprinty jako moduły")
    print("✨ To jest DEMO modułowej struktury jak w głównym projekcie v32.0!")
    print("-" * 70)
    app.run(debug=True, port=5001) 