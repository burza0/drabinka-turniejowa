#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
import qrcode
import uuid
import base64
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def generate_qr_for_zawodnik(nr_startowy, imie, nazwisko):
    """Generuje unikalny QR kod dla zawodnika"""
    # Format: SKATECROSS_{nr_startowy}_{unique_hash}
    unique_hash = uuid.uuid4().hex[:8].upper()
    qr_data = f"SKATECROSS_{nr_startowy}_{unique_hash}"
    
    return qr_data

def generate_qr_image(qr_data):
    """Generuje obraz QR kodu jako base64"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Konwertuj do base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

def update_qr_codes():
    """Generuje QR kody dla wszystkich zawodników którzy ich nie mają"""
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🔧 Generowanie QR kodów dla zawodników...")
        
        # Znajdź zawodników bez QR kodów
        cur.execute("""
            SELECT nr_startowy, imie, nazwisko 
            FROM zawodnicy 
            WHERE qr_code IS NULL 
            ORDER BY nr_startowy
        """)
        zawodnicy_bez_qr = cur.fetchall()
        
        print(f"📊 Znaleziono {len(zawodnicy_bez_qr)} zawodników bez QR kodów")
        
        updated_count = 0
        for nr_startowy, imie, nazwisko in zawodnicy_bez_qr:
            try:
                # Generuj unikalny QR kod
                qr_data = generate_qr_for_zawodnik(nr_startowy, imie, nazwisko)
                
                # Sprawdź czy QR kod już nie istnieje (zabezpieczenie przed duplikatami)
                cur.execute("SELECT COUNT(*) FROM zawodnicy WHERE qr_code = %s", (qr_data,))
                if cur.fetchone()[0] > 0:
                    print(f"⚠️  QR kod dla {nr_startowy} już istnieje, pomijam...")
                    continue
                
                # Zapisz QR kod do bazy
                cur.execute(
                    "UPDATE zawodnicy SET qr_code = %s WHERE nr_startowy = %s",
                    (qr_data, nr_startowy)
                )
                
                updated_count += 1
                print(f"✅ {nr_startowy}. {imie} {nazwisko} -> {qr_data}")
                
            except Exception as e:
                print(f"❌ Błąd dla zawodnika {nr_startowy}: {e}")
                continue
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n🎉 Wygenerowano QR kody dla {updated_count} zawodników!")
        
    except Exception as e:
        print(f"❌ Błąd podczas generowania QR kodów: {e}")
        if conn:
            conn.rollback()
            conn.close()

def show_qr_stats():
    """Pokazuje statystyki QR kodów"""
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Statystyki QR kodów
        cur.execute("SELECT COUNT(*) FROM zawodnicy")
        total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM zawodnicy WHERE qr_code IS NOT NULL")
        with_qr = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM zawodnicy WHERE checked_in = TRUE")
        checked_in = cur.fetchone()[0]
        
        print(f"\n📊 STATYSTYKI QR KODÓW:")
        print(f"  Łącznie zawodników: {total}")
        print(f"  Z QR kodami: {with_qr}")
        print(f"  Zameldowanych: {checked_in}")
        print(f"  Bez QR kodów: {total - with_qr}")
        
        # Przykładowe QR kody
        cur.execute("SELECT nr_startowy, imie, nazwisko, qr_code FROM zawodnicy WHERE qr_code IS NOT NULL LIMIT 5")
        examples = cur.fetchall()
        
        print(f"\n🔍 PRZYKŁADOWE QR KODY:")
        for nr, imie, nazwisko, qr in examples:
            print(f"  {nr}. {imie} {nazwisko} -> {qr}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd podczas pobierania statystyk: {e}")

if __name__ == "__main__":
    print("🏆 Generator QR kodów SKATECROSS")
    print("=" * 40)
    
    # Pokaż aktualne statystyki
    show_qr_stats()
    
    # Wygeneruj QR kody
    update_qr_codes()
    
    # Pokaż zaktualizowane statystyki
    show_qr_stats() 