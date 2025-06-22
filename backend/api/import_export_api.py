# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Import/Export API
Wersja: 2.0.0
Endpointy API dla operacji import/export danych
"""

from flask import Blueprint, request, send_file, jsonify
import os
import tempfile
from datetime import datetime
from typing import Dict, Any
import traceback
from pathlib import Path
import json

from utils.api_response import APIResponse, handle_api_errors, ErrorCodes
from utils.import_export import ImportExportManager, validate_file_format, get_import_export_history
from utils.database import get_all

import_export_bp = Blueprint('import_export', __name__)

# === KONFIGURACJA ===

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
EXPORT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'exports')

# Utwórz foldery jeśli nie istnieją
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Sprawdza czy rozszerzenie pliku jest dozwolone"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_id():
    """Pobiera ID użytkownika z sesji/kontekstu"""
    # TODO: Implementacja autentykacji
    return request.headers.get('X-User-ID', 'anonymous')

# === ENDPOINTY IMPORTU ===

@import_export_bp.route('/api/import/upload', methods=['POST'])
@handle_api_errors
def upload_file_for_import():
    """
    Upload pliku do importu
    POST /api/import/upload
    """
    if 'file' not in request.files:
        return APIResponse.validation_error("Brak pliku w żądaniu")
    
    file = request.files['file']
    
    if file.filename == '':
        return APIResponse.validation_error("Nie wybrano pliku")
    
    if not allowed_file(file.filename):
        return APIResponse.validation_error(
            f"Niedozwolone rozszerzenie pliku. Dozwolone: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Sprawdź rozmiar pliku
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return APIResponse.validation_error(
            f"Plik zbyt duży. Maksymalny rozmiar: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Zapisz plik
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Waliduj format
    is_valid, format_type, error_msg = validate_file_format(file_path)
    
    if not is_valid:
        os.remove(file_path)  # Usuń nieprawidłowy plik
        return APIResponse.validation_error(error_msg)
    
    return APIResponse.success(
        data={
            'file_id': filename,
            'original_name': file.filename,
            'file_size': file_size,
            'format': format_type,
            'upload_path': file_path
        },
        message="Plik przesłany pomyślnie"
    )

@import_export_bp.route('/api/import/validate', methods=['POST'])
@handle_api_errors
def validate_import_file():
    """
    Walidacja pliku przed importem
    POST /api/import/validate
    Body: {
        "file_id": "filename",
        "table": "zawodnicy",
        "options": {...}
    }
    """
    data = request.get_json()
    
    if not data or 'file_id' not in data:
        return APIResponse.validation_error("Brak file_id w żądaniu")
    
    file_id = data['file_id']
    table = data.get('table', 'zawodnicy')
    options = data.get('options', {})
    
    # Sprawdź czy plik istnieje
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    if not os.path.exists(file_path):
        return APIResponse.not_found("Plik", file_id)
    
    # Wykryj format
    is_valid, format_type, error_msg = validate_file_format(file_path)
    if not is_valid:
        return APIResponse.validation_error(error_msg)
    
    # Walidacja tylko dla zawodników
    if table != 'zawodnicy':
        return APIResponse.validation_error("Obsługiwana jest tylko tabela 'zawodnicy'")
    
    # Wykonaj walidację
    manager = ImportExportManager(user_id=get_user_id())
    result = manager.import_zawodnicy_from_file(
        file_path=file_path,
        format=format_type,
        update_existing=options.get('update_existing', True),
        validate_only=True
    )
    
    return APIResponse.success(
        data={
            'validation_result': {
                'is_valid': result.success,
                'records_processed': result.records_processed,
                'errors': result.errors,
                'warnings': result.warnings,
                'execution_time': result.execution_time
            },
            'file_info': {
                'file_id': file_id,
                'format': format_type,
                'table': table
            },
            'import_preview': {
                'will_import': result.records_processed - len(result.errors),
                'will_skip': len(result.errors),
                'estimated_time': result.execution_time * 2  # Szacowany czas importu
            }
        },
        message="Walidacja zakończona"
    )

@import_export_bp.route('/api/import/execute', methods=['POST'])
@handle_api_errors
def execute_import():
    """
    Wykonanie importu danych
    POST /api/import/execute
    Body: {
        "file_id": "filename",
        "table": "zawodnicy",
        "options": {
            "update_existing": true,
            "skip_errors": false
        }
    }
    """
    data = request.get_json()
    
    if not data or 'file_id' not in data:
        return APIResponse.validation_error("Brak file_id w żądaniu")
    
    file_id = data['file_id']
    table = data.get('table', 'zawodnicy')
    options = data.get('options', {})
    
    # Sprawdź czy plik istnieje
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    if not os.path.exists(file_path):
        return APIResponse.not_found("Plik", file_id)
    
    # Wykryj format
    is_valid, format_type, error_msg = validate_file_format(file_path)
    if not is_valid:
        return APIResponse.validation_error(error_msg)
    
    # Import tylko dla zawodników
    if table != 'zawodnicy':
        return APIResponse.validation_error("Obsługiwana jest tylko tabela 'zawodnicy'")
    
    # Wykonaj import
    manager = ImportExportManager(user_id=get_user_id())
    result = manager.import_zawodnicy_from_file(
        file_path=file_path,
        format=format_type,
        update_existing=options.get('update_existing', True),
        validate_only=False
    )
    
    # Usuń plik po imporcie (opcjonalnie)
    if options.get('delete_after_import', True):
        try:
            os.remove(file_path)
        except:
            pass  # Ignoruj błędy usuwania
    
    if result.success:
        return APIResponse.success(
            data={
                'import_result': {
                    'success': result.success,
                    'records_processed': result.records_processed,
                    'records_imported': result.records_imported,
                    'records_updated': result.records_updated,
                    'records_skipped': result.records_skipped,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'execution_time': result.execution_time
                },
                'summary': {
                    'total_affected': result.records_imported + result.records_updated,
                    'success_rate': round(
                        (result.records_imported + result.records_updated) / max(result.records_processed, 1) * 100, 2
                    )
                }
            },
            message=f"Import zakończony. Przetworzono {result.records_imported + result.records_updated} rekordów."
        )
    else:
        return APIResponse.error(
            message="Import zakończony z błędami",
            code=ErrorCodes.VALIDATION_ERROR,
            data={
                'import_result': {
                    'success': result.success,
                    'records_processed': result.records_processed,
                    'records_imported': result.records_imported,
                    'records_updated': result.records_updated,
                    'records_skipped': result.records_skipped,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'execution_time': result.execution_time
                }
            },
            status_code=400
        )

# === ENDPOINTY EKSPORTU ===

@import_export_bp.route('/api/export/zawodnicy', methods=['POST'])
@handle_api_errors
def export_zawodnicy():
    """
    Eksport zawodników do pliku
    POST /api/export/zawodnicy
    Body: {
        "format": "csv|xlsx|json",
        "filters": {
            "kategoria": "Junior A",
            "plec": "M",
            "klub": "RC Warszawa",
            "checked_in": true
        },
        "columns": ["nr_startowy", "imie", "nazwisko", ...]
    }
    """
    data = request.get_json() or {}
    
    format_type = data.get('format', 'csv').lower()
    if format_type not in ['csv', 'xlsx', 'json']:
        return APIResponse.validation_error(
            f"Nieobsługiwany format eksportu: {format_type}. Dostępne: csv, xlsx, json"
        )
    
    filters = data.get('filters', {})
    columns = data.get('columns')
    
    # Wygeneruj nazwę pliku
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"zawodnicy_export_{timestamp}.{format_type}"
    file_path = os.path.join(EXPORT_FOLDER, filename)
    
    # Wykonaj eksport
    manager = ImportExportManager(user_id=get_user_id())
    result = manager.export_zawodnicy_to_file(
        file_path=file_path,
        format=format_type,
        filters=filters,
        columns=columns
    )
    
    if result.success:
        return APIResponse.success(
            data={
                'export_result': {
                    'success': result.success,
                    'records_exported': result.records_exported,
                    'file_size': result.file_size,
                    'format': result.format,
                    'execution_time': result.execution_time
                },
                'download': {
                    'filename': filename,
                    'download_url': f'/api/export/download/{filename}',
                    'file_size_mb': round(result.file_size / (1024*1024), 2)
                }
            },
            message=f"Eksport zakończony. Wyeksportowano {result.records_exported} rekordów."
        )
    else:
        return APIResponse.internal_error(
            Exception("Błąd podczas eksportu danych")
        )

@import_export_bp.route('/api/export/download/<filename>', methods=['GET'])
def download_export_file(filename):
    """
    Pobieranie wyeksportowanego pliku
    GET /api/export/download/{filename}
    """
    try:
        file_path = os.path.join(EXPORT_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Plik nie został znaleziony'}), 404
        
        # Sprawdź czy plik nie jest za stary (24h)
        file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
        if file_age > 24 * 3600:  # 24 godziny
            os.remove(file_path)
            return jsonify({'error': 'Plik wygasł'}), 410
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === ENDPOINTY ZARZĄDZANIA ===

@import_export_bp.route('/api/import-export/history', methods=['GET'])
@handle_api_errors
def get_operations_history():
    """
    Historia operacji import/export
    GET /api/import-export/history?limit=50
    """
    limit = request.args.get('limit', 50, type=int)
    limit = min(max(limit, 1), 200)  # Ograniczenie 1-200
    
    history = get_import_export_history(limit)
    
    return APIResponse.success(
        data=history,
        count=len(history),
        message="Historia operacji pobrana pomyślnie"
    )

@import_export_bp.route('/api/import-export/cleanup', methods=['POST'])
@handle_api_errors
def cleanup_old_files():
    """
    Czyszczenie starych plików
    POST /api/import-export/cleanup
    Body: {
        "max_age_hours": 24,
        "dry_run": false
    }
    """
    data = request.get_json() or {}
    max_age_hours = data.get('max_age_hours', 24)
    dry_run = data.get('dry_run', False)
    
    current_time = datetime.now().timestamp()
    max_age_seconds = max_age_hours * 3600
    
    cleaned_files = []
    total_size_freed = 0
    
    # Czyść folder uploads
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                file_size = os.path.getsize(file_path)
                if not dry_run:
                    os.remove(file_path)
                cleaned_files.append({
                    'filename': filename,
                    'folder': 'uploads',
                    'age_hours': round(file_age / 3600, 1),
                    'size_bytes': file_size
                })
                total_size_freed += file_size
    
    # Czyść folder exports
    for filename in os.listdir(EXPORT_FOLDER):
        file_path = os.path.join(EXPORT_FOLDER, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                file_size = os.path.getsize(file_path)
                if not dry_run:
                    os.remove(file_path)
                cleaned_files.append({
                    'filename': filename,
                    'folder': 'exports',
                    'age_hours': round(file_age / 3600, 1),
                    'size_bytes': file_size
                })
                total_size_freed += file_size
    
    return APIResponse.success(
        data={
            'cleanup_result': {
                'files_cleaned': len(cleaned_files),
                'total_size_freed_mb': round(total_size_freed / (1024*1024), 2),
                'max_age_hours': max_age_hours,
                'dry_run': dry_run
            },
            'cleaned_files': cleaned_files
        },
        message=f"{'Symulacja' if dry_run else 'Operacja'} czyszczenia zakończona. "
                f"{'Zostałoby usuniętych' if dry_run else 'Usunięto'} {len(cleaned_files)} plików."
    )

@import_export_bp.route('/api/import-export/templates', methods=['GET'])
@handle_api_errors
def get_import_templates():
    """
    Szablony plików do importu
    GET /api/import-export/templates?format=csv
    """
    format_type = request.args.get('format', 'csv').lower()
    
    if format_type not in ['csv', 'xlsx', 'json']:
        return APIResponse.validation_error(
            f"Nieobsługiwany format: {format_type}"
        )
    
    # Definicja pól dla zawodników
    template_fields = {
        'nr_startowy': {
            'required': True,
            'type': 'integer',
            'description': 'Numer startowy zawodnika (unikalny)'
        },
        'imie': {
            'required': True,
            'type': 'string',
            'description': 'Imię zawodnika'
        },
        'nazwisko': {
            'required': True,
            'type': 'string',
            'description': 'Nazwisko zawodnika'
        },
        'kategoria': {
            'required': False,
            'type': 'string',
            'description': 'Kategoria wiekowa (np. Junior A, Senior)'
        },
        'plec': {
            'required': False,
            'type': 'string',
            'description': 'Płeć: M (mężczyzna), K (kobieta), I (inne)',
            'allowed_values': ['M', 'K', 'I']
        },
        'klub': {
            'required': False,
            'type': 'string',
            'description': 'Nazwa klubu'
        },
        'email': {
            'required': False,
            'type': 'string',
            'description': 'Adres email'
        },
        'telefon': {
            'required': False,
            'type': 'string',
            'description': 'Numer telefonu'
        },
        'data_urodzenia': {
            'required': False,
            'type': 'date',
            'description': 'Data urodzenia (format: YYYY-MM-DD)',
            'example': '1990-01-15'
        }
    }
    
    # Przykładowe dane
    example_data = [
        {
            'nr_startowy': 1,
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'kategoria': 'Senior',
            'plec': 'M',
            'klub': 'RC Warszawa',
            'email': 'jan.kowalski@example.com',
            'telefon': '123456789',
            'data_urodzenia': '1990-05-15'
        },
        {
            'nr_startowy': 2,
            'imie': 'Anna',
            'nazwisko': 'Nowak',
            'kategoria': 'Junior A',
            'plec': 'K',
            'klub': 'RC Kraków',
            'email': 'anna.nowak@example.com',
            'telefon': '987654321',
            'data_urodzenia': '2005-08-22'
        }
    ]
    
    return APIResponse.success(
        data={
            'template_info': {
                'format': format_type,
                'table': 'zawodnicy',
                'description': 'Szablon do importu zawodników'
            },
            'fields': template_fields,
            'example_data': example_data,
            'download_url': f'/api/import-export/templates/download?format={format_type}',
            'import_notes': [
                'Pola nr_startowy, imie i nazwisko są wymagane',
                'Nr startowy musi być unikalny',
                'Płeć: M=mężczyzna, K=kobieta, I=inne',
                'Data urodzenia w formacie YYYY-MM-DD',
                'Maksymalny rozmiar pliku: 10MB'
            ]
        },
        message="Szablon importu pobrany pomyślnie"
    )

@import_export_bp.route('/api/import-export/templates/download', methods=['GET'])
def download_import_template():
    """
    Pobieranie szablonu do importu
    GET /api/import-export/templates/download?format=csv
    """
    format_type = request.args.get('format', 'csv').lower()
    
    if format_type not in ['csv', 'xlsx']:
        return jsonify({'error': 'Nieobsługiwany format szablonu'}), 400
    
    # Dane szablonu
    template_data = [
        {
            'nr_startowy': 1,
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'kategoria': 'Senior',
            'plec': 'M',
            'klub': 'RC Warszawa',
            'email': 'jan.kowalski@example.com',
            'telefon': '123456789',
            'data_urodzenia': '1990-05-15'
        }
    ]
    
    try:
        # Utwórz plik tymczasowy
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format_type}') as tmp_file:
            if format_type == 'csv':
                import pandas as pd
                df = pd.DataFrame(template_data)
                df.to_csv(tmp_file.name, index=False, encoding='utf-8-sig')
                mimetype = 'text/csv'
            elif format_type == 'xlsx':
                import pandas as pd
                df = pd.DataFrame(template_data)
                df.to_excel(tmp_file.name, index=False, engine='openpyxl')
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name=f'szablon_zawodnicy.{format_type}',
                mimetype=mimetype
            )
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

print("📊 SKATECROSS QR - Moduł Import/Export API załadowany") 