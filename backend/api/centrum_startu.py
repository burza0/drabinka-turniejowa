from flask import Blueprint, jsonify, request
from utils.database import get_all, get_one, execute_query

centrum_startu_bp = Blueprint('centrum_startu', __name__)

@centrum_startu_bp.route("/api/grupy-startowe")
def grupy_startowe():
    try:
        grupy_data = get_all("""
            SELECT 
                kategoria,
                plec,
                COUNT(*) as liczba_zameldowanych,
                STRING_AGG(
                    CONCAT(nr_startowy, ': ', imie, ' ', nazwisko, ' (', klub, ')'), 
                    E'\n' ORDER BY nr_startowy
                ) as lista_zawodnikow,
                STRING_AGG(nr_startowy::text, ',' ORDER BY nr_startowy) as numery_startowe
            FROM zawodnicy 
            WHERE checked_in = TRUE AND kategoria IS NOT NULL
            GROUP BY kategoria, plec 
            ORDER BY kategoria, plec
        """)
        grupy_startowe = []
        numer_grupy = 1
        for grupa in grupy_data:
            nazwa_grupy = f"Grupa {numer_grupy}: {grupa['kategoria']} {'Mężczyźni' if grupa['plec'] == 'M' else 'Kobiety'}"
            grupy_startowe.append({
                "numer_grupy": numer_grupy,
                "nazwa": nazwa_grupy,
                "kategoria": grupa['kategoria'],
                "plec": grupa['plec'],
                "liczba_zawodnikow": grupa['liczba_zameldowanych'],
                "lista_zawodnikow": grupa['lista_zawodnikow'],
                "numery_startowe": grupa['numery_startowe'],
                "estimated_time": grupa['liczba_zameldowanych'] * 20,
                "status": "OCZEKUJE"
            })
            numer_grupy += 1
        return jsonify({
            "success": True,
            "total_grup": len(grupy_startowe),
            "total_zawodnikow": sum(g['liczba_zawodnikow'] for g in grupy_startowe),
            "grupy": grupy_startowe,
            "estimated_total_time_min": sum(g['estimated_time'] for g in grupy_startowe) / 60
        }), 200
    except Exception as e:
        print(f"Błąd w grupy-startowe: {e}")
        return jsonify({"error": str(e)}), 500

@centrum_startu_bp.route("/api/grupa-aktywna", methods=['GET'])
def get_grupa_aktywna():
    try:
        global aktywna_grupa_cache
        return jsonify({
            "success": True, 
            "aktywna_grupa": aktywna_grupa_cache if aktywna_grupa_cache["numer_grupy"] is not None else None,
            "kategoria": aktywna_grupa_cache.get("kategoria"),
            "plec": aktywna_grupa_cache.get("plec")
        }), 200
    except Exception as e:
        print(f"Błąd w get-grupa-aktywna: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# Globalna zmienna dla aktywnej grupy (jak w oryginalnym systemie)
aktywna_grupa_cache = {
    "numer_grupy": None,
    "kategoria": None,
    "plec": None,
    "nazwa": None
}

@centrum_startu_bp.route("/api/grupa-aktywna", methods=['POST'])
def set_grupa_aktywna():
    try:
        data = request.json
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        nazwa = data.get('nazwa', f"{kategoria} {'Mężczyźni' if plec == 'M' else 'Kobiety'}")
        numer_grupy = data.get('numer_grupy', 1)
        
        if not kategoria or not plec:
            return jsonify({"success": False, "message": "Brak kategorii lub płci"}), 400

        # Sprawdź czy są zawodnicy w tej grupie z checked_in = TRUE
        zawodnicy = get_all("""
            SELECT nr_startowy FROM zawodnicy 
            WHERE kategoria = %s AND plec = %s AND checked_in = TRUE
        """, (kategoria, plec))
        
        if not zawodnicy:
            return jsonify({
                "success": False, 
                "message": f"Brak zameldowanych zawodników w grupie {kategoria} {plec}"
            }), 400

        # Sprawdź czy grupa już jest w kolejce (TOGGLE LOGIC)
        istniejacy_checkpoint = get_one("""
            SELECT COUNT(*) as count FROM checkpoints 
            WHERE checkpoint_name = 'active-group-queue' 
            AND nr_startowy IN (
                SELECT nr_startowy FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND checked_in = TRUE
            )
        """, (kategoria, plec))
        
        if istniejacy_checkpoint['count'] > 0:
            # Grupa jest już w kolejce - USUŃ JĄ (toggle off)
            for zawodnik in zawodnicy:
                nr_startowy = zawodnik['nr_startowy']
                execute_query("""
                    DELETE FROM checkpoints 
                    WHERE checkpoint_name = 'active-group-queue' AND nr_startowy = %s
                """, (nr_startowy,))
            
            return jsonify({
                "success": True, 
                "message": f"Usunięto grupę {nazwa} z kolejki ({len(zawodnicy)} zawodników)",
                "action": "removed"
            }), 200
        else:
            # Grupa nie jest w kolejce - DODAJ JĄ (toggle on)
            dodanych = 0
            for zawodnik in zawodnicy:
                nr_startowy = zawodnik['nr_startowy']
                
                # Sprawdź czy zawodnik już nie jest w kolejce (ani skanowany, ani z grupy)
                existing = get_one("""
                    SELECT COUNT(*) as count FROM checkpoints 
                    WHERE nr_startowy = %s AND checkpoint_name IN ('start-line-verify', 'active-group-queue')
                """, (nr_startowy,))
                
                if existing['count'] == 0:
                    # Dodaj checkpoint active-group-queue
                    execute_query("""
                        INSERT INTO checkpoints (nr_startowy, checkpoint_name, qr_code, device_id)
                        VALUES (%s, %s, %s, %s)
                    """, (nr_startowy, 'active-group-queue', f'GROUP_{kategoria}_{plec}_{nr_startowy}', 'centrum-startu'))
                    dodanych += 1

            # Ustaw aktywną grupę w cache dla kompatybilności
            global aktywna_grupa_cache
            aktywna_grupa_cache = {
                "numer_grupy": numer_grupy,
                "kategoria": kategoria,
                "plec": plec,
                "nazwa": nazwa
            }

            return jsonify({
                "success": True, 
                "message": f"Dodano grupę {nazwa} do kolejki ({dodanych} zawodników)",
                "action": "added"
            }), 200
    except Exception as e:
        print(f"Błąd w set-grupa-aktywna: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue", methods=['GET'])
def get_start_queue():
    """Pobierz kolejkę zawodników oczekujących na starcie"""
    try:
        queue_data = []
        
        # Pobierz zawodników skanowanych (start-line-verify) 
        skanowani_zawodnicy = get_all("""
            SELECT DISTINCT
                z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
                c.timestamp as ostatni_skan,
                'SKANOWANY' as source_type
            FROM zawodnicy z
            JOIN checkpoints c ON z.nr_startowy = c.nr_startowy 
                AND c.checkpoint_name = 'start-line-verify'
            ORDER BY c.timestamp ASC
        """)
        
        queue_data.extend(skanowani_zawodnicy)
        
        # Pobierz zawodników dodanych z grup (active-group-queue)
        grupa_zawodnicy = get_all("""
            SELECT DISTINCT
                z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
                c.timestamp as czas_dodania,
                'AKTYWNA_GRUPA' as source_type
            FROM zawodnicy z
            JOIN checkpoints c ON z.nr_startowy = c.nr_startowy 
                AND c.checkpoint_name = 'active-group-queue'
            WHERE z.nr_startowy NOT IN (
                SELECT nr_startowy FROM checkpoints 
                WHERE checkpoint_name = 'start-line-verify'
            )
            AND z.nr_startowy NOT IN (
                SELECT nr_startowy FROM checkpoints 
                WHERE checkpoint_name = 'hidden-from-queue'
            )
            ORDER BY c.timestamp ASC
        """)
        
        # Dodaj oznaczenie dla zawodników którzy są zarówno skanowani jak i z grup
        for skanowany in skanowani_zawodnicy:
            # Sprawdź czy zawodnik jest też w active-group-queue
            w_grupie = get_one("""
                SELECT COUNT(*) as count FROM checkpoints 
                WHERE nr_startowy = %s AND checkpoint_name = 'active-group-queue'
            """, (skanowany['nr_startowy'],))
            
            if w_grupie['count'] > 0:
                skanowany['source_type'] = 'AKTYWNA_GRUPA_I_SKANOWANY'
        
        queue_data.extend(grupa_zawodnicy)
        
        return jsonify({"success": True, "queue": queue_data, "count": len(queue_data)}), 200
    except Exception as e:
        print(f"Błąd w get-start-queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue/remove/<int:nr_startowy>", methods=['DELETE'])
def remove_from_start_queue(nr_startowy):
    try:
        removed_types = []
        
        # Sprawdź czy zawodnik jest skanowany (start-line-verify)
        skanowany_checkpoint = get_one("""
            SELECT id FROM checkpoints 
            WHERE checkpoint_name = 'start-line-verify' AND nr_startowy = %s
        """, (nr_startowy,))
        
        if skanowany_checkpoint:
            # Usuń checkpoint skanowania
            execute_query("""
                DELETE FROM checkpoints 
                WHERE checkpoint_name = 'start-line-verify' AND nr_startowy = %s
            """, (nr_startowy,))
            removed_types.append("skanowany")
        
        # Sprawdź czy zawodnik jest z aktywnej grupy (active-group-queue)
        grupa_checkpoint = get_one("""
            SELECT id FROM checkpoints 
            WHERE checkpoint_name = 'active-group-queue' AND nr_startowy = %s
        """, (nr_startowy,))
        
        if grupa_checkpoint:
            # Usuń checkpoint grupy
            execute_query("""
                DELETE FROM checkpoints 
                WHERE checkpoint_name = 'active-group-queue' AND nr_startowy = %s
            """, (nr_startowy,))
            removed_types.append("z grupy")
        
        if removed_types:
            types_str = " i ".join(removed_types)
            return jsonify({"success": True, "message": f"Usunięto zawodnika {nr_startowy} z kolejki ({types_str})"}), 200
        else:
            return jsonify({"success": False, "message": f"Zawodnik {nr_startowy} nie znajduje się w kolejce"}), 404

    except Exception as e:
        print(f"Błąd w remove-from-start-queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue/remove-group", methods=['DELETE'])
def remove_group_from_start_queue():
    try:
        data = request.json
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        
        if not kategoria or not plec:
            return jsonify({"success": False, "message": "Brak kategorii lub płci"}), 400

        # Sprawdź ile zawodników z tej grupy jest w kolejce
        zawodnicy_w_kolejce = get_all("""
            SELECT c.nr_startowy FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            WHERE c.checkpoint_name = 'active-group-queue' 
            AND z.kategoria = %s AND z.plec = %s
        """, (kategoria, plec))
        
        if not zawodnicy_w_kolejce:
            return jsonify({"success": False, "message": f"Grupa {kategoria} {plec} nie znajduje się w kolejce"}), 404

        # Usuń wszystkich zawodników tej grupy z kolejki
        for zawodnik in zawodnicy_w_kolejce:
            execute_query("""
                DELETE FROM checkpoints 
                WHERE checkpoint_name = 'active-group-queue' AND nr_startowy = %s
            """, (zawodnik['nr_startowy'],))

        return jsonify({
            "success": True, 
            "message": f"Usunięto grupę {kategoria} {plec} z kolejki ({len(zawodnicy_w_kolejce)} zawodników)"
        }), 200
    except Exception as e:
        print(f"Błąd w remove-group-from-start-queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue/groups", methods=['GET'])
def get_groups_in_queue():
    try:
        # Pobierz listę grup aktualnie w kolejce z liczbą zawodników
        grupy_w_kolejce = get_all("""
            SELECT 
                z.kategoria,
                z.plec,
                COUNT(*) as liczba_zawodnikow,
                MIN(c.timestamp) as czas_dodania,
                STRING_AGG(z.nr_startowy::text, ',' ORDER BY z.nr_startowy) as numery_startowe
            FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            WHERE c.checkpoint_name = 'active-group-queue'
            GROUP BY z.kategoria, z.plec
            ORDER BY MIN(c.timestamp) ASC
        """)

        # Dodaj nazwę grupy dla każdej grupy
        for grupa in grupy_w_kolejce:
            grupa['nazwa'] = f"{grupa['kategoria']} {'Mężczyźni' if grupa['plec'] == 'M' else 'Kobiety'}"

        return jsonify({
            "success": True, 
            "groups": grupy_w_kolejce, 
            "total_groups": len(grupy_w_kolejce),
            "total_athletes": sum(g['liczba_zawodnikow'] for g in grupy_w_kolejce)
        }), 200
    except Exception as e:
        print(f"Błąd w get-groups-in-queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue/group-status", methods=['GET'])
def get_group_status():
    try:
        kategoria = request.args.get('kategoria')
        plec = request.args.get('plec')
        
        if not kategoria or not plec:
            return jsonify({"success": False, "message": "Brak kategorii lub płci"}), 400

        # Sprawdź czy grupa jest w kolejce
        zawodnicy_w_kolejce = get_one("""
            SELECT COUNT(*) as count FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            WHERE c.checkpoint_name = 'active-group-queue' 
            AND z.kategoria = %s AND z.plec = %s
        """, (kategoria, plec))
        
        is_active = zawodnicy_w_kolejce['count'] > 0 if zawodnicy_w_kolejce else False
        
        return jsonify({
            "success": True, 
            "is_active": is_active,
            "count": zawodnicy_w_kolejce['count'] if zawodnicy_w_kolejce else 0
        }), 200
    except Exception as e:
        print(f"Błąd w get-group-status: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue/all-group-statuses", methods=['GET'])
def get_all_group_statuses():
    try:
        # Pobierz wszystkie grupy zameldowane
        wszystkie_grupy = get_all("""
            SELECT DISTINCT kategoria, plec
            FROM zawodnicy 
            WHERE checked_in = TRUE AND kategoria IS NOT NULL
            ORDER BY kategoria, plec
        """)
        
        # Sprawdź status każdej grupy
        statuses = {}
        for grupa in wszystkie_grupy:
            key = f"{grupa['kategoria']}_{grupa['plec']}"
            
            zawodnicy_w_kolejce = get_one("""
                SELECT COUNT(*) as count FROM checkpoints c
                JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
                WHERE c.checkpoint_name = 'active-group-queue' 
                AND z.kategoria = %s AND z.plec = %s
            """, (grupa['kategoria'], grupa['plec']))
            
            statuses[key] = {
                "is_active": zawodnicy_w_kolejce['count'] > 0 if zawodnicy_w_kolejce else False,
                "count": zawodnicy_w_kolejce['count'] if zawodnicy_w_kolejce else 0
            }
        
        return jsonify({"success": True, "statuses": statuses}), 200
    except Exception as e:
        print(f"Błąd w get-all-group-statuses: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@centrum_startu_bp.route("/api/start-queue/clear", methods=['POST'])
def clear_start_queue():
    """Wyczyść kolejkę startową - usuń wszystkie grupy i skanowanych zawodników"""
    try:
        data = request.json or {}
        clear_type = data.get('type', 'all')  # 'all', 'scanned', 'groups'
        
        removed_counts = {'groups': 0, 'scanned': 0}
        
        if clear_type in ['all', 'scanned']:
            # Usuń wszystkich skanowanych zawodników (start-line-verify)
            scanned_result = execute_query("""
                DELETE FROM checkpoints 
                WHERE checkpoint_name = 'start-line-verify'
            """)
            removed_counts['scanned'] = scanned_result
        
        if clear_type in ['all', 'groups']:
            # Usuń wszystkie grupy z kolejki (active-group-queue)
            groups_result = execute_query("""
                DELETE FROM checkpoints 
                WHERE checkpoint_name = 'active-group-queue'
            """)
            removed_counts['groups'] = groups_result
            
            # Wyczyść cache aktywnej grupy
            global aktywna_grupa_cache
            aktywna_grupa_cache = {
                "numer_grupy": None,
                "kategoria": None,
                "plec": None,
                "nazwa": None
            }
        
        total_removed = removed_counts['groups'] + removed_counts['scanned']
        
        if clear_type == 'all':
            message = f"Wyczyszczono całą kolejkę startową ({total_removed} zawodników)"
        elif clear_type == 'scanned':
            message = f"Usunięto skanowanych zawodników z kolejki ({removed_counts['scanned']} zawodników)"
        elif clear_type == 'groups':
            message = f"Usunięto wszystkie grupy z kolejki ({removed_counts['groups']} zawodników)"
        else:
            message = f"Wyczyszczono kolejkę ({total_removed} zawodników)"
        
        return jsonify({
            "success": True, 
            "message": message,
            "removed": removed_counts,
            "total_removed": total_removed
        }), 200
    except Exception as e:
        print(f"Błąd w clear-start-queue: {e}")
        return jsonify({"success": False, "message": str(e)}), 500