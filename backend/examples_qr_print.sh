#!/bin/bash
# Przykłady użycia generatora PDF z kodami QR SKATECROSS

echo "🏆 PRZYKŁADY UŻYCIA - Generator PDF QR kodów"
echo "=" * 50

echo ""
echo "📋 1. NAKLEJKI dla wybranych zawodników:"
echo "python print_qr_codes.py --numbers 1 2 3 5 10 --layout stickers --output naklejki_wybrani.pdf"

echo ""
echo "📋 2. LISTA wszystkich z kategorii Junior A:"
echo "python print_qr_codes.py --category 'Junior A' --layout list --output lista_juniorA.pdf"

echo ""
echo "📋 3. DUŻE KODY dla konkretnego zawodnika:"
echo "python print_qr_codes.py --numbers 2 --layout large --output duzy_anna_nowak.pdf"

echo ""
echo "📋 4. NAKLEJKI dla wszystkich kobiet:"
echo "python print_qr_codes.py --gender K --layout stickers --output naklejki_kobiety.pdf"

echo ""
echo "📋 5. LISTA dla klubu (częściowe dopasowanie):"
echo "python print_qr_codes.py --club 'Kraków' --layout list --output lista_krakow.pdf"

echo ""
echo "📋 6. NAKLEJKI dla kombinacji kryteriów:"
echo "python print_qr_codes.py --category 'Senior' --gender M --layout stickers --output naklejki_senior_m.pdf"

echo ""
echo "📋 7. WSZYSTKICH zawodników (UWAGA: duży plik!):"
echo "python print_qr_codes.py --all --layout list --output wszystkich_lista.pdf"

echo ""
echo "🔧 DOSTĘPNE OPCJE:"
echo "  --numbers X Y Z     # Konkretne numery startowe"
echo "  --category 'NAZWA'  # Kategoria (Junior A, Junior B, Junior C, Junior D, Senior, Masters)"
echo "  --gender M/K        # Płeć"
echo "  --club 'NAZWA'      # Nazwa klubu (częściowe dopasowanie)"
echo "  --layout TYPE       # stickers (naklejki), list (lista), large (duże)"
echo "  --output PLIK.pdf   # Nazwa pliku wyjściowego"
echo "  --all              # Wszyscy zawodnicy"

echo ""
echo "📄 LAYOUT TYPES:"
echo "  stickers - Naklejki 3x8 na stronę A4 (24 naklejki)"
echo "  list     - Kompaktowa lista z małymi QR kodami"
echo "  large    - Duże QR kody, jeden na stronę"

echo ""
echo "💡 PRZYKŁAD PRAKTYCZNY:"
echo "# Drukowanie naklejek na numery startowe dla kategorii Junior A"
echo "python print_qr_codes.py --category 'Junior A' --layout stickers --output junior_A_naklejki.pdf"
echo ""
echo "# Lista weryfikacyjna dla sędziów z małymi kodami QR"
echo "python print_qr_codes.py --all --layout list --output lista_weryfikacyjna.pdf"
echo ""
echo "# Duże kody QR do testowania skanerów"
echo "python print_qr_codes.py --numbers 1 2 3 4 5 --layout large --output test_duze_kody.pdf" 