#!/bin/bash

# Azure Deployment Verification Script
# Run this after completing the Azure deployment steps

API_URL="https://snr-news-api.azurewebsites.net"
FRONTEND_URL="https://snr-web.azurestaticapps.net"

echo "🚀 Testing Smart News Recommendation System Deployment"
echo "=================================================="
echo

echo "📡 Testing Backend API..."
echo "Health Check:"
HEALTH=$(curl -s "$API_URL/health" | jq -r '.status' 2>/dev/null)
if [ "$HEALTH" = "ok" ]; then
    echo "✅ API Health: OK"
else
    echo "❌ API Health: FAILED"
    echo "Response: $(curl -s "$API_URL/health")"
fi

echo
echo "Trending Articles:"
TRENDING=$(curl -s "$API_URL/trending?k=3" | jq '.items | length' 2>/dev/null)
if [ "$TRENDING" -gt 0 ] 2>/dev/null; then
    echo "✅ Trending: $TRENDING articles returned"
else
    echo "❌ Trending: FAILED"
    echo "Response: $(curl -s "$API_URL/trending?k=3")"
fi

echo
echo "Search Functionality:"
SEARCH_RESULT=$(curl -s -X POST "$API_URL/search" \
    -H "content-type: application/json" \
    -d '{"q":"economy","k":5}' | jq '.items | length' 2>/dev/null)
if [ "$SEARCH_RESULT" -gt 0 ] 2>/dev/null; then
    echo "✅ Search: $SEARCH_RESULT results returned"
else
    echo "❌ Search: FAILED"
    echo "Response: $(curl -s -X POST "$API_URL/search" -H "content-type: application/json" -d '{"q":"economy","k":5}')"
fi

echo
echo "Recommendations:"
REC_RESULT=$(curl -s -X POST "$API_URL/recommend" \
    -H "content-type: application/json" \
    -d '{"user_id":"u123","k":5,"recent_clicks":["n101","n205"]}' | jq '.items | length' 2>/dev/null)
if [ "$REC_RESULT" -gt 0 ] 2>/dev/null; then
    echo "✅ Recommendations: $REC_RESULT items returned"
else
    echo "❌ Recommendations: FAILED"
    echo "Response: $(curl -s -X POST "$API_URL/recommend" -H "content-type: application/json" -d '{"user_id":"u123","k":5,"recent_clicks":["n101","n205"]}')"
fi

echo
echo "🌐 Testing Frontend..."
FRONTEND_STATUS=$(curl -s -w "%{http_code}" -o /dev/null "$FRONTEND_URL")
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "✅ Frontend: Accessible"
else
    echo "❌ Frontend: HTTP $FRONTEND_STATUS"
fi

echo
echo "📊 Summary:"
echo "Backend API: $API_URL"
echo "Frontend: $FRONTEND_URL"
echo
echo "Next steps:"
echo "1. Open frontend URL in browser"
echo "2. Test user interactions (search, recommendations)" 
echo "3. Check browser DevTools Network tab for API calls"
echo "4. Monitor logs: az webapp log tail -g snr-rg -n snr-api"