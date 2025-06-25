# -*- coding: utf-8 -*-
"""
SKATECROSS QR - System Import/Export
Wersja: 2.0.0
Obsługa importu i eksportu danych zawodników, wyników i rankingów
"""

import pandas as pd
import json
import csv
import io
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Union
import logging
from pathlib import Path
import traceback
from dataclasses import dataclass, asdict
from utils.database import execute_query, get_all
from utils.api_response import APIResponse

# === KONFIGURACJA ===

logger = logging.getLogger(__name__)

@dataclass
class ImportResult:
    """Wynik operacji importu"""
    success: bool
    records_processed: int
    records_imported: int
    records_updated: int
    records_skipped: int
    errors: List[str]
    warnings: List[str]
    execution_time: float

@dataclass
class ExportResult:
    """Wynik operacji eksportu"""
    success: bool
    records_exported: int
    file_size: int
    file_path: Optional[str]
    format: str
    execution_time: float

# === KLASA GŁÓWNA ===

class ImportExportManager:
    """Główna klasa do zarządzania importem i eksportem"""
    
    SUPPORTED_FORMATS = ['csv', 'xlsx', 'json']
    
    # Mapowanie kolumn CSV na kolumny bazy danych
    COLUMN_MAPPING = {
        'nr_startowy': 'nr_startowy',
        'numer_startowy': 'nr_startowy',
        'start_number': 'nr_startowy',
        'imie': 'imie',
        'imię': 'imie',
        'first_name': 'imie',
        'nazwisko': 'nazwisko',
        'last_name': 'nazwisko',
        'surname': 'nazwisko',
        'kategoria': 'kategoria',
        'category': 'kategoria',
        'plec': 'plec',
        'płeć': 'plec',
        'sex': 'plec',
        'gender': 'plec',
        'klub': 'klub',
        'club': 'klub',
        'team': 'klub',
        'email': 'email',
        'telefon': 'telefon',
        'phone': 'telefon',
        'data_urodzenia': 'data_urodzenia',
        'date_of_birth': 'data_urodzenia',
        'birth_date': 'data_urodzenia',
        'urodziny': 'data_urodzenia',
    }
    
    REQUIRED_FIELDS = ['nr_startowy', 'imie', 'nazwisko']
    
    def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id or 'system'
    
    # === IMPORT ZAWODNIKÓW ===
    
    def import_zawodnicy_from_file(
        self, 
        file_path: str, 
        format: str, 
        update_existing: bool = True,
        validate_only: bool = False
    ) -> ImportResult:
        """
        Import zawodników z pliku
        
        Args:
            file_path: Ścieżka do pliku
            format: Format pliku (csv, xlsx, json)
            update_existing: Czy aktualizować istniejących zawodników
            validate_only: Tylko walidacja bez zapisywania
        """
        start_time = datetime.now()
        
        try:
            # Walidacja formatu
            if format not in self.SUPPORTED_FORMATS:
                return ImportResult(
                    success=False,
                    records_processed=0,
                    records_imported=0,
                    records_updated=0,
                    records_skipped=0,
                    errors=[f"Nieobsługiwany format: {format}"],
                    warnings=[],
                    execution_time=0
                )
            
            # Wczytaj dane
            if format == 'csv':
                data = self._read_csv(file_path)
            elif format == 'xlsx':
                data = self._read_excel(file_path)
            elif format == 'json':
                data = self._read_json(file_path)
            
            if data is None:
                return ImportResult(
                    success=False,
                    records_processed=0,
                    records_imported=0,
                    records_updated=0,
                    records_skipped=0,
                    errors=["Nie udało się wczytać danych z pliku"],
                    warnings=[],
                    execution_time=0
                )
            
            # Przetwórz dane
            result = self._process_zawodnicy_data(data, update_existing, validate_only)
            
            # Zapisz log operacji
            if not validate_only:
                self._log_import_operation(
                    file_path=file_path,
                    format=format,
                    table='zawodnicy',
                    result=result
                )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Błąd importu: {e}")
            return ImportResult(
                success=False,
                records_processed=0,
                records_imported=0,
                records_updated=0,
                records_skipped=0,
                errors=[f"Błąd importu: {str(e)}"],
                warnings=[],
                execution_time=execution_time
            )
    
    def _read_csv(self, file_path: str) -> Optional[pd.DataFrame]:
        """Wczytuje dane z pliku CSV"""
        try:
            # Spróbuj różne kodowania
            encodings = ['utf-8', 'cp1250', 'iso-8859-2']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    logger.info(f"CSV wczytany z kodowaniem: {encoding}")
                    return df
                except UnicodeDecodeError:
                    continue
            
            # Jeśli nic nie zadziałało, spróbuj automatyczne wykrywanie
            df = pd.read_csv(file_path)
            return df
            
        except Exception as e:
            logger.error(f"Błąd wczytywania CSV: {e}")
            return None
    
    def _read_excel(self, file_path: str) -> Optional[pd.DataFrame]:
        """Wczytuje dane z pliku Excel"""
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            return df
        except Exception as e:
            logger.error(f"Błąd wczytywania Excel: {e}")
            return None
    
    def _read_json(self, file_path: str) -> Optional[pd.DataFrame]:
        """Wczytuje dane z pliku JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict) and 'data' in data:
                df = pd.DataFrame(data['data'])
            else:
                df = pd.DataFrame([data])
            
            return df
        except Exception as e:
            logger.error(f"Błąd wczytywania JSON: {e}")
            return None
    
    def _process_zawodnicy_data(
        self, 
        df: pd.DataFrame, 
        update_existing: bool,
        validate_only: bool
    ) -> ImportResult:
        """Przetwarza dane zawodników"""
        
        records_processed = 0
        records_imported = 0
        records_updated = 0
        records_skipped = 0
        errors = []
        warnings = []
        
        # Normalizuj nazwy kolumn
        df = self._normalize_column_names(df)
        
        # Sprawdź wymagane kolumny
        missing_fields = [field for field in self.REQUIRED_FIELDS if field not in df.columns]
        if missing_fields:
            return ImportResult(
                success=False,
                records_processed=0,
                records_imported=0,
                records_updated=0,
                records_skipped=0,
                errors=[f"Brakuje wymaganych kolumn: {missing_fields}"],
                warnings=[],
                execution_time=0
            )
        
        # Przetwórz każdy wiersz
        for index, row in df.iterrows():
            records_processed += 1
            
            try:
                # Walidacja i czyszczenie danych
                clean_data, row_errors = self._validate_and_clean_zawodnik_data(row, index + 1)
                
                if row_errors:
                    errors.extend(row_errors)
                    records_skipped += 1
                    continue
                
                if validate_only:
                    continue
                
                # Sprawdź czy zawodnik już istnieje
                existing = get_all(
                    "SELECT nr_startowy FROM zawodnicy WHERE nr_startowy = %s",
                    (clean_data['nr_startowy'],)
                )
                
                if existing:
                    if update_existing:
                        # Aktualizuj istniejącego zawodnika
                        self._update_zawodnik(clean_data)
                        records_updated += 1
                    else:
                        warnings.append(f"Wiersz {index + 1}: Zawodnik nr {clean_data['nr_startowy']} już istnieje - pominięto")
                        records_skipped += 1
                else:
                    # Dodaj nowego zawodnika
                    self._insert_zawodnik(clean_data)
                    records_imported += 1
                    
            except Exception as e:
                error_msg = f"Wiersz {index + 1}: Błąd przetwarzania - {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
                records_skipped += 1
        
        success = len(errors) == 0 or (records_imported + records_updated) > 0
        
        return ImportResult(
            success=success,
            records_processed=records_processed,
            records_imported=records_imported,
            records_updated=records_updated,
            records_skipped=records_skipped,
            errors=errors,
            warnings=warnings,
            execution_time=0  # Will be set by caller
        )
    
    def _normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalizuje nazwy kolumn używając mapowania"""
        normalized_columns = {}
        
        for col in df.columns:
            col_lower = str(col).strip().lower()
            if col_lower in self.COLUMN_MAPPING:
                normalized_columns[col] = self.COLUMN_MAPPING[col_lower]
            else:
                normalized_columns[col] = col
        
        return df.rename(columns=normalized_columns)
    
    def _validate_and_clean_zawodnik_data(
        self, 
        row: pd.Series, 
        row_number: int
    ) -> tuple[Dict[str, Any], List[str]]:
        """Waliduje i czyści dane zawodnika"""
        
        errors = []
        clean_data = {}
        
        # Nr startowy (wymagany)
        try:
            nr_startowy = int(row['nr_startowy'])
            if nr_startowy <= 0:
                errors.append(f"Wiersz {row_number}: Nr startowy musi być większy od 0")
            else:
                clean_data['nr_startowy'] = nr_startowy
        except (ValueError, TypeError):
            errors.append(f"Wiersz {row_number}: Nieprawidłowy nr startowy")
        
        # Imię (wymagane)
        imie = str(row['imie']).strip() if pd.notna(row['imie']) else ''
        if not imie:
            errors.append(f"Wiersz {row_number}: Imię jest wymagane")
        else:
            clean_data['imie'] = imie[:50]  # Ograniczenie długości
        
        # Nazwisko (wymagane)
        nazwisko = str(row['nazwisko']).strip() if pd.notna(row['nazwisko']) else ''
        if not nazwisko:
            errors.append(f"Wiersz {row_number}: Nazwisko jest wymagane")
        else:
            clean_data['nazwisko'] = nazwisko[:50]
        
        # Kategoria (opcjonalna)
        if 'kategoria' in row and pd.notna(row['kategoria']):
            clean_data['kategoria'] = str(row['kategoria']).strip()[:20]
        
        # Płeć (opcjonalna, walidacja)
        if 'plec' in row and pd.notna(row['plec']):
            plec = str(row['plec']).strip().upper()
            if plec in ['M', 'K', 'I']:
                clean_data['plec'] = plec
            elif plec in ['MĘŻCZYZNA', 'MĘSKI', 'MALE']:
                clean_data['plec'] = 'M'
            elif plec in ['KOBIETA', 'ŻEŃSKI', 'FEMALE']:
                clean_data['plec'] = 'K'
            else:
                warnings.append(f"Wiersz {row_number}: Nierozpoznana płeć '{plec}' - ustawiono domyślnie")
        
        # Klub (opcjonalny)
        if 'klub' in row and pd.notna(row['klub']):
            clean_data['klub'] = str(row['klub']).strip()[:100]
        
        # Email (opcjonalny, walidacja)
        if 'email' in row and pd.notna(row['email']):
            email = str(row['email']).strip()
            if '@' in email and '.' in email:
                clean_data['email'] = email[:255]
            else:
                errors.append(f"Wiersz {row_number}: Nieprawidłowy format email")
        
        # Data urodzenia (opcjonalna)
        if 'data_urodzenia' in row and pd.notna(row['data_urodzenia']):
            try:
                if isinstance(row['data_urodzenia'], (datetime, date)):
                    clean_data['data_urodzenia'] = row['data_urodzenia']
                else:
                    # Spróbuj różne formaty dat
                    date_str = str(row['data_urodzenia'])
                    for date_format in ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y']:
                        try:
                            clean_data['data_urodzenia'] = datetime.strptime(date_str, date_format).date()
                            break
                        except ValueError:
                            continue
                    else:
                        errors.append(f"Wiersz {row_number}: Nieprawidłowy format daty urodzenia")
            except:
                errors.append(f"Wiersz {row_number}: Błąd przetwarzania daty urodzenia")
        
        return clean_data, errors
    
    def _insert_zawodnik(self, data: Dict[str, Any]):
        """Wstawia nowego zawodnika do bazy"""
        
        columns = list(data.keys())
        placeholders = ', '.join(['%s'] * len(columns))
        values = list(data.values())
        
        query = f"""
            INSERT INTO zawodnicy ({', '.join(columns)}) 
            VALUES ({placeholders})
        """
        
        execute_query(query, values)
    
    def _update_zawodnik(self, data: Dict[str, Any]):
        """Aktualizuje istniejącego zawodnika"""
        
        nr_startowy = data.pop('nr_startowy')
        
        if not data:  # Jeśli nie ma danych do aktualizacji
            return
        
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        values = list(data.values()) + [nr_startowy]
        
        query = f"""
            UPDATE zawodnicy 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE nr_startowy = %s
        """
        
        execute_query(query, values)
    
    # === EXPORT ZAWODNIKÓW ===
    
    def export_zawodnicy_to_file(
        self,
        file_path: str,
        format: str,
        filters: Optional[Dict[str, Any]] = None,
        columns: Optional[List[str]] = None
    ) -> ExportResult:
        """
        Eksport zawodników do pliku
        
        Args:
            file_path: Ścieżka docelowa
            format: Format pliku (csv, xlsx, json)
            filters: Filtry do zastosowania
            columns: Kolumny do eksportu
        """
        start_time = datetime.now()
        
        try:
            # Pobierz dane
            data = self._get_zawodnicy_for_export(filters, columns)
            
            if not data:
                return ExportResult(
                    success=False,
                    records_exported=0,
                    file_size=0,
                    file_path=None,
                    format=format,
                    execution_time=0
                )
            
            # Eksportuj w odpowiednim formacie
            if format == 'csv':
                success = self._export_to_csv(data, file_path)
            elif format == 'xlsx':
                success = self._export_to_excel(data, file_path)
            elif format == 'json':
                success = self._export_to_json(data, file_path)
            else:
                success = False
            
            if success:
                file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
                
                # Zapisz log operacji
                self._log_export_operation(
                    file_path=file_path,
                    format=format,
                    table='zawodnicy',
                    records_count=len(data),
                    file_size=file_size
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return ExportResult(
                    success=True,
                    records_exported=len(data),
                    file_size=file_size,
                    file_path=file_path,
                    format=format,
                    execution_time=execution_time
                )
            else:
                return ExportResult(
                    success=False,
                    records_exported=0,
                    file_size=0,
                    file_path=None,
                    format=format,
                    execution_time=0
                )
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Błąd eksportu: {e}")
            return ExportResult(
                success=False,
                records_exported=0,
                file_size=0,
                file_path=None,
                format=format,
                execution_time=execution_time
            )
    
    def _get_zawodnicy_for_export(
        self,
        filters: Optional[Dict[str, Any]] = None,
        columns: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Pobiera dane zawodników do eksportu"""
        
        # Domyślne kolumny
        if columns is None:
            columns = [
                'nr_startowy', 'imie', 'nazwisko', 'kategoria', 'plec', 
                'klub', 'email', 'telefon', 'data_urodzenia', 'checked_in'
            ]
        
        # Buduj zapytanie
        query = f"SELECT {', '.join(columns)} FROM zawodnicy WHERE 1=1"
        params = []
        
        # Dodaj filtry
        if filters:
            if 'kategoria' in filters:
                query += " AND kategoria = %s"
                params.append(filters['kategoria'])
            
            if 'plec' in filters:
                query += " AND plec = %s"
                params.append(filters['plec'])
            
            if 'klub' in filters:
                query += " AND klub = %s"
                params.append(filters['klub'])
            
            if 'checked_in' in filters:
                query += " AND checked_in = %s"
                params.append(filters['checked_in'])
        
        query += " ORDER BY nr_startowy"
        
        return get_all(query, params)
    
    def _export_to_csv(self, data: List[Dict], file_path: str) -> bool:
        """Eksportuje do CSV"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding='utf-8-sig')  # BOM dla Excel
            return True
        except Exception as e:
            logger.error(f"Błąd eksportu CSV: {e}")
            return False
    
    def _export_to_excel(self, data: List[Dict], file_path: str) -> bool:
        """Eksportuje do Excel"""
        try:
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            return True
        except Exception as e:
            logger.error(f"Błąd eksportu Excel: {e}")
            return False
    
    def _export_to_json(self, data: List[Dict], file_path: str) -> bool:
        """Eksportuje do JSON"""
        try:
            # Konwertuj daty do string
            processed_data = []
            for record in data:
                processed_record = {}
                for key, value in record.items():
                    if isinstance(value, (date, datetime)):
                        processed_record[key] = value.isoformat()
                    else:
                        processed_record[key] = value
                processed_data.append(processed_record)
            
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'format': 'json',
                'records_count': len(processed_data),
                'data': processed_data
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"Błąd eksportu JSON: {e}")
            return False
    
    # === LOGGING ===
    
    def _log_import_operation(
        self,
        file_path: str,
        format: str,
        table: str,
        result: ImportResult
    ):
        """Loguje operację importu"""
        try:
            file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
            
            execute_query("""
                INSERT INTO import_export_logs 
                (typ, format, tabela, nazwa_pliku, rozmiar_pliku, liczba_rekordow, 
                 status, bledy, ostrzezenia, metadane, user_id, czas_koniec)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'import',
                format,
                table,
                Path(file_path).name,
                file_size,
                result.records_imported + result.records_updated,
                'sukces' if result.success else 'bledny',
                json.dumps(result.errors),
                json.dumps(result.warnings),
                json.dumps({
                    'records_processed': result.records_processed,
                    'records_imported': result.records_imported,
                    'records_updated': result.records_updated,
                    'records_skipped': result.records_skipped,
                    'execution_time': result.execution_time
                }),
                self.user_id,
                datetime.now()
            ))
        except Exception as e:
            logger.error(f"Błąd logowania importu: {e}")
    
    def _log_export_operation(
        self,
        file_path: str,
        format: str,
        table: str,
        records_count: int,
        file_size: int
    ):
        """Loguje operację eksportu"""
        try:
            execute_query("""
                INSERT INTO import_export_logs 
                (typ, format, tabela, nazwa_pliku, rozmiar_pliku, liczba_rekordow, 
                 status, user_id, czas_koniec)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                'export',
                format,
                table,
                Path(file_path).name,
                file_size,
                records_count,
                'sukces',
                self.user_id,
                datetime.now()
            ))
        except Exception as e:
            logger.error(f"Błąd logowania eksportu: {e}")

# === POMOCNICZE FUNKCJE ===

def get_import_export_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Pobiera historię operacji import/export"""
    return get_all("""
        SELECT id, typ, format, tabela, nazwa_pliku, rozmiar_pliku, 
               liczba_rekordow, status, user_id, czas_start, czas_koniec
        FROM import_export_logs
        ORDER BY czas_start DESC
        LIMIT %s
    """, (limit,))

def validate_file_format(file_path: str) -> tuple[bool, str, str]:
    """
    Waliduje format pliku
    
    Returns:
        (is_valid, format, error_message)
    """
    if not Path(file_path).exists():
        return False, '', 'Plik nie istnieje'
    
    extension = Path(file_path).suffix.lower()
    
    if extension == '.csv':
        return True, 'csv', ''
    elif extension in ['.xlsx', '.xls']:
        return True, 'xlsx', ''
    elif extension == '.json':
        return True, 'json', ''
    else:
        return False, '', f'Nieobsługiwany format pliku: {extension}'

# === PRZYKŁAD UŻYCIA ===

if __name__ == "__main__":
    # Przykład importu
    manager = ImportExportManager(user_id='admin')
    
    # Import z CSV
    result = manager.import_zawodnicy_from_file(
        file_path='zawodnicy.csv',
        format='csv',
        update_existing=True
    )
    
    print(f"Import result: {asdict(result)}")
    
    # Eksport do Excel
    export_result = manager.export_zawodnicy_to_file(
        file_path='export_zawodnicy.xlsx',
        format='xlsx',
        filters={'kategoria': 'Junior A'}
    )
    
    print(f"Export result: {asdict(export_result)}") 