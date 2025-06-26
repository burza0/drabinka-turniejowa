#!/bin/bash

# 🔍 SKATECROSS Quick Production Check
# Szybkie sprawdzenie czy produkcja ma najnowsze zmiany

echo "🔍 QUICK CHECK sk8lc Production"
echo "==============================="

echo "🌐 HTTP Status..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://sk8lc-07194bee9be5.herokuapp.com/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ OK: $HTTP_CODE"
else
    echo "❌ ERROR: $HTTP_CODE"
fi

echo ""
echo "📱 Frontend Version..."
if ls frontend/dist/assets/index-*.js >/dev/null 2>&1; then
    LOCAL_HASH=$(ls frontend/dist/assets/index-*.js | grep -o 'index-[^.]*\.js' | head -1)
    PROD_HASH=$(curl -s https://sk8lc-07194bee9be5.herokuapp.com/ | grep -o "index-[^\.]*\.js" | head -1)
    
    echo "Local:  $LOCAL_HASH"
    echo "Prod:   $PROD_HASH"
    
    if [ "$LOCAL_HASH" = "$PROD_HASH" ]; then
        echo "✅ Synchronized"
    else
        echo "❌ Desynchronized!"
    fi
else
    echo "⚠️ No local build found"
fi

echo ""
echo "🔧 API Version..."
API_RESPONSE=$(curl -s https://sk8lc-07194bee9be5.herokuapp.com/api/version 2>/dev/null)
if [[ $API_RESPONSE == *"SKATECROSS"* ]]; then
    VERSION=$(echo $API_RESPONSE | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
    ENV=$(echo $API_RESPONSE | grep -o '"environment":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Version: $VERSION ($ENV)"
else
    echo "❌ API not responding"
fi

echo ""
echo "📊 Last Deploy..."
LAST_COMMIT=$(git log -1 --pretty=format:"%h %s" 2>/dev/null || echo "Unknown")
echo "Last commit: $LAST_COMMIT"

echo ""
echo "💡 Usage:"
echo "  Deploy:     ./deploy-sk8lc.sh"
echo "  Check:      ./check-sk8lc.sh"
echo "  Production: https://sk8lc-07194bee9be5.herokuapp.com/"
