#!/bin/bash

# 🚀 SKATECROSS v37.0 - Bezpieczny Deploy na Produkcję
# Zapobiega problemom z desynchronizacją lokalnej/produkcyjnej wersji

set -e  # Exit on any error

echo "🚀 SKATECROSS Deploy Script v37.0"
echo "=================================="

# 1. SPRAWDZENIE CZY JESTEŚMY W REPO
if [ ! -d ".git" ]; then
    echo "❌ ERROR: Nie jesteś w głównym folderze repo!"
    exit 1
fi

# 2. SPRAWDZENIE CZYSTOŚCI REPO  
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  WARNING: Masz uncommitted changes!"
    git status --short
    read -p "Kontynuować? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 3. PULL NAJNOWSZYCH ZMIAN
echo "📥 Pulling najnowsze zmiany z master..."
git pull origin master

# 4. FRONTEND BUILD
echo "🏗️  Building frontend..."
cd frontend
npm run build
echo "✅ Frontend build complete"

# 5. DODANIE DIST DO GIT
cd ..
echo "📦 Dodaję nowy frontend dist do git..."
git add -f frontend/dist/
if [ -n "$(git diff --cached)" ]; then
    git commit -m "BUILD: Frontend dist update - $(date '+%Y-%m-%d %H:%M')"
    echo "✅ Frontend dist committed"
else
    echo "ℹ️  No frontend changes to commit"
fi

# 6. DEPLOY NA HEROKU
echo "🚀 Deploying to Heroku sk8lc..."
git push sk8lc master

# 7. WALIDACJA DEPLOY
echo "⏳ Czekam 10s na restart Heroku..."
sleep 10

echo "🔍 Sprawdzam czy deploy przeszedł..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://sk8lc-07194bee9be5.herokuapp.com/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Aplikacja odpowiada: $HTTP_CODE"
else
    echo "❌ ERROR: Aplikacja nie odpowiada: $HTTP_CODE"
    exit 1
fi

# 8. SPRAWDZENIE HASH ASSETU FRONTEND
echo "🔍 Sprawdzam hash frontend assetu..."
LOCAL_HASH=$(ls frontend/dist/assets/index-*.js | grep -o 'index-[^.]*\.js' | head -1)
PROD_HASH=$(curl -s https://sk8lc-07194bee9be5.herokuapp.com/ | grep -o "index-[^\.]*\.js" | head -1)

echo "📍 Local hash:  $LOCAL_HASH"
echo "🌐 Prod hash:   $PROD_HASH"

if [ "$LOCAL_HASH" = "$PROD_HASH" ]; then
    echo "✅ SUCCESS: Frontend synchronized!"
else
    echo "❌ ERROR: Frontend desynchronized!"
    echo "   Local:  $LOCAL_HASH"
    echo "   Prod:   $PROD_HASH"
    exit 1
fi

# 9. SPRAWDZENIE API
echo "🔍 Testing API endpoints..."
API_RESPONSE=$(curl -s https://sk8lc-07194bee9be5.herokuapp.com/api/version)
if [[ $API_RESPONSE == *"SKATECROSS"* ]]; then
    echo "✅ API working"
else
    echo "❌ ERROR: API not responding correctly"
    exit 1
fi

echo ""
echo "🎉 =================================="
echo "🎉 DEPLOY SUCCESS!"
echo "🎉 =================================="
echo "🌐 Produkcja: https://sk8lc-07194bee9be5.herokuapp.com/"
echo "📱 Frontend:  $PROD_HASH"
echo "⏰ Deploy:    $(date)"
echo ""
