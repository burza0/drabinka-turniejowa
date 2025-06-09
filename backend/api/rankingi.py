from flask import Blueprint, jsonify, request
from utils.database import get_all

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

# --- Endpointy rankingowe ---
@rankingi_bp.route("/api/rankings/individual")
def get_individual_ranking():
    try:
        season = request.args.get('season')
        if season:
            try:
                season = int(season)
            except ValueError:
                return jsonify({"error": "Nieprawidłowy format sezonu"}), 400
        ranking = calculate_individual_ranking(season)
        return jsonify(ranking), 200
    except Exception as e:
        print(f"Błąd w individual ranking: {e}")
        return jsonify({"error": str(e)}), 500

@rankingi_bp.route("/api/rankings/general")
def get_general_ranking():
    try:
        season = request.args.get('season')
        if season:
            try:
                season = int(season)
            except ValueError:
                return jsonify({"error": "Nieprawidłowy format sezonu"}), 400
        ranking = calculate_general_ranking_n2(season)
        return jsonify(ranking), 200
    except Exception as e:
        print(f"Błąd w general ranking: {e}")
        return jsonify({"error": str(e)}), 500

@rankingi_bp.route("/api/rankings/clubs/total")
def get_club_ranking_total():
    try:
        season = request.args.get('season')
        if season:
            try:
                season = int(season)
            except ValueError:
                return jsonify({"error": "Nieprawidłowy format sezonu"}), 400
        ranking = calculate_club_ranking_total(season)
        return jsonify(ranking), 200
    except Exception as e:
        print(f"Błąd w club ranking total: {e}")
        return jsonify({"error": str(e)}), 500

@rankingi_bp.route("/api/rankings/clubs/top3")
def get_club_ranking_top3():
    try:
        season = request.args.get('season')
        if season:
            try:
                season = int(season)
            except ValueError:
                return jsonify({"error": "Nieprawidłowy format sezonu"}), 400
        ranking = calculate_club_ranking_top3(season)
        return jsonify(ranking), 200
    except Exception as e:
        print(f"Błąd w club ranking top3: {e}")
        return jsonify({"error": str(e)}), 500

@rankingi_bp.route("/api/rankings/medals")
def get_medal_ranking():
    try:
        season = request.args.get('season')
        if season:
            try:
                season = int(season)
            except ValueError:
                return jsonify({"error": "Nieprawidłowy format sezonu"}), 400
        ranking = calculate_medal_ranking(season)
        return jsonify(ranking), 200
    except Exception as e:
        print(f"Błąd w medal ranking: {e}")
        return jsonify({"error": str(e)}), 500

@rankingi_bp.route("/api/rankings/summary")
def get_rankings_summary():
    try:
        season = request.args.get('season')
        if season:
            try:
                season = int(season)
            except ValueError:
                return jsonify({"error": "Nieprawidłowy format sezonu"}), 400
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
        return jsonify(summary), 200
    except Exception as e:
        print(f"Błąd w rankings summary: {e}")
        return jsonify({"error": str(e)}), 500 