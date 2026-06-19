#!/bin/bash
# Sentinel Security - Day 2: Authentication Testing
# Dusty Wallet Penetration Test

OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/security_audit_firm/reports"
mkdir -p $OUTPUT_DIR

REPORT_FILE="$OUTPUT_DIR/day2_auth_$(date +%Y%m%d_%H%M).txt"
API_URL="http://localhost:3001/api"

echo "===============================================" > $REPORT_FILE
echo "SENTINEL SECURITY - DAY 2: AUTHENTICATION TESTS" >> $REPORT_FILE
echo "Target: Dusty Wallet" >> $REPORT_FILE
echo "Started: $(date -Iseconds)" >> $REPORT_FILE
echo "===============================================" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 1: Brute Force Resistance
echo "[1] BRUTE FORCE RESISTANCE TEST" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
echo "Attempting 10 rapid login requests..." >> $REPORT_FILE
echo "" >> $REPORT_FILE

for i in {1..10}; do
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Content-Type: application/json" \
        -d '{"email":"test@test.com","password":"wrongpassword"}' \
        "$API_URL/auth/login" 2>/dev/null)
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    echo "Request $i: HTTP $HTTP_CODE" >> $REPORT_FILE
    
    if [ "$HTTP_CODE" = "429" ]; then
        echo "✓ Rate limiting triggered at request $i" >> $REPORT_FILE
        break
    fi
    sleep 0.5
done
echo "" >> $REPORT_FILE

# Test 2: JWT Token Analysis
echo "[2] JWT TOKEN SECURITY" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
AUTH_FILE="/root/.openclaw/workspace/aocros/dusty/backend/routes/auth.js"
if [ -f "$AUTH_FILE" ]; then
    echo "Analyzing JWT implementation..." >> $REPORT_FILE
    
    # Check JWT secret configuration
    JWT_SECRET=$(grep -o "JWT_SECRET[^,]*" $AUTH_FILE | head -1)
    if [ -n "$JWT_SECRET" ]; then
        echo "✓ JWT_SECRET configured" >> $REPORT_FILE
    else
        echo "⚠ JWT_SECRET not found in code" >> $REPORT_FILE
    fi
    
    # Check token expiration
    JWT_EXPIRE=$(grep -o "expiresIn[^,]*" $AUTH_FILE | head -1)
    if [ -n "$JWT_EXPIRE" ]; then
        echo "✓ Token expiration: $JWT_EXPIRE" >> $REPORT_FILE
    else
        echo "⚠ Token expiration not set" >> $REPORT_FILE
    fi
    
    # Check bcrypt rounds
    BCRYPT_ROUNDS=$(grep -o "bcrypt.hash.*[0-9]" $AUTH_FILE | head -1)
    if [ -n "$BCRYPT_ROUNDS" ]; then
        echo "✓ Password hashing: $BCRYPT_ROUNDS" >> $REPORT_FILE
    fi
else
    echo "⚠ Auth file not found" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# Test 3: Input Validation
echo "[3] INPUT VALIDATION TESTS" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE

# SQL Injection attempt
echo "Testing SQL injection protection..." >> $REPORT_FILE
curl -s -X POST \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com\'; DROP TABLE users; --","password":"test"}' \
    "$API_URL/auth/login" 2>/dev/null | head -1 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# XSS attempt
echo "Testing XSS protection..." >> $REPORT_FILE
curl -s -X POST \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"<script>alert(1)</script>"}' \
    "$API_URL/auth/register" 2>/dev/null | head -1 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 4: Session Management
echo "[4] SESSION MANAGEMENT" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE

echo "Checking session configuration..." >> $REPORT_FILE
SERVER_FILE="/root/.openclaw/workspace/aocros/dusty/backend/server.js"
if [ -f "$SERVER_FILE" ]; then
    # Check for session middleware
    SESSION=$(grep -n "session" $SERVER_FILE | head -5)
    if [ -n "$SESSION" ]; then
        echo "✓ Session middleware found" >> $REPORT_FILE
    else
        echo "ℹ No session middleware (stateless JWT)" >> $REPORT_FILE
    fi
fi
echo "" >> $REPORT_FILE

# Test 5: Password Policy
echo "[5] PASSWORD POLICY" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE

echo "Testing weak password rejection..." >> $REPORT_FILE
# Test short password
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"123","name":"Test"}' \
    "$API_URL/auth/register" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "400" ]; then
    echo "✓ Weak password rejected (HTTP 400)" >> $REPORT_FILE
else
    echo "⚠ Weak password accepted (HTTP $HTTP_CODE)" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# Test 6: CORS Configuration
echo "[6] CORS SECURITY" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE

echo "Checking CORS configuration..." >> $REPORT_FILE
if [ -f "$SERVER_FILE" ]; then
    CORS=$(grep -A 3 "cors(" $SERVER_FILE | grep -o "origin.*")
    if [ -n "$CORS" ]; then
        echo "CORS origin config: $CORS" >> $REPORT_FILE
    else
        echo "⚠ CORS origin not restricted" >> $REPORT_FILE
    fi
fi
echo "" >> $REPORT_FILE

# Summary
echo "===============================================" >> $REPORT_FILE
echo "DAY 2 AUTHENTICATION TESTS COMPLETE" >> $REPORT_FILE
echo "Completed: $(date -Iseconds)" >> $REPORT_FILE
echo "Report: $REPORT_FILE" >> $REPORT_FILE
echo "===============================================" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "Next: Day 3 - API & Database Security" >> $REPORT_FILE

echo "Day 2 Authentication Tests Complete!"
echo "Report: $REPORT_FILE"
cat $REPORT_FILE
