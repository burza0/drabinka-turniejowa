#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

def analyze_database():
    """Analizuje bazę danych pod kątem wydajności"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    print('🔍 ANALIZA WYDAJNOŚCI BAZY DANYCH')
    print('=' * 50)

    # Sprawdź istniejące indeksy
    print('\n📊 ISTNIEJĄCE INDEKSY:')
    cur.execute('''
        SELECT 
            schemaname, tablename, indexname, indexdef
        FROM pg_indexes 
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname;
    ''')

    for row in cur.fetchall():
        print(f'  {row[1]}.{row[2]}: {row[3]}')

    # Rozmiary tabel
    print('\n📏 ROZMIARY TABEL:')
    cur.execute('''
        SELECT 
            schemaname, tablename, 
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
            pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
    ''')

    for row in cur.fetchall():
        print(f'  {row[1]}: {row[2]}')

    # Statystyki tabel
    print('\n📈 LICZBA REKORDÓW:')
    tables = ['zawodnicy', 'wyniki', 'checkpoints', 'kluby']
    for table in tables:
        try:
            cur.execute(f'SELECT COUNT(*) FROM {table}')
            count = cur.fetchone()[0]
            print(f'  {table}: {count:,} rekordów')
        except:
            print(f'  {table}: tabela nie istnieje')

    # Sprawdź najczęściej używane zapytania (analysis)
    print('\n🔎 ANALIZA POTENCJALNYCH PROBLEMÓW:')
    
    # Brakujące indeksy na często używanych kolumnach
    missing_indexes = []
    
    # Sprawdź czy są indeksy na kluczowych kolumnach
    important_columns = [
        ('zawodnicy', 'kategoria'),
        ('zawodnicy', 'plec'),
        ('zawodnicy', 'klub'),
        ('zawodnicy', 'qr_code'),
        ('zawodnicy', 'checked_in'),
        ('wyniki', 'status'),
        ('wyniki', 'czas_przejazdu_s'),
        ('checkpoints', 'checkpoint_name'),
        ('checkpoints', 'timestamp'),
        ('checkpoints', 'device_id'),
        ('checkpoints', 'nr_startowy')
    ]
    
    for table, column in important_columns:
        cur.execute('''
            SELECT COUNT(*) FROM pg_indexes 
            WHERE tablename = %s 
            AND indexdef LIKE %s
        ''', (table, f'%{column}%'))
        
        index_count = cur.fetchone()[0]
        if index_count == 0:
            missing_indexes.append(f'{table}.{column}')
    
    if missing_indexes:
        print('\n❌ BRAKUJĄCE INDEKSY:')
        for missing in missing_indexes:
            print(f'  - {missing}')
    else:
        print('\n✅ Wszystkie ważne kolumny mają indeksy')

    # Sprawdź duplikaty w checkpoints
    print('\n🔄 SPRAWDZANIE DUPLIKATÓW:')
    cur.execute('''
        SELECT nr_startowy, checkpoint_name, COUNT(*)
        FROM checkpoints
        GROUP BY nr_startowy, checkpoint_name
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        LIMIT 10
    ''')
    
    duplicates = cur.fetchall()
    if duplicates:
        print('  ❌ Znalezione duplikaty w checkpoints:')
        for nr, checkpoint, count in duplicates:
            print(f'    Nr {nr}, {checkpoint}: {count} razy')
    else:
        print('  ✅ Brak duplikatów w checkpoints')

    # Sprawdź wolne zapytania (symulacja)
    print('\n⏱️ POTENCJALNE PROBLEMY WYDAJNOŚCI:')
    
    # Sprawdź zapytania bez WHERE
    issues = []
    
    # Duże JOINy bez indeksów
    cur.execute('''
        SELECT COUNT(*)
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        LEFT JOIN checkpoints c ON z.nr_startowy = c.nr_startowy
    ''')
    
    total_joins = cur.fetchone()[0]
    if total_joins > 1000:
        issues.append(f'Duże JOIN operations ({total_joins:,} rekordów)')

    # Sprawdź fragmentację checkpoints
    cur.execute('SELECT COUNT(*) FROM checkpoints WHERE timestamp < NOW() - INTERVAL \'30 days\'')
    old_checkpoints = cur.fetchone()[0]
    if old_checkpoints > 1000:
        issues.append(f'Stare checkpoints do archiwizacji: {old_checkpoints:,}')

    if issues:
        for issue in issues:
            print(f'  ⚠️  {issue}')
    else:
        print('  ✅ Brak oczywistych problemów wydajności')

    cur.close()
    conn.close()

if __name__ == '__main__':
    analyze_database() 