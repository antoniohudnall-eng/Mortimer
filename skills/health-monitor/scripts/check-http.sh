#!/bin/bash
# Check HTTP endpoint health

URL="$1"
TIMEOUT="${2:-5}"

if [ -z "$URL" ]; then
    echo "Usage: check-http.sh <url> [timeout_seconds]"
    exit 1
fi

response=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$TIMEOUT" "$URL" 2>/dev/null)

if [ "$response" = "200" ]; then
    echo "✅ HEALTHY - $URL (HTTP $response)"
    exit 0
else
    echo "❌ UNHEALTHY - $URL (HTTP ${response:-no response})"
    exit 1
fi
