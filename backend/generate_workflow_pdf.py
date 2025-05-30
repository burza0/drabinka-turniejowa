#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

# Używamy standardowych fontów dostępnych w reportlab
FONT_FAMILY = 'Helvetica'
FONT_FAMILY_BOLD = 'Helvetica-Bold'
FONT_FAMILY_MONO = 'Courier'

def create_workflow_pdf():
    # Ustawienia dokumentu z właściwym encodingiem
    filename = "SKATECROSS_Workflow_Zawodow.pdf"
    doc = SimpleDocTemplate(
        filename, 
        pagesize=A4,
        rightMargin=2*cm, 
        leftMargin=2*cm,
        topMargin=2.5*cm, 
        bottomMargin=2.5*cm,
        title="SKATECROSS - Workflow Zawodów",
        author="SKATECROSS Dashboard System"
    )
    
    # Style z obsługą polskich znaków
    styles = getSampleStyleSheet()
    
    # Główny tytuł
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        spaceAfter=25,
        spaceBefore=10,
        alignment=TA_CENTER,
        textColor=HexColor('#1e40af'),
        fontName=FONT_FAMILY_BOLD,
        leading=30
    )
    
    # Podtytuł
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=30,
        spaceBefore=10,
        alignment=TA_CENTER,
        textColor=HexColor('#374151'),
        fontName=FONT_FAMILY,
        leading=20
    )
    
    # Nagłówki sekcji
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=15,
        spaceBefore=25,
        textColor=HexColor('#1e40af'),
        fontName=FONT_FAMILY_BOLD,
        leading=20,
        borderWidth=1,
        borderColor=HexColor('#e5e7eb'),
        borderPadding=8,
        backColor=HexColor('#f8fafc')
    )
    
    # Podsekcje
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=13,
        spaceAfter=10,
        spaceBefore=18,
        textColor=HexColor('#374151'),
        fontName=FONT_FAMILY_BOLD,
        leading=16
    )
    
    # Normalny tekst
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        spaceBefore=4,
        alignment=TA_JUSTIFY,
        fontName=FONT_FAMILY,
        leading=14,
        leftIndent=0,
        rightIndent=0
    )
    
    # Kod/przykłady
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=8,
        fontName=FONT_FAMILY_MONO,
        backColor=HexColor('#f3f4f6'),
        borderColor=HexColor('#d1d5db'),
        borderWidth=1,
        borderPadding=8,
        spaceAfter=12,
        spaceBefore=8,
        leftIndent=10,
        rightIndent=10,
        leading=12
    )
    
    # Informacje dodatkowe (box)
    info_style = ParagraphStyle(
        'Info',
        parent=normal_style,
        backColor=HexColor('#eff6ff'),
        borderColor=HexColor('#3b82f6'),
        borderWidth=2,
        borderPadding=12,
        spaceAfter=15,
        spaceBefore=10
    )
    
    # Tworzenie treści
    story = []
    
    # === STRONA TYTUŁOWA ===
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("SKATECROSS DASHBOARD", title_style))
    story.append(Paragraph("Workflow Zawodów - Instrukcja Obsługi", subtitle_style))
    story.append(Spacer(1, 1*cm))
    
    # Informacje o dokumencie
    doc_info = f"""
    <b>Wersja:</b> 2.0<br/>
    <b>Data wygenerowania:</b> {datetime.now().strftime('%d.%m.%Y, godz. %H:%M')}<br/>
    <b>System:</b> SKATECROSS Dashboard z workflow zawodów<br/>
    <b>Autor:</b> System SKATECROSS
    """
    story.append(Paragraph(doc_info, info_style))
    story.append(Spacer(1, 2*cm))
    
    # Spis treści
    toc_data = [
        ['SPIS TREŚCI', ''],
        ['1. Wprowadzenie', 'str. 2'],
        ['2. Architektura systemu', 'str. 2'],
        ['3. Workflow zawodów', 'str. 2-3'],
        ['4. Instrukcja obsługi', 'str. 3-4'],
        ['5. API Endpointy', 'str. 4'],
        ['6. Przykłady użycia', 'str. 4-5'],
        ['7. Konfiguracja i uruchomienie', 'str. 5'],
        ['8. Baza danych', 'str. 5'],
        ['9. Rozwiązywanie problemów', 'str. 5']
    ]
    
    toc_table = Table(toc_data, colWidths=[12*cm, 3*cm])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(toc_table)
    
    # Nowa strona
    story.append(PageBreak())
    
    # === 1. WPROWADZENIE ===
    story.append(Paragraph("1. WPROWADZENIE", heading_style))
    
    intro_text = """
    System SKATECROSS Dashboard został rozszerzony o kompletny workflow zawodów, który umożliwia 
    sprawne zarządzanie całym procesem organizacji zawodów skatecross.
    """
    story.append(Paragraph(intro_text, normal_style))
    story.append(Spacer(1, 10))
    
    # Funkcjonalności w ładnej tabeli
    func_data = [
        ['FUNKCJONALNOŚĆ', 'OPIS'],
        ['Grupy startowe', 'Automatyczne tworzenie grup na podstawie zameldowanych zawodników'],
        ['Weryfikacja QR', 'Kontrola zawodników na linii startu przez skanowanie kodów QR'],
        ['Kolejka startowa', 'Monitoring zawodników oczekujących na start w czasie rzeczywistym'],
        ['Integracja QR', 'Pełna kompatybilność z istniejącym systemem kodów QR'],
        ['Statystyki', 'Podgląd liczby grup, zawodników i szacowanego czasu zawodów']
    ]
    
    func_table = Table(func_data, colWidths=[4*cm, 11*cm])
    func_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1fae5')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(func_table)
    story.append(Spacer(1, 20))
    
    # === 2. ARCHITEKTURA SYSTEMU ===
    story.append(Paragraph("2. ARCHITEKTURA SYSTEMU", heading_style))
    
    # Komponenty
    components_data = [
        ['KOMPONENT', 'FUNKCJA', 'DOSTĘP'],
        ['GrupyStartowe.vue', 'Zarządzanie grupami startowymi', 'Admin'],
        ['StartLineScanner.vue', 'Weryfikacja zawodników na starcie', 'Admin'],
        ['QrPrint.vue', 'Drukowanie QR kodów (istniejący)', 'Admin'],
        ['QrAdminDashboard.vue', 'Dashboard QR (istniejący)', 'Admin']
    ]
    
    components_table = Table(components_data, colWidths=[4.5*cm, 7.5*cm, 3*cm])
    components_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0'))
    ]))
    story.append(components_table)
    story.append(Spacer(1, 20))
    
    # === 3. WORKFLOW ZAWODÓW ===
    story.append(Paragraph("3. WORKFLOW ZAWODÓW", heading_style))
    
    # 3.1 Dzień przed zawodami
    story.append(Paragraph("3.1 Dzień przed zawodami", subheading_style))
    
    prep_text = """
    <b>Przygotowania organizacyjne:</b><br/>
    1. <b>Lista startowa</b> - wszyscy zawodnicy wprowadzeni do systemu<br/>
    2. <b>Generowanie QR kodów</b> - zakładka "Drukowanie QR"<br/>
    3. <b>Drukowanie naklejek</b> - QR kody na numerach startowych<br/>
    4. <b>Sprawdzenie statusów</b> - kontrola w "QR Dashboard"
    """
    story.append(Paragraph(prep_text, normal_style))
    story.append(Spacer(1, 15))
    
    # 3.2 Dzień zawodów
    story.append(Paragraph("3.2 Dzień zawodów", subheading_style))
    
    # Workflow w ulepszonej tabeli
    workflow_data = [
        ['ETAP', 'MIEJSCE', 'DZIAŁANIE', 'SYSTEM'],
        ['1. Check-in', 'Biuro zawodów', 'Zameldowanie zawodników', 'QR Scanner - checked_in=TRUE'],
        ['2. Grupy', 'Organizacja', 'Tworzenie grup startowych', 'Zakładka "Grupy Startowe"'],
        ['3. Start', 'Linia startu', 'Weryfikacja zawodników', 'Zakładka "Linia Startu"'],
        ['4. Wyniki', 'Meta', 'Zapisywanie czasów', 'System pomiaru (istniejący)']
    ]
    
    workflow_table = Table(workflow_data, colWidths=[2.5*cm, 3*cm, 4.5*cm, 5*cm])
    workflow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fffbeb')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#fed7aa')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(workflow_table)
    story.append(Spacer(1, 20))
    
    # Nowa strona
    story.append(PageBreak())
    
    # === 4. INSTRUKCJA OBSŁUGI ===
    story.append(Paragraph("4. INSTRUKCJA OBSŁUGI", heading_style))
    
    # 4.1 Grupy Startowe
    story.append(Paragraph("4.1 Zarządzanie Grupami Startowymi", subheading_style))
    
    access_info = """
    <b>Dostęp:</b> Menu Admin - "Grupy Startowe"
    """
    story.append(Paragraph(access_info, info_style))
    
    groups_functions = """
    <b>Główne funkcje:</b><br/>
    • <b>Automatyczne grupowanie</b> - system tworzy grupy na podstawie zameldowanych zawodników<br/>
    • <b>Podział według kategorii i płci</b> - np. "Junior B Mężczyźni", "Senior Kobiety"<br/>
    • <b>Szacunkowy czas</b> - 20 sekund na zawodnika (można dostosować)<br/>
    • <b>Aktywacja grupy</b> - ustaw aktywną grupę do weryfikacji na starcie<br/><br/>
    
    <b>Dostępne statystyki:</b><br/>
    • Liczba grup startowych<br/>
    • Liczba zameldowanych zawodników<br/>
    • Szacunkowy czas zawodów w minutach<br/>
    • Aktualnie aktywna grupa
    """
    story.append(Paragraph(groups_functions, normal_style))
    story.append(Spacer(1, 15))
    
    # 4.2 Linia Startu
    story.append(Paragraph("4.2 Weryfikacja na Linii Startu", subheading_style))
    
    startline_access = """
    <b>Dostęp:</b> Menu Admin - "Linia Startu"
    """
    story.append(Paragraph(startline_access, info_style))
    
    startline_process = """
    <b>Proces weryfikacji (krok po kroku):</b><br/>
    1. <b>Skanowanie QR</b> - za pomocą czytnika lub wpis ręczny<br/>
    2. <b>Automatyczna weryfikacja</b> - system sprawdza status zawodnika<br/>
    3. <b>Decyzja systemu</b> - jedna z trzech opcji weryfikacji
    """
    story.append(Paragraph(startline_process, normal_style))
    story.append(Spacer(1, 10))
    
    # Tabela statusów weryfikacji
    status_data = [
        ['STATUS', 'OPIS SYTUACJI', 'REKOMENDOWANE DZIAŁANIE'],
        ['AKCEPTUJ', 'Zawodnik zameldowany, bez wyniku', 'Może startować'],
        ['OSTRZEŻENIE', 'Zawodnik już ma wynik lub inna grupa', 'Sprawdź szczegóły, można pozwolić'],
        ['ODRZUĆ', 'Niezameldowany lub inne problemy', 'Nie może startować']
    ]
    
    status_table = Table(status_data, colWidths=[3*cm, 6*cm, 6*cm])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#dc2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fef2f2')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#fca5a5')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(status_table)
    story.append(Spacer(1, 15))
    
    # Kolejka startowa
    queue_info = """
    <b>Kolejka startowa:</b><br/>
    • <b>Automatyczne dodawanie</b> - zawodnicy pojawiają się po zeskanowaniu<br/>
    • <b>Odświeżanie co 5 sekund</b> - aktualne informacje w czasie rzeczywistym<br/>
    • <b>Historia skanów</b> - znaczniki czasu wszystkich weryfikacji<br/>
    • <b>Status wyników</b> - informacja czy zawodnik już ma zapisany czas
    """
    story.append(Paragraph(queue_info, normal_style))
    story.append(Spacer(1, 20))
    
    # Nowa strona
    story.append(PageBreak())
    
    # === 5. API ENDPOINTY ===
    story.append(Paragraph("5. API ENDPOINTY", heading_style))
    
    api_intro = """
    System workflow korzysta z następujących endpointów API Backend (Flask):
    """
    story.append(Paragraph(api_intro, normal_style))
    story.append(Spacer(1, 10))
    
    # Tabela API
    api_data = [
        ['ENDPOINT', 'METODA', 'FUNKCJA'],
        ['/api/grupy-startowe', 'GET', 'Pobieranie wszystkich grup startowych'],
        ['/api/grupa-aktywna', 'POST', 'Ustawianie aktywnej grupy'],
        ['/api/start-line-verify', 'POST', 'Weryfikacja QR na linii startu'],
        ['/api/start-queue', 'GET', 'Pobranie kolejki startowej'],
        ['/api/qr/check-in', 'POST', 'Zameldowanie zawodnika (check-in)'],
        ['/api/qr/stats', 'GET', 'Statystyki kodów QR']
    ]
    
    api_table = Table(api_data, colWidths=[5*cm, 2*cm, 8*cm])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#cbd5e1'))
    ]))
    story.append(api_table)
    story.append(Spacer(1, 20))
    
    # === 6. PRZYKŁADY UŻYCIA ===
    story.append(Paragraph("6. PRZYKŁADY UŻYCIA", heading_style))
    
    # Przykład 1
    story.append(Paragraph("6.1 Weryfikacja zawodnika na linii startu", subheading_style))
    
    example1_code = """curl -X POST -H "Content-Type: application/json" \\
  -d '{"qr_code":"SKATECROSS_1_C0A8C8E6","device_id":"start-terminal"}' \\
  http://localhost:5000/api/start-line-verify

Przykładowa odpowiedź:
{
  "action": "OSTRZEŻENIE",
  "issues": ["Zawodnik już ma zapisany wynik"],
  "komunikat": "Jan Kowalski - SPRAWDŹ SZCZEGÓŁY",
  "success": true,
  "zawodnik": {
    "nr_startowy": 1,
    "imie": "Jan",
    "nazwisko": "Kowalski",
    "kategoria": "Junior B",
    "plec": "M",
    "checked_in": true,
    "ma_wynik": true
  }
}"""
    story.append(Paragraph(example1_code, code_style))
    story.append(Spacer(1, 15))
    
    # Przykład 2
    story.append(Paragraph("6.2 Pobieranie grup startowych", subheading_style))
    
    example2_code = """curl http://localhost:5000/api/grupy-startowe

Przykładowa odpowiedź:
{
  "success": true,
  "total_grup": 2,
  "total_zawodnikow": 3,
  "estimated_total_time_min": 1.0,
  "grupy": [
    {
      "numer_grupy": 1,
      "nazwa": "Grupa 1: Junior B Mężczyźni",
      "kategoria": "Junior B",
      "plec": "M",
      "liczba_zawodnikow": 2,
      "estimated_time": 40,
      "status": "OCZEKUJE"
    }
  ]
}"""
    story.append(Paragraph(example2_code, code_style))
    story.append(Spacer(1, 20))
    
    # === 7. KONFIGURACJA ===
    story.append(Paragraph("7. KONFIGURACJA I URUCHOMIENIE", heading_style))
    
    requirements_info = """
    <b>Wymagania systemu:</b> Python 3.8+, Node.js 16+, PostgreSQL 12+
    """
    story.append(Paragraph(requirements_info, info_style))
    
    config_text = """
    <b>Krok po kroku uruchomienie:</b><br/>
    1. <b>Backend:</b> cd backend && source venv/bin/activate && python3 api_server.py<br/>
    2. <b>Frontend:</b> cd frontend && npm run dev<br/><br/>
    
    <b>Dostęp do aplikacji:</b><br/>
    • <b>Frontend:</b> http://localhost:5174<br/>
    • <b>Backend API:</b> http://localhost:5000<br/>
    • <b>Admin panel:</b> Przełącznik "Admin" w prawym górnym rogu interfejsu
    """
    story.append(Paragraph(config_text, normal_style))
    story.append(Spacer(1, 20))
    
    # === 8. BAZA DANYCH ===
    story.append(Paragraph("8. STRUKTURA BAZY DANYCH", heading_style))
    
    db_text = """
    <b>Nowe kolumny dodane dla workflow:</b><br/>
    • <b>zawodnicy.checked_in</b> (BOOLEAN) - status zameldowania<br/>
    • <b>zawodnicy.check_in_time</b> (TIMESTAMP) - czas zameldowania<br/>
    • <b>zawodnicy.qr_code</b> (VARCHAR) - unikalny kod QR<br/><br/>
    
    <b>Tabela checkpoints (nowa):</b><br/>
    • <b>id</b> (SERIAL PRIMARY KEY) - identyfikator<br/>
    • <b>nr_startowy</b> (INTEGER) - FK do zawodnicy<br/>
    • <b>checkpoint_name</b> (VARCHAR) - typ checkpointu<br/>
    • <b>timestamp</b> (TIMESTAMP) - czas skanowania<br/>
    • <b>device_id</b> (VARCHAR) - identyfikator urządzenia<br/>
    • <b>qr_code</b> (VARCHAR) - zeskanowany kod
    """
    story.append(Paragraph(db_text, normal_style))
    story.append(Spacer(1, 20))
    
    # === 9. ROZWIĄZYWANIE PROBLEMÓW ===
    story.append(Paragraph("9. ROZWIĄZYWANIE PROBLEMÓW", heading_style))
    
    # Tabela problemów
    troubleshooting_data = [
        ['PROBLEM', 'ROZWIĄZANIE'],
        ['Brak grup startowych', 'Sprawdź czy zawodnicy są zameldowani (checked_in=TRUE)'],
        ['QR kod nie działa', 'Sprawdź format: SKATECROSS_NR_HASH (8 znaków hash)'],
        ['Błąd "nie zameldowany"', 'Zawodnik musi przejść check-in w biurze zawodów'],
        ['Kolejka startowa pusta', 'Zawodnicy muszą być zweryfikowani na linii startu'],
        ['Port 5000 zajęty', 'Użyj: PORT=5001 python3 api_server.py'],
        ['Frontend nie ładuje się', 'Sprawdź czy npm run dev działa i port 5174 dostępny'],
        ['Polskie znaki nie wyświetlają się', 'Sprawdź encoding UTF-8 w przeglądarce'],
        ['Błąd bazy danych', 'Sprawdź połączenie PostgreSQL i tabele checkpoints']
    ]
    
    troubleshooting_table = Table(troubleshooting_data, colWidths=[7*cm, 8*cm])
    troubleshooting_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#dc2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_FAMILY_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_FAMILY),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fef2f2')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#fca5a5')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(troubleshooting_table)
    story.append(Spacer(1, 30))
    
    # === FOOTER ===
    footer_text = """
    <b>SKATECROSS Dashboard</b> - System workflow zawodów<br/>
    Wersja 2.0 z ulepszonym formatowaniem<br/>
    © 2024 - System zarządzania zawodami skatecross
    """
    footer_style = ParagraphStyle(
        'Footer', 
        parent=styles['Normal'], 
        fontSize=9, 
        alignment=TA_CENTER, 
        textColor=HexColor('#6b7280'),
        fontName=FONT_FAMILY,
        spaceAfter=0,
        spaceBefore=20
    )
    story.append(Paragraph(footer_text, footer_style))
    
    # Budowanie PDF
    doc.build(story)
    return filename

if __name__ == "__main__":
    filename = create_workflow_pdf()
    print(f"✅ PDF wygenerowany: {filename}")
    print(f"📄 Lokalizacja: {os.path.abspath(filename)}")
    
    # Sprawdzenie rozmiaru pliku
    if os.path.exists(filename):
        size_kb = os.path.getsize(filename) / 1024
        print(f"📊 Rozmiar pliku: {size_kb:.1f} KB")
        print(f"🎯 Używane fonty: {FONT_FAMILY} (standardowe)") 