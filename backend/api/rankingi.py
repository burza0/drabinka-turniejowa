from flask import Blueprint, jsonify, request
from utils.database import get_all
from utils.api_response import APIResponse, handle_api_errors, validate_season, validate_pagination

rankingi_bp = Blueprint('rankingi', __name__)

# --- Funkcje rankingowe ---
def calculate_individual_ranking(season=None):
    query = f"""
        WITH wyniki_z_pozycjami AS (
            SELECT 
                w.nr_startowy,
                z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                ROW_NUMBER() OVER (
                    PARTITION BY z.kategoria, z.plec 
                    ORDER BY w.czas_przejazdu_s ASC
                ) as pozycja,
                w.czas_przejazdu_s
            FROM wyniki w
            JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
            WHERE w.status = 'FINISHED' 
                AND w.czas_przejazdu_s IS NOT NULL
        ),
        punkty_zawodnikow AS (
            SELECT 
                nr_startowy, imie, nazwisko, kategoria, plec, klub,
                pozycja,
                CASE 
                    WHEN pozycja <= 32 THEN 
                        CASE pozycja
                            WHEN 1 THEN 100 WHEN 2 THEN 80 WHEN 3 THEN 60 WHEN 4 THEN 50
                            WHEN 5 THEN 45 WHEN 6 THEN 40 WHEN 7 THEN 36 WHEN 8 THEN 32
                            WHEN 9 THEN 29 WHEN 10 THEN 26 WHEN 11 THEN 24 WHEN 12 THEN 22
                            WHEN 13 THEN 20 WHEN 14 THEN 18 WHEN 15 THEN 16 WHEN 16 THEN 15
                            WHEN 17 THEN 14 WHEN 18 THEN 13 WHEN 19 THEN 12 WHEN 20 THEN 11
                            WHEN 21 THEN 10 WHEN 22 THEN 9 WHEN 23 THEN 8 WHEN 24 THEN 7
                            WHEN 25 THEN 6 WHEN 26 THEN 5 WHEN 27 THEN 4 WHEN 28 THEN 3
                            WHEN 29 THEN 2 WHEN 30 THEN 1 WHEN 31 THEN 1 WHEN 32 THEN 1
                            ELSE 0
                        END
                    ELSE 0
                END as punkty,
                czas_przejazdu_s
            FROM wyniki_z_pozycjami
        )
        SELECT 
            nr_startowy, imie, nazwisko, kategoria, plec, klub,
            SUM(punkty) as punkty,
            COUNT(*) as liczba_zawodow,
            MIN(czas_przejazdu_s) as najlepszy_czas
        FROM punkty_zawodnikow
        GROUP BY nr_startowy, imie, nazwisko, kategoria, plec, klub
        ORDER BY punkty DESC, najlepszy_czas ASC
    """
    return get_all(query)

def calculate_general_ranking_n2(season=None):
    # Ranking generalny n-2: suma punktów z najlepszych startów, pomijając dwa najsłabsze (jeśli zawodnik ma >2 starty)
    query = f"""
        WITH wyniki_z_pozycjami AS (
            SELECT 
                w.nr_startowy,
                z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                ROW_NUMBER() OVER (
                    PARTITION BY z.kategoria, z.plec 
                    ORDER BY w.czas_przejazdu_s ASC
                ) as pozycja,
                w.czas_przejazdu_s
            FROM wyniki w
            JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
            WHERE w.status = 'FINISHED' 
                AND w.czas_przejazdu_s IS NOT NULL
        ),
        punkty_zawodnikow AS (
            SELECT 
                nr_startowy, imie, nazwisko, kategoria, plec, klub,
                pozycja,
                CASE 
                    WHEN pozycja <= 32 THEN 
                        CASE pozycja
                            WHEN 1 THEN 100 WHEN 2 THEN 80 WHEN 3 THEN 60 WHEN 4 THEN 50
                            WHEN 5 THEN 45 WHEN 6 THEN 40 WHEN 7 THEN 36 WHEN 8 THEN 32
                            WHEN 9 THEN 29 WHEN 10 THEN 26 WHEN 11 THEN 24 WHEN 12 THEN 22
                            WHEN 13 THEN 20 WHEN 14 THEN 18 WHEN 15 THEN 16 WHEN 16 THEN 15
                            WHEN 17 THEN 14 WHEN 18 THEN 13 WHEN 19 THEN 12 WHEN 20 THEN 11
                            WHEN 21 THEN 10 WHEN 22 THEN 9 WHEN 23 THEN 8 WHEN 24 THEN 7
                            WHEN 25 THEN 6 WHEN 26 THEN 5 WHEN 27 THEN 4 WHEN 28 THEN 3
                            WHEN 29 THEN 2 WHEN 30 THEN 1 WHEN 31 THEN 1 WHEN 32 THEN 1
                            ELSE 0
                        END
                    ELSE 0
                END as punkty,
                czas_przejazdu_s
            FROM wyniki_z_pozycjami
        ),
        ranked AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY nr_startowy ORDER BY punkty DESC) as rn,
                COUNT(*) OVER (PARTITION BY nr_startowy) as total
            FROM punkty_zawodnikow
        )
        SELECT 
            nr_startowy, imie, nazwisko, kategoria, plec, klub,
            SUM(punkty) as punkty,
            COUNT(*) as liczba_zawodow,
            MIN(czas_przejazdu_s) as najlepszy_czas
        FROM ranked
        WHERE (total <= 2 OR rn <= total - 2)
        GROUP BY nr_startowy, imie, nazwisko, kategoria, plec, klub
        ORDER BY punkty DESC, najlepszy_czas ASC
    """
    return get_all(query)

def calculate_club_ranking_total(season=None):
    query = f"""
        WITH wyniki_z_pozycjami AS (
            SELECT 
                w.nr_startowy,
                z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                ROW_NUMBER() OVER (
                    PARTITION BY z.kategoria, z.plec 
                    ORDER BY w.czas_przejazdu_s ASC
                ) as pozycja,
                w.czas_przejazdu_s
            FROM wyniki w
            JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
            WHERE w.status = 'FINISHED' 
                AND w.czas_przejazdu_s IS NOT NULL
                AND z.klub IS NOT NULL
        ),
        punkty_zawodnikow AS (
            SELECT 
                klub, kategoria, plec, nr_startowy,
                CASE 
                    WHEN pozycja <= 32 THEN 
                        CASE pozycja
                            WHEN 1 THEN 100 WHEN 2 THEN 80 WHEN 3 THEN 60 WHEN 4 THEN 50
                            WHEN 5 THEN 45 WHEN 6 THEN 40 WHEN 7 THEN 36 WHEN 8 THEN 32
                            WHEN 9 THEN 29 WHEN 10 THEN 26 WHEN 11 THEN 24 WHEN 12 THEN 22
                            WHEN 13 THEN 20 WHEN 14 THEN 18 WHEN 15 THEN 16 WHEN 16 THEN 15
                            WHEN 17 THEN 14 WHEN 18 THEN 13 WHEN 19 THEN 12 WHEN 20 THEN 11
                            WHEN 21 THEN 10 WHEN 22 THEN 9 WHEN 23 THEN 8 WHEN 24 THEN 7
                            WHEN 25 THEN 6 WHEN 26 THEN 5 WHEN 27 THEN 4 WHEN 28 THEN 3
                            WHEN 29 THEN 2 WHEN 30 THEN 1 WHEN 31 THEN 1 WHEN 32 THEN 1
                            ELSE 0
                        END
                    ELSE 0
                END as punkty,
                ROW_NUMBER() OVER (
                    PARTITION BY klub, kategoria, plec 
                    ORDER BY pozycja ASC
                ) as ranking_w_kategorii
            FROM wyniki_z_pozycjami
        )
        SELECT 
            klub,
            SUM(punkty) as punkty_total,
            COUNT(DISTINCT CONCAT(kategoria, '_', plec)) as aktywne_kategorie,
            ROUND(AVG(punkty), 1) as balance
        FROM punkty_zawodnikow
        GROUP BY klub
        ORDER BY punkty_total DESC, aktywne_kategorie DESC
    """
    return get_all(query)

def calculate_club_ranking_top3(season=None):
    query = f"""
        WITH wyniki_z_pozycjami AS (
            SELECT 
                w.nr_startowy,
                z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                ROW_NUMBER() OVER (
                    PARTITION BY z.kategoria, z.plec 
                    ORDER BY w.czas_przejazdu_s ASC
                ) as pozycja,
                w.czas_przejazdu_s
            FROM wyniki w
            JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
            WHERE w.status = 'FINISHED' 
                AND w.czas_przejazdu_s IS NOT NULL
                AND z.klub IS NOT NULL
        ),
        punkty_zawodnikow AS (
            SELECT 
                klub, kategoria, plec, nr_startowy,
                CASE 
                    WHEN pozycja <= 32 THEN 
                        CASE pozycja
                            WHEN 1 THEN 100 WHEN 2 THEN 80 WHEN 3 THEN 60 WHEN 4 THEN 50
                            WHEN 5 THEN 45 WHEN 6 THEN 40 WHEN 7 THEN 36 WHEN 8 THEN 32
                            WHEN 9 THEN 29 WHEN 10 THEN 26 WHEN 11 THEN 24 WHEN 12 THEN 22
                            WHEN 13 THEN 20 WHEN 14 THEN 18 WHEN 15 THEN 16 WHEN 16 THEN 15
                            WHEN 17 THEN 14 WHEN 18 THEN 13 WHEN 19 THEN 12 WHEN 20 THEN 11
                            WHEN 21 THEN 10 WHEN 22 THEN 9 WHEN 23 THEN 8 WHEN 24 THEN 7
                            WHEN 25 THEN 6 WHEN 26 THEN 5 WHEN 27 THEN 4 WHEN 28 THEN 3
                            WHEN 29 THEN 2 WHEN 30 THEN 1 WHEN 31 THEN 1 WHEN 32 THEN 1
                            ELSE 0
                        END
                    ELSE 0
                END as punkty,
                ROW_NUMBER() OVER (
                    PARTITION BY klub, kategoria, plec 
                    ORDER BY pozycja ASC
                ) as ranking_w_kategorii
            FROM wyniki_z_pozycjami
        ),
        top3_per_category AS (
            SELECT 
                klub, kategoria, plec, punkty
            FROM punkty_zawodnikow
            WHERE ranking_w_kategorii <= 3
        )
        SELECT 
            klub,
            SUM(punkty) as punkty_top3,
            COUNT(DISTINCT CONCAT(kategoria, '_', plec)) as aktywne_kategorie,
            ROUND(AVG(punkty), 1) as balance
        FROM top3_per_category
        GROUP BY klub
        ORDER BY punkty_top3 DESC, aktywne_kategorie DESC
    """
    return get_all(query)

def calculate_medal_ranking(season=None):
    query = f"""
        WITH wyniki_z_pozycjami AS (
            SELECT 
                w.nr_startowy,
                z.klub,
                ROW_NUMBER() OVER (
                    PARTITION BY z.kategoria, z.plec 
                    ORDER BY w.czas_przejazdu_s ASC
                ) as pozycja
            FROM wyniki w
            JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
            WHERE w.status = 'FINISHED' 
                AND w.czas_przejazdu_s IS NOT NULL
                AND z.klub IS NOT NULL
        ),
        medale AS (
            SELECT 
                klub,
                SUM(CASE WHEN pozycja = 1 THEN 1 ELSE 0 END) as zlote,
                SUM(CASE WHEN pozycja = 2 THEN 1 ELSE 0 END) as srebrne,
                SUM(CASE WHEN pozycja = 3 THEN 1 ELSE 0 END) as brazowe
            FROM wyniki_z_pozycjami
            WHERE pozycja <= 3
            GROUP BY klub
        )
        SELECT 
            klub,
            zlote,
            srebrne,
            brazowe,
            (zlote + srebrne + brazowe) as lacznie
        FROM medale
        ORDER BY zlote DESC, srebrne DESC, brazowe DESC
    """
    return get_all(query)

def calculate_time_ranking(kategoria=None, plec=None, klub=None, typ='best', season=None, status='completed', limit=100, page=1, search=None, sort='time_asc'):
    """
    Ranking czasowy - najlepsze/najnowsze/średnie czasy zawodników
    
    Args:
        kategoria: filtr kategorii (np. "Junior A") 
        plec: filtr płci ("M"/"K")
        klub: filtr klubu
        typ: typ rankingu ("best", "latest", "avg", "all")
        season: sezon (opcjonalne)
        status: status wyników ("completed", "all")
        limit: max liczba wyników na stronę
        page: numer strony (1-based)
        search: wyszukiwanie po imieniu/nazwisku
        sort: sortowanie time_asc/time_desc/name_asc/name_desc/kategoria_asc/klub_asc
    """
    
    # Base conditions
    conditions = []
    params = []
    
    # Basic filters
    conditions.append("r.total_time IS NOT NULL")
    conditions.append("r.total_time > 0")  # Exclude invalid times
    conditions.append("r.total_time < 600")  # Exclude times > 10min (likely errors)
    
    if kategoria:
        conditions.append("z.kategoria = %s")
        params.append(kategoria)
    
    if plec:
        conditions.append("z.plec = %s") 
        params.append(plec)
        
    if klub:
        conditions.append("z.klub = %s")
        params.append(klub)
        
    if status != 'all':
        conditions.append("r.status = %s")
        params.append(status)
    
    # Search by name
    if search:
        search_pattern = f"%{search.strip()}%"
        conditions.append("(LOWER(z.imie) LIKE LOWER(%s) OR LOWER(z.nazwisko) LIKE LOWER(%s) OR LOWER(CONCAT(z.imie, ' ', z.nazwisko)) LIKE LOWER(%s))")
        params.extend([search_pattern, search_pattern, search_pattern])
    
    where_clause = " AND ".join(conditions)
    
    # Calculate offset for pagination
    offset = (page - 1) * limit
    
    # Build sorting clause based on sort parameter
    sort_clauses = {
        'time_asc': 'total_time ASC',
        'time_desc': 'total_time DESC', 
        'name_asc': 'z.nazwisko ASC, z.imie ASC',
        'name_desc': 'z.nazwisko DESC, z.imie DESC',
        'kategoria_asc': 'z.kategoria ASC, total_time ASC',
        'klub_asc': 'z.klub ASC, total_time ASC'
    }
    
    order_by = sort_clauses.get(sort, 'total_time ASC')  # Default to time ascending
    
    if typ == 'best':
        # Count query for pagination
        count_query = f"""
            SELECT COUNT(DISTINCT r.nr_startowy)
            FROM sectro_results r
            JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
            JOIN sectro_sessions s ON r.session_id = s.id
            WHERE {where_clause}
        """
        
        # Main query with pagination and sorting
        query = f"""
            WITH best_times AS (
                SELECT 
                    r.nr_startowy,
                    z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                    MIN(r.total_time) as total_time,
                    MAX(r.status) as sectro_status,
                    MAX(s.created_at) as last_session_date,
                    COUNT(*) as liczba_startow
                FROM sectro_results r
                JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
                JOIN sectro_sessions s ON r.session_id = s.id
                WHERE {where_clause}
                GROUP BY r.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub
                ORDER BY {order_by}
                LIMIT %s OFFSET %s
            )
            SELECT 
                nr_startowy, imie, nazwisko, kategoria, plec, klub,
                total_time, sectro_status, liczba_startow,
                ROW_NUMBER() OVER (ORDER BY {order_by}) + %s as pozycja
            FROM best_times 
            ORDER BY {order_by}
        """
        params_main = params + [limit, offset, offset]
        
    elif typ == 'latest':
        # Count query for pagination
        count_query = f"""
            WITH ranked_times AS (
                SELECT DISTINCT r.nr_startowy
                FROM sectro_results r
                JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
                JOIN sectro_sessions s ON r.session_id = s.id
                WHERE {where_clause}
            )
            SELECT COUNT(*) FROM ranked_times
        """
        
        # Main query with pagination and sorting
        query = f"""
            WITH ranked_times AS (
                SELECT 
                    r.nr_startowy,
                    z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                    r.total_time, r.status as sectro_status,
                    s.created_at as session_date,
                    ROW_NUMBER() OVER (
                        PARTITION BY r.nr_startowy 
                        ORDER BY s.created_at DESC
                    ) as rn
                FROM sectro_results r
                JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
                JOIN sectro_sessions s ON r.session_id = s.id
                WHERE {where_clause}
            ),
            latest_times AS (
                SELECT 
                    nr_startowy, imie, nazwisko, kategoria, plec, klub,
                    total_time, sectro_status,
                    1 as liczba_startow
                FROM ranked_times 
                WHERE rn = 1
                ORDER BY {order_by}
                LIMIT %s OFFSET %s
            )
            SELECT 
                nr_startowy, imie, nazwisko, kategoria, plec, klub,
                total_time, sectro_status, liczba_startow,
                ROW_NUMBER() OVER (ORDER BY {order_by}) + %s as pozycja
            FROM latest_times
            ORDER BY {order_by}
        """
        params_main = params + [limit, offset, offset]
        
    elif typ == 'avg':
        # Count query for pagination
        count_query = f"""
            SELECT COUNT(DISTINCT r.nr_startowy)
            FROM sectro_results r
            JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
            JOIN sectro_sessions s ON r.session_id = s.id
            WHERE {where_clause}
            HAVING COUNT(*) >= 2
        """
        
        # Main query with pagination and sorting
        query = f"""
            WITH avg_times AS (
                SELECT 
                    r.nr_startowy,
                    z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                    AVG(r.total_time) as total_time,
                    'completed' as sectro_status,
                    COUNT(*) as liczba_startow
                FROM sectro_results r
                JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
                JOIN sectro_sessions s ON r.session_id = s.id
                WHERE {where_clause}
                GROUP BY r.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub
                HAVING COUNT(*) >= 2
                ORDER BY {order_by}
                LIMIT %s OFFSET %s
            )
            SELECT 
                nr_startowy, imie, nazwisko, kategoria, plec, klub,
                total_time, sectro_status, liczba_startow,
                ROW_NUMBER() OVER (ORDER BY {order_by}) + %s as pozycja
            FROM avg_times 
            ORDER BY {order_by}
        """
        params_main = params + [limit, offset, offset]
        
    else:  # typ == 'all'
        # Count query for pagination
        count_query = f"""
            SELECT COUNT(*)
            FROM sectro_results r
            JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
            JOIN sectro_sessions s ON r.session_id = s.id
            WHERE {where_clause}
        """
        
        # Main query with pagination and sorting
        query = f"""
            SELECT 
                r.nr_startowy,
                z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                r.total_time, 
                r.status as sectro_status,
                1 as liczba_startow,
                ROW_NUMBER() OVER (ORDER BY {order_by}) + %s as pozycja
            FROM sectro_results r
            JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
            JOIN sectro_sessions s ON r.session_id = s.id
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
        """
        params_main = params + [offset, limit, offset]
    
    # Get total count for pagination metadata
    total_count_result = get_all(count_query, params)
    total_count = total_count_result[0]['count'] if total_count_result else 0
    
    # Get paginated results
    results = get_all(query, params_main)
    
    # Calculate pagination metadata
    total_pages = max(1, (total_count + limit - 1) // limit)  # Ceiling division
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        'ranking': results,
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'total_results': total_count,
            'per_page': limit,
            'has_next': has_next,
            'has_prev': has_prev,
            'start_index': offset + 1,
            'end_index': min(offset + limit, total_count)
        }
    }

# --- Endpointy rankingowe ---
@rankingi_bp.route("/api/rankings/individual")
@handle_api_errors
def get_individual_ranking():
    """
    Endpoint zwracający ranking indywidualny zawodników
    GET /api/rankings/individual?season=2025&page=1&limit=50
    """
    season = validate_season(request.args.get('season'))
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    ranking = calculate_individual_ranking(season)
    
    # Paginacja
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = ranking[start_idx:end_idx]
    
    return APIResponse.paginated(
        data=paginated_data,
        page=page,
        limit=limit,
        total=len(ranking),
        message=f"Ranking indywidualny pobrany pomyślnie"
    )

@rankingi_bp.route("/api/rankings/general")
@handle_api_errors
def get_general_ranking():
    """
    Endpoint zwracający ranking generalny zawodników (n-2)
    GET /api/rankings/general?season=2025&page=1&limit=50
    """
    season = validate_season(request.args.get('season'))
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    ranking = calculate_general_ranking_n2(season)
    
    # Paginacja
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = ranking[start_idx:end_idx]
    
    return APIResponse.paginated(
        data=paginated_data,
        page=page,
        limit=limit,
        total=len(ranking),
        message=f"Ranking generalny pobrany pomyślnie"
    )

@rankingi_bp.route("/api/rankings/clubs/total")
@handle_api_errors
def get_club_ranking_total():
    """
    Endpoint zwracający ranking klubów (wszyscy zawodnicy)
    GET /api/rankings/clubs/total?season=2025&page=1&limit=50
    """
    season = validate_season(request.args.get('season'))
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    ranking = calculate_club_ranking_total(season)
    
    # Paginacja
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = ranking[start_idx:end_idx]
    
    return APIResponse.paginated(
        data=paginated_data,
        page=page,
        limit=limit,
        total=len(ranking),
        message=f"Ranking klubów (total) pobrany pomyślnie"
    )

@rankingi_bp.route("/api/rankings/clubs/top3")
@handle_api_errors
def get_club_ranking_top3():
    """
    Endpoint zwracający ranking klubów (top 3 z każdej kategorii)
    GET /api/rankings/clubs/top3?season=2025&page=1&limit=50
    """
    season = validate_season(request.args.get('season'))
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    ranking = calculate_club_ranking_top3(season)
    
    # Paginacja
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = ranking[start_idx:end_idx]
    
    return APIResponse.paginated(
        data=paginated_data,
        page=page,
        limit=limit,
        total=len(ranking),
        message=f"Ranking klubów (top3) pobrany pomyślnie"
    )

@rankingi_bp.route("/api/rankings/medals")
@handle_api_errors
def get_medal_ranking():
    """
    Endpoint zwracający ranking medalowy klubów
    GET /api/rankings/medals?season=2025&page=1&limit=50
    """
    season = validate_season(request.args.get('season'))
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    ranking = calculate_medal_ranking(season)
    
    # Paginacja
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_data = ranking[start_idx:end_idx]
    
    return APIResponse.paginated(
        data=paginated_data,
        page=page,
        limit=limit,
        total=len(ranking),
        message=f"Ranking medalowy pobrany pomyślnie"
    )

@rankingi_bp.route("/api/rankings/summary")
@handle_api_errors
def get_rankings_summary():
    """
    Endpoint zwracający podsumowanie wszystkich rankingów
    GET /api/rankings/summary?season=2025
    """
    season = validate_season(request.args.get('season'))
    
    individual = calculate_individual_ranking(season)
    general = calculate_general_ranking_n2(season)
    clubs_total = calculate_club_ranking_total(season)
    clubs_top3 = calculate_club_ranking_top3(season)
    medals = calculate_medal_ranking(season)
    
    summary = {
        "season": season or "wszystkie",
        "stats": {
            "zawodnicy_total": len(individual),
            "zawodnicy_general": len(general),
            "kluby_total": len(clubs_total),
            "kluby_top3": len(clubs_top3),
            "kluby_z_medalami": len(medals)
        },
        "top_zawodnik": individual[0] if individual else None,
        "top_general": general[0] if general else None,
        "top_klub_total": clubs_total[0] if clubs_total else None,
        "top_klub_top3": clubs_top3[0] if clubs_top3 else None,
        "top_medals": medals[0] if medals else None
    }
    
    return APIResponse.success(
        data=summary,
        message="Podsumowanie rankingów pobrane pomyślnie"
    )

@rankingi_bp.route("/api/rankings/times")
@handle_api_errors
def get_time_ranking():
    """
    Endpoint rankingu czasowego
    GET /api/rankings/times?kategoria=Junior A&plec=M&typ=best&limit=25&page=1&search=Anna&sort=time_asc
    
    Parameters:
        kategoria: kategoria zawodników (opcjonalne)
        plec: płeć M/K (opcjonalne)  
        klub: nazwa klubu (opcjonalne)
        typ: best/latest/avg/all (default: best)
        status: completed/all (default: completed)
        season: sezon (opcjonalne, obecnie nie używane)
        limit: wyników na stronę (default: 25, max: 100)
        page: numer strony (default: 1)
        search: wyszukiwanie po imieniu/nazwisku (opcjonalne)
        sort: sortowanie time_asc/time_desc/name_asc/name_desc/kategoria_asc/klub_asc (default: time_asc)
    """
    
    # Parse parameters
    kategoria = request.args.get('kategoria')
    plec = request.args.get('plec')
    klub = request.args.get('klub')
    typ = request.args.get('typ', 'best')
    status = request.args.get('status', 'completed')
    season = request.args.get('season')  # Currently not used, ready for future
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'time_asc')  # NEW: sorting parameter
    
    # Validate and parse pagination parameters
    try:
        limit = min(int(request.args.get('limit', 25)), 100)  # Default 25, max 100
    except (ValueError, TypeError):
        limit = 25
    
    try:
        page = max(1, int(request.args.get('page', 1)))  # Minimum page 1
    except (ValueError, TypeError):
        page = 1
    
    # Validate typ parameter
    if typ not in ['best', 'latest', 'avg', 'all']:
        return APIResponse.error(
            message="Nieprawidłowy typ rankingu. Dozwolone: best, latest, avg, all",
            code=400
        )
    
    # Validate sort parameter
    valid_sorts = ['time_asc', 'time_desc', 'name_asc', 'name_desc', 'kategoria_asc', 'klub_asc']
    if sort not in valid_sorts:
        return APIResponse.error(
            message=f"Nieprawidłowe sortowanie. Dozwolone: {', '.join(valid_sorts)}",
            code=400
        )
    
    # Clean search parameter
    search_query = search if search else None
    
    # Get ranking data with pagination and sorting
    result = calculate_time_ranking(
        kategoria=kategoria,
        plec=plec, 
        klub=klub,
        typ=typ,
        season=season,
        status=status,
        limit=limit,
        page=page,
        search=search_query,
        sort=sort  # NEW: pass sort parameter
    )
    
    # Enhanced response with metadata
    response_data = {
        "ranking": result['ranking'],
        "pagination": result['pagination'],
        "filters": {
            "kategoria": kategoria,
            "plec": plec,
            "klub": klub, 
            "typ": typ,
            "status": status,
            "search": search_query,
            "sort": sort,  # NEW: include sort in response
            "limit": limit,
            "page": page
        },
        "meta": {
            "count": len(result['ranking']),
            "typ_description": {
                "best": "Najlepszy czas każdego zawodnika",
                "latest": "Ostatni czas każdego zawodnika", 
                "avg": "Średni czas każdego zawodnika (min. 2 starty)",
                "all": "Wszystkie czasy (bez grupowania)"
            }.get(typ, "")
        }
    }
    
    return APIResponse.success(
        data=response_data,
        message=f"Ranking czasowy ({typ}) - strona {page}/{result['pagination']['total_pages']} ({result['pagination']['total_results']} wyników)"
    )

@rankingi_bp.route("/api/rankings/times/stats")  
@handle_api_errors
def get_time_ranking_stats():
    """
    Statystyki rankingu czasowego
    GET /api/rankings/times/stats
    """
    
    stats_query = """
        SELECT 
            COUNT(DISTINCT r.nr_startowy) as total_athletes,
            COUNT(*) as total_results,
            MIN(r.total_time) as fastest_time,
            MAX(r.total_time) as slowest_time,
            AVG(r.total_time) as average_time,
            COUNT(DISTINCT z.kategoria) as total_categories,
            COUNT(DISTINCT z.klub) as total_clubs
        FROM sectro_results r
        JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy  
        WHERE r.total_time IS NOT NULL 
        AND r.total_time > 0 
        AND r.total_time < 600
        AND r.status = 'completed'
    """
    
    stats = get_all(stats_query)
    
    return APIResponse.success(
        data=stats[0] if stats else {},
        message="Statystyki rankingu czasowego pobrane pomyślnie"
    ) 