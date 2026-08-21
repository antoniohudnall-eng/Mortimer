#!/bin/bash
# Monitor multiple services from a config file

CONFIG_FILE="$1"

if [ -z "$CONFIG_FILE" ] || [ ! -f "$CONFIG_FILE" ]; then
    echo "Usage: health-check.sh <services_config.txt>"
    exit 1
fi

FAILED=0
echo "Health Check Report - $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo ""

while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    
    # Check if it's a URL or process name
    if [[ "$line" =~ ^http ]]; then
        scripts/check-http.sh "$line" || ((FAILED++))
    else
        # Process check
        if pgrep -f "$line" > /dev/null; then
            echo "✅ HEALTHY - Process: $line (running)"
        else
            echo "❌ UNHEALTHY - Process: $line (not running)"
            ((FAILED++))
        fi
    fi
done < "$CONFIG_FILE"

echo ""
if [ $FAILED -eq 0 ]; then
    echo "All services healthy ✅"
    exit 0
else
    echo "$FAILED service(s) unhealthy ❌"
    exit 1
fi
