#!/bin/bash
#
# Test Binance API Connectivity
#
# This script tests the connection to Binance API and validates
# authentication credentials.
#
# Usage:
#   ./test-connection.sh
#
# Environment Variables:
#   BINANCE_API_KEY       - Your Binance API key (required)
#   BINANCE_API_SECRET    - Your Binance API secret (required)
#   BINANCE_BASE_URL      - Binance API base URL (optional)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Binance API Connection Test"
echo "=========================================="
echo ""

# Check environment variables
if [ -z "$BINANCE_API_KEY" ]; then
    echo -e "${RED}✗ BINANCE_API_KEY is not set${NC}"
    echo "  Please set your Binance API key:"
    echo "  export BINANCE_API_KEY='your_api_key'"
    exit 1
else
    # Mask the API key for display
    KEY_LENGTH=${#BINANCE_API_KEY}
    MASKED_KEY="${BINANCE_API_KEY:0:4}...${BINANCE_API_KEY: -4}"
    echo -e "${GREEN}✓ BINANCE_API_KEY is set${NC} ($MASKED_KEY)"
fi

if [ -z "$BINANCE_API_SECRET" ]; then
    echo -e "${RED}✗ BINANCE_API_SECRET is not set${NC}"
    echo "  Please set your Binance API secret:"
    echo "  export BINANCE_API_SECRET='your_api_secret'"
    exit 1
else
    # Mask the API secret for display
    SECRET_LENGTH=${#BINANCE_API_SECRET}
    MASKED_SECRET="${BINANCE_API_SECRET:0:4}...${BINANCE_API_SECRET: -4}"
    echo -e "${GREEN}✓ BINANCE_API_SECRET is set${NC} ($MASKED_SECRET)"
fi

# Set base URL
BASE_URL="${BINANCE_BASE_URL:-https://api.binance.com}"
echo -e "${GREEN}✓ Base URL${NC}: $BASE_URL"

echo ""
echo "------------------------------------------"
echo "Testing Public API (Exchange Info)"
echo "------------------------------------------"

# Test public endpoint
PUBLIC_RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}/api/v3/exchangeInfo" 2>/dev/null)
HTTP_CODE=$(echo "$PUBLIC_RESPONSE" | tail -n1)
BODY=$(echo "$PUBLIC_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    SYMBOL_COUNT=$(echo "$BODY" | grep -o '"symbol"' | wc -l)
    echo -e "${GREEN}✓ Public API is accessible${NC}"
    echo "  Available trading pairs: $SYMBOL_COUNT"
else
    echo -e "${RED}✗ Public API test failed${NC}"
    echo "  HTTP Status: $HTTP_CODE"
    echo "  Response: $BODY"
    exit 1
fi

echo ""
echo "------------------------------------------"
echo "Testing Authenticated API (Account)"
echo "------------------------------------------"

# Generate timestamp and signature
TIMESTAMP=$(date +%s000)
QUERY_STRING="timestamp=$TIMESTAMP"
SIGNATURE=$(echo -n "$QUERY_STRING" | openssl dgst -sha256 -hmac "$BINANCE_API_SECRET" | sed 's/^.* //')

# Test authenticated endpoint
AUTH_RESPONSE=$(curl -s -w "\n%{http_code}" \
    -H "X-MBX-APIKEY: $BINANCE_API_KEY" \
    "${BASE_URL}/api/v3/account?${QUERY_STRING}&signature=${SIGNATURE}" 2>/dev/null)

AUTH_HTTP_CODE=$(echo "$AUTH_RESPONSE" | tail -n1)
AUTH_BODY=$(echo "$AUTH_RESPONSE" | sed '$d')

if [ "$AUTH_HTTP_CODE" = "200" ]; then
    ACCOUNT_TYPE=$(echo "$AUTH_BODY" | grep -o '"accountType":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✓ Authenticated API is accessible${NC}"
    echo "  Account Type: $ACCOUNT_TYPE"
    
    # Count non-zero balances
    BALANCE_COUNT=$(echo "$AUTH_BODY" | grep -o '"asset":"[^"]*","free":"[^"]*"' | grep -v '"free":"0' | wc -l)
    echo "  Non-zero balances: $BALANCE_COUNT"
elif [ "$AUTH_HTTP_CODE" = "401" ]; then
    echo -e "${RED}✗ Authentication failed${NC}"
    echo "  Please check your API key and secret."
    echo "  Response: $AUTH_BODY"
    exit 1
elif [ "$AUTH_HTTP_CODE" = "429" ]; then
    echo -e "${YELLOW}⚠ Rate limit exceeded${NC}"
    echo "  Please wait before trying again."
    exit 1
else
    echo -e "${RED}✗ Authenticated API test failed${NC}"
    echo "  HTTP Status: $AUTH_HTTP_CODE"
    echo "  Response: $AUTH_BODY"
    exit 1
fi

echo ""
echo "------------------------------------------"
echo "Testing Rate Limit Headers"
echo "------------------------------------------"

# Check rate limit headers
RATE_LIMIT_RESPONSE=$(curl -s -I \
    -H "X-MBX-APIKEY: $BINANCE_API_KEY" \
    "${BASE_URL}/api/v3/account?${QUERY_STRING}&signature=${SIGNATURE}" 2>/dev/null)

WEIGHT_USED=$(echo "$RATE_LIMIT_RESPONSE" | grep -i "x-mbx-used-weight" | awk '{print $2}' | tr -d '\r')
WEIGHT_LIMIT=$(echo "$RATE_LIMIT_RESPONSE" | grep -i "x-mbx-weight-limit" | awk '{print $2}' | tr -d '\r')

if [ -n "$WEIGHT_USED" ]; then
    echo -e "${GREEN}✓ Rate limit headers present${NC}"
    echo "  Weight used: $WEIGHT_USED"
    if [ -n "$WEIGHT_LIMIT" ]; then
        echo "  Weight limit: $WEIGHT_LIMIT"
    fi
else
    echo -e "${YELLOW}⚠ Rate limit headers not found${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}All tests passed!${NC}"
echo "=========================================="
echo ""
echo "Your Binance API connection is working correctly."
echo "You can now use the crypto exchange API skill."
