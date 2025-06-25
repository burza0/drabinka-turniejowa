"""
SKATECROSS QR System - QR Generation Module
Blueprint dla endpointów generowania QR kodów
"""

from flask import Blueprint, jsonify, request
import qrcode
import base64
import io
from utils.database import find_zawodnik_by_nr, update_zawodnik_qr, get_qr_stats

qr_generation_bp = Blueprint('qr_generation', __name__)

@qr_generation_bp.route("/api/qr/generate/<int:nr_startowy>", methods=['POST'])
def qr_generate_for_zawodnik(nr_startowy):
    """Generowanie QR kodu dla pojedynczego zawodnika"""
    try:
        # Znajdź zawodnika
        zawodnik = find_zawodnik_by_nr(nr_startowy)
        if not zawodnik:
            return jsonify({"error": "Zawodnik nie istnieje"}), 404
        
        # Wygeneruj QR kod
        qr_data = f"SKATECROSS_QR_{nr_startowy}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Zapisz QR kod w danych
        update_zawodnik_qr(nr_startowy, qr_data)
        
        # Wygeneruj obraz QR kodu jako base64
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

@qr_generation_bp.route("/api/qr/generate-bulk", methods=['POST'])
def qr_generate_bulk():
    """Masowe generowanie QR kodów"""
    try:
        data = request.json
        numery_startowe = data.get('numery_startowe', [])
        
        if not numery_startowe:
            return jsonify({"error": "Brak numerów startowych"}), 400
        
        results = []
        
        for nr_startowy in numery_startowe:
            try:
                # Znajdź zawodnika
                zawodnik = find_zawodnik_by_nr(nr_startowy)
                
                if not zawodnik:
                    results.append({
                        "nr_startowy": nr_startowy,
                        "success": False,
                        "error": "Zawodnik nie istnieje"
                    })
                    continue
                
                # Wygeneruj QR kod
                qr_data = f"SKATECROSS_QR_{nr_startowy}"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                # Zapisz QR kod w danych
                update_zawodnik_qr(nr_startowy, qr_data)
                
                # Wygeneruj obraz QR kodu jako base64
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                results.append({
                    "nr_startowy": nr_startowy,
                    "success": True,
                    "qr_code": qr_data,
                    "qr_image": f"data:image/png;base64,{img_str}",
                    "zawodnik": zawodnik
                })
                
            except Exception as e:
                results.append({
                    "nr_startowy": nr_startowy,
                    "success": False,
                    "error": str(e)
                })
        
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        return jsonify({
            "success": True,
            "generated": len(successful),
            "failed": len(failed),
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd masowego generowania QR: {str(e)}"
        }), 500

@qr_generation_bp.route("/api/qr/stats")
def qr_stats():
    """Statystyki QR kodów"""
    try:
        stats = get_qr_stats()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania statystyk QR: {str(e)}"}), 500 