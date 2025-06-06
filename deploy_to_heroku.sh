#!/bin/bash

# Skrypt do automatycznego deployu lokalnego kodu na Heroku
# Użycie: ./deploy_to_heroku.sh NAZWA_APLIKACJI_HEROKU

set -e

if [ -z "$1" ]; then
  echo "Podaj nazwę aplikacji Heroku jako pierwszy argument!"
  exit 1
fi

HEROKU_APP_NAME="$1"

# 1. Logowanie do Heroku
heroku login

# 2. Dodanie remote jeśli nie istnieje
heroku git:remote -a "$HEROKU_APP_NAME"

# 3. Wypchnięcie lokalnego kodu na Heroku (wymuszenie nadpisania)
git push heroku HEAD:main --force

# 4. (Opcjonalnie) migracje lub inne zadania po stronie Heroku
# Przykład: heroku run python backend/api_server.py -a "$HEROKU_APP_NAME"

# 5. Wyświetlenie logów
heroku logs --tail -a "$HEROKU_APP_NAME"

echo "\n✅ Deploy zakończony! Sprawdź aplikację na https://$HEROKU_APP_NAME.herokuapp.com/" 