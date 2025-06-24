# -*- coding: utf-8 -*-
"""
SKATECROSS QR - QR Generation API Blueprint
Wersja: 1.0.0
System generowania i skanowania kodów QR
"""

from flask import Blueprint, jsonify, request, render_template_string
import qrcode
import io
import base64
import sys
import os

# Dodaj ścieżkę do utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.database import get_all, get_one, execute_query

qr_generation_bp = Blueprint('qr_generation', __name__)

@qr_generation_bp.route('/api/qr/generate/<int:nr_startowy>', methods=['GET'])
def generate_qr_code(nr_startowy):
    """Generuje kod QR dla zawodnika"""
    
    # Pobierz zawodnika z bazy PostgreSQL
    zawodnik = get_one("""
        SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code
        FROM zawodnicy 
        WHERE nr_startowy = %s
    """, (nr_startowy,))
    
    if not zawodnik:
        return jsonify({
            "success": False,
            "error": f"Nie znaleziono zawodnika o numerze startowym {nr_startowy}"
        }), 404
    
    # Generuj kod QR
    qr_data = f"SKATECROSS_QR_{zawodnik['nr_startowy']}_{zawodnik['imie']}_{zawodnik['nazwisko']}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Utwórz obraz QR kodu
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Konwertuj na base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return jsonify({
        "success": True,
        "data": {
            "zawodnik": zawodnik,
            "qr_code_data": qr_data,
            "qr_code_image": f"data:image/png;base64,{img_base64}"
        }
    })

@qr_generation_bp.route('/api/qr/bulk-generate', methods=['POST'])
def bulk_generate_qr():
    """Generuje kody QR dla wielu zawodników"""
    
    data = request.get_json()
    numery_startowe = data.get('numery_startowe', [])
    
    if not numery_startowe:
        return jsonify({
            "success": False,
            "error": "Brak numerów startowych do wygenerowania"
        }), 400
    
    generated_codes = []
    errors = []
    
    for nr in numery_startowe:
        try:
            # Pobierz zawodnika
            zawodnik = get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code
                FROM zawodnicy 
                WHERE nr_startowy = %s
            """, (nr,))
            
            if not zawodnik:
                errors.append(f"Nie znaleziono zawodnika nr {nr}")
                continue
            
            # Generuj QR kod (bez obrazu - tylko dane)
            qr_data = f"SKATECROSS_QR_{zawodnik['nr_startowy']}_{zawodnik['imie']}_{zawodnik['nazwisko']}"
            
            generated_codes.append({
                "nr_startowy": nr,
                "zawodnik": zawodnik,
                "qr_code_data": qr_data
            })
            
        except Exception as e:
            errors.append(f"Błąd generowania QR dla zawodnika {nr}: {str(e)}")
    
    return jsonify({
        "success": True,
        "data": {
            "generated_count": len(generated_codes),
            "error_count": len(errors),
            "codes": generated_codes,
            "errors": errors
        }
    })

@qr_generation_bp.route('/api/qr/dashboard', methods=['GET'])
def qr_dashboard():
    """Dashboard z statystykami QR kodów"""
    
    # Pobierz statystyki z bazy PostgreSQL
    stats_result = get_one("""
        SELECT 
            COUNT(*) as total_zawodnicy,
            COUNT(CASE WHEN qr_code IS NOT NULL THEN 1 END) as z_qr_kodami,
            COUNT(CASE WHEN checked_in = true THEN 1 END) as zameldowani
        FROM zawodnicy
    """)
    
    # Pobierz przykładowych zawodników
    sample_zawodnicy = get_all("""
        SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
               COALESCE(checked_in, false) as checked_in
        FROM zawodnicy 
        ORDER BY nr_startowy 
        LIMIT 10
    """)
    
    stats = {
        "total_zawodnicy": stats_result['total_zawodnicy'] if stats_result else 0,
        "z_qr_kodami": stats_result['z_qr_kodami'] if stats_result else 0,
        "bez_qr_kodow": (stats_result['total_zawodnicy'] - stats_result['z_qr_kodami']) if stats_result else 0,
        "zameldowani": stats_result['zameldowani'] if stats_result else 0,
        "niezameldowani": (stats_result['total_zawodnicy'] - stats_result['zameldowani']) if stats_result else 0
    }
    
    return jsonify({
        "success": True,
        "data": {
            "stats": stats,
            "sample_zawodnicy": sample_zawodnicy
        }
    })

@qr_generation_bp.route('/api/qr/manual-checkins', methods=['GET'])
def get_manual_checkins():
    """Pobiera listę zawodników do ręcznego meldowania"""
    
    # Pobierz niezameldowanych zawodników
    niezameldowani = get_all("""
        SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
               COALESCE(checked_in, false) as checked_in
        FROM zawodnicy 
        WHERE COALESCE(checked_in, false) = false
        ORDER BY nr_startowy
        LIMIT 50
    """)
    
    return jsonify({
        "success": True,
        "data": {
            "niezameldowani": niezameldowani,
            "count": len(niezameldowani)
        }
    })

print("🔲 SKATECROSS QR - Moduł QR Generation załadowany z Supabase PostgreSQL") 