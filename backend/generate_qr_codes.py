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
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Zwiększona korekcja błędów
        box_size=15,  # Większy rozmiar
        border=8,     # Większa ramka
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Generuj obraz z lepszym kontrastem
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Zwiększ rozmiar obrazu dla lepszej czytelności
    img = img.resize((400, 400), resample=0)
    
    # Konwertuj do base64
    buffer = BytesIO()
    img.save(buffer, format='PNG', quality=100)
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

def test_qr_code(qr_data):
    """Testuje wygenerowany kod QR"""
    try:
        # Generuj obraz QR
        img_str = generate_qr_image(qr_data)
        
        # Zapisz do pliku testowego
        test_dir = "test_qr"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            
        # Zapisz jako HTML z podglądem
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test QR Code</title>
            <style>
                body {{ font-family: Arial; text-align: center; padding: 20px; }}
                .qr-container {{ 
                    max-width: 400px; 
                    margin: 0 auto; 
                    padding: 20px;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                }}
                .qr-code {{ margin: 20px 0; }}
                .qr-text {{ 
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 5px;
                    font-family: monospace;
                }}
            </style>
        </head>
        <body>
            <div class="qr-container">
                <h2>Test QR Code</h2>
                <div class="qr-code">
                    <img src="data:image/png;base64,{img_str}" width="300" height="300">
                </div>
                <div class="qr-text">
                    {qr_data}
                </div>
                <p>Skopiuj ten kod i przetestuj w skanerze</p>
            </div>
        </body>
        </html>
        """
        
        with open(f"{test_dir}/test_{qr_data}.html", "w") as f:
            f.write(html_content)
            
        print(f"✅ Wygenerowano testowy QR kod: {test_dir}/test_{qr_data}.html")
        return True
        
    except Exception as e:
        print(f"❌ Błąd podczas testowania QR kodu: {e}")
        return False

if __name__ == "__main__":
    print("🏆 Generator QR kodów SKATECROSS")
    print("=" * 40)
    
    # Test wygenerowanego kodu
    test_qr = "SKATECROSS_1_TEST123"
    print("\n🧪 Testowanie generowania QR kodu...")
    test_qr_code(test_qr)
    
    # Pokaż aktualne statystyki
    show_qr_stats()
    
    # Wygeneruj QR kody
    update_qr_codes()
    
    # Pokaż zaktualizowane statystyki
    show_qr_stats() 