#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
import qrcode
import argparse
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from io import BytesIO
import tempfile
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def generate_qr_for_print(qr_data, size_mm=25):
    """Generuje kod QR zoptymalizowany do druku"""
    # Oblicz rozmiar w pikselach (300 DPI dla dobrej jakości druku)
    size_px = int(size_mm * 300 / 25.4)  # 25.4mm = 1 cal
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Najwyższa korekcja błędów
        box_size=max(10, size_px // 25),  # Dostosuj box_size do rozmiaru
        border=6,  # Większa ramka dla druku
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Generuj obraz w wysokiej rozdzielczości
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size_px, size_px), resample=0)
    
    # Zapisz do tymczasowego pliku
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(temp_file.name, format='PNG', dpi=(300, 300))
    
    return temp_file.name

def get_zawodnicy_by_criteria(criteria):
    """Pobiera zawodników według kryteriów"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        base_query = """
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code
            FROM zawodnicy 
            WHERE qr_code IS NOT NULL
        """
        
        params = []
        
        if criteria.get('numbers'):
            # Konkretne numery startowe
            placeholders = ','.join(['%s'] * len(criteria['numbers']))
            base_query += f" AND nr_startowy IN ({placeholders})"
            params.extend(criteria['numbers'])
            
        if criteria.get('category'):
            base_query += " AND kategoria = %s"
            params.append(criteria['category'])
            
        if criteria.get('gender'):
            base_query += " AND plec = %s"
            params.append(criteria['gender'])
            
        if criteria.get('club'):
            base_query += " AND klub ILIKE %s"
            params.append(f"%{criteria['club']}%")
        
        base_query += " ORDER BY nr_startowy"
        
        cur.execute(base_query, params)
        zawodnicy = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return zawodnicy
        
    except Exception as e:
        print(f"❌ Błąd podczas pobierania zawodników: {e}")
        return []

def create_qr_label(zawodnik_data, qr_size_mm=25):
    """Tworzy pojedynczą etykietę z kodem QR dla zawodnika"""
    nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code = zawodnik_data
    
    # Generuj kod QR
    qr_image_path = generate_qr_for_print(qr_code, qr_size_mm)
    
    # Dane do etykiety
    label_data = {
        'qr_image': qr_image_path,
        'nr_startowy': nr_startowy,
        'imie': imie,
        'nazwisko': nazwisko,
        'kategoria': kategoria,
        'plec': plec,
        'klub': klub or 'Brak klubu',
        'qr_code': qr_code
    }
    
    return label_data

def generate_pdf_stickers(zawodnicy, output_file="qr_stickers.pdf", layout="stickers"):
    """Generuje PDF z naklejkami QR kodów"""
    
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=10*mm,
        leftMargin=10*mm,
        topMargin=10*mm,
        bottomMargin=10*mm
    )
    
    styles = getSampleStyleSheet()
    
    # Style dla różnych elementów
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=20,
        alignment=1  # Wyśrodkowanie
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.darkgreen,
        spaceAfter=5
    )
    
    content = []
    
    # Tytuł dokumentu
    title = Paragraph("🏆 SKATECROSS - Kody QR do druku", title_style)
    content.append(title)
    
    info = Paragraph(f"Wygenerowano {len(zawodnicy)} kodów QR | Data: {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')}", header_style)
    content.append(info)
    content.append(Spacer(1, 10*mm))
    
    if layout == "stickers":
        # Layout naklejek - 3 kolumny na stronie
        generate_sticker_layout(content, zawodnicy, styles)
    elif layout == "list":
        # Layout listy - jeden zawodnik na linię
        generate_list_layout(content, zawodnicy, styles)
    elif layout == "large":
        # Layout dużych kodów - jeden kod na stronę
        generate_large_layout(content, zawodnicy, styles)
    
    # Generuj PDF
    doc.build(content)
    print(f"✅ Wygenerowano PDF: {output_file}")
    
    # Usuń tymczasowe pliki QR
    for zawodnik in zawodnicy:
        label = create_qr_label(zawodnik)
        if os.path.exists(label['qr_image']):
            os.unlink(label['qr_image'])

def generate_sticker_layout(content, zawodnicy, styles):
    """Generuje layout naklejek - 3x8 = 24 naklejki na stronę"""
    
    # Przygotuj dane w grupach po 3 (3 kolumny)
    rows = []
    for i in range(0, len(zawodnicy), 3):
        row_zawodnicy = zawodnicy[i:i+3]
        
        # Utwórz etykiety dla tej linii
        row_labels = []
        for zawodnik in row_zawodnicy:
            label = create_qr_label(zawodnik, qr_size_mm=20)  # Mniejsze QR dla naklejek
            
            # Stwórz komórkę dla naklejki
            cell_content = [
                [Image(label['qr_image'], width=20*mm, height=20*mm)],
                [Paragraph(f"<b>#{label['nr_startowy']}</b>", styles['Normal'])],
                [Paragraph(f"{label['imie']} {label['nazwisko']}", styles['Normal'])],
                [Paragraph(f"{label['kategoria']} | {label['plec']}", styles['Normal'])],
                [Paragraph(f"{label['klub'][:20]}{'...' if len(label['klub']) > 20 else ''}", styles['Normal'])]
            ]
            
            cell_table = Table(cell_content, colWidths=[20*mm])
            cell_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            row_labels.append(cell_table)
        
        # Dopełnij wiersz pustymi komórkami jeśli potrzeba
        while len(row_labels) < 3:
            row_labels.append("")
        
        rows.append(row_labels)
    
    # Utwórz główną tabelę
    main_table = Table(rows, colWidths=[65*mm, 65*mm, 65*mm], rowHeights=[30*mm]*len(rows))
    main_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    
    content.append(main_table)

def generate_list_layout(content, zawodnicy, styles):
    """Generuje layout listy - kompaktowy"""
    
    header_data = [['Nr', 'Kod QR', 'Zawodnik', 'Kategoria', 'Klub']]
    
    for zawodnik in zawodnicy:
        label = create_qr_label(zawodnik, qr_size_mm=15)
        
        header_data.append([
            label['nr_startowy'],
            Image(label['qr_image'], width=15*mm, height=15*mm),
            f"{label['imie']} {label['nazwisko']}",
            f"{label['kategoria']} | {label['plec']}",
            label['klub'][:25] + ('...' if len(label['klub']) > 25 else '')
        ])
    
    table = Table(header_data, colWidths=[15*mm, 20*mm, 50*mm, 25*mm, 60*mm])
    table.setStyle(TableStyle([
        # Nagłówek
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        
        # Dane
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Nr startowy
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # QR kod
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Ramki
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
        
        # Naprzemienne kolory wierszy
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    content.append(table)

def generate_large_layout(content, zawodnicy, styles):
    """Generuje layout dużych kodów - jeden kod na stronę"""
    
    large_style = ParagraphStyle(
        'Large',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=10
    )
    
    for i, zawodnik in enumerate(zawodnicy):
        label = create_qr_label(zawodnik, qr_size_mm=60)  # Duży QR kod
        
        # Wyśrodkowana tabela z dużym kodem
        large_data = [
            [Image(label['qr_image'], width=60*mm, height=60*mm)],
            [Paragraph(f"<b>#{label['nr_startowy']} - {label['imie']} {label['nazwisko']}</b>", large_style)],
            [Paragraph(f"Kategoria: {label['kategoria']} | Płeć: {label['plec']}", large_style)],
            [Paragraph(f"Klub: {label['klub']}", large_style)],
            [Paragraph(f"QR Code: {label['qr_code']}", styles['Normal'])],
        ]
        
        large_table = Table(large_data, colWidths=[80*mm])
        large_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('SPACEAFTER', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 2, colors.darkblue),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
        ]))
        
        content.append(large_table)
        
        # Dodaj nową stronę (oprócz ostatniego)
        if i < len(zawodnicy) - 1:
            content.append(SimpleDocTemplate.PageBreak())

def main():
    parser = argparse.ArgumentParser(description='Generator PDF z kodami QR dla zawodników')
    
    parser.add_argument('--numbers', nargs='+', type=int, help='Numery startowe zawodników (np. --numbers 1 2 3)')
    parser.add_argument('--category', help='Kategoria zawodników (np. OPEN, JUNIOR)')
    parser.add_argument('--gender', choices=['M', 'K'], help='Płeć zawodników')
    parser.add_argument('--club', help='Nazwa klubu (częściowe dopasowanie)')
    parser.add_argument('--layout', choices=['stickers', 'list', 'large'], default='stickers', 
                       help='Layout: stickers (naklejki), list (lista), large (duże kody)')
    parser.add_argument('--output', default='qr_codes.pdf', help='Nazwa pliku wyjściowego')
    parser.add_argument('--all', action='store_true', help='Wszystkich zawodników')
    
    args = parser.parse_args()
    
    # Przygotuj kryteria
    criteria = {}
    if args.numbers:
        criteria['numbers'] = args.numbers
    if args.category:
        criteria['category'] = args.category
    if args.gender:
        criteria['gender'] = args.gender
    if args.club:
        criteria['club'] = args.club
    
    # Jeśli nie podano kryteriów i nie --all, pokaż pomoc
    if not criteria and not args.all:
        print("❌ Musisz podać kryteria wyboru zawodników lub użyć --all")
        parser.print_help()
        return
    
    print("🏆 Generator PDF z kodami QR SKATECROSS")
    print("=" * 50)
    
    # Pobierz zawodników
    zawodnicy = get_zawodnicy_by_criteria(criteria)
    
    if not zawodnicy:
        print("❌ Nie znaleziono zawodników spełniających kryteria")
        return
    
    print(f"📊 Znaleziono {len(zawodnicy)} zawodników")
    print(f"📄 Layout: {args.layout}")
    print(f"💾 Plik wyjściowy: {args.output}")
    
    # Generuj PDF
    generate_pdf_stickers(zawodnicy, args.output, args.layout)
    
    print(f"✅ Gotowe! Otwórz plik: {args.output}")

if __name__ == "__main__":
    main() 