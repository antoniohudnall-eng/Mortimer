#!/bin/bash
# Sentinel Security - Day 3: API & Database Security
# Dusty Wallet Penetration Test

OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/security_audit_firm/reports"
mkdir -p $OUTPUT_DIR

REPORT_FILE="$OUTPUT_DIR/day3_api_security_$(date +%Y%m%d_%H%M).txt"
API_URL="http://localhost:3001/api"

echo "===============================================" > $REPORT_FILE
echo "SENTINEL SECURITY - DAY 3: API & DATABASE" >> $REPORT_FILE
echo "Target: Dusty Wallet" >> $REPORT_FILE
echo "Started: $(date -Iseconds)" >> $REPORT_FILE
echo "===============================================" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 1: SQL Injection
echo "[1] SQL INJECTION TESTS" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
echo "Testing login with SQL injection payload..." >> $REPORT_FILE

curl -s -X POST -H "Content-Type: application/json" \
    -d '{"email":"admin'\'' OR '\''1'\''='\''1","password":"anything"}' \
    "$API_URL/auth/login" 2>/dev/null | head -1 >> $REPORT_FILE

echo "" >> $REPORT_FILE
echo "Testing registration with union select..." >> $REPORT_FILE
curl -s -X POST -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test","name":"test'\'' UNION SELECT * FROM users--"}' \
    "$API_URL/auth/register" 2>/dev/null | head -1 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 2: NoSQL Injection
echo "[2] NOSQL INJECTION TESTS" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
curl -s -X POST -H "Content-Type: application/json" \
    -d '{"email":{"$ne":"null"},"password":{"$ne":"null"}}' \
    "$API_URL/auth/login" 2>/dev/null | head -1 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 3: IDOR (Insecure Direct Object Reference)
echo "[3] IDOR TESTS" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
echo "Testing wallet access without authentication..." >> $REPORT_FILE
curl -s "$API_URL/wallet/1" 2>/dev/null | head -1 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 4: Mass Assignment
echo "[4] MASS ASSIGNMENT TEST" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
curl -s -X POST -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test","name":"test","isAdmin":true,"role":"admin"}' \
    "$API_URL/auth/register" 2>/dev/null | head -1 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 5: API Rate Limiting
echo "[5] API RATE LIMITING TEST" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
echo "Sending 50 rapid requests to /api/health..." >> $REPORT_FILE
for i in {1..50}; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" 2>/dev/null)
    if [ "$HTTP_CODE" = "429" ]; then
        echo "Rate limit triggered at request $i" >> $REPORT_FILE
        break
    fi
done
echo "" >> $REPORT_FILE

# Test 6: CORS Misconfiguration
echo "[6] CORS CONFIGURATION TEST" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
curl -s -X OPTIONS -H "Origin: https://evil.com" \
    -H "Access-Control-Request-Method: POST" \
    "$API_URL/auth/login" 2>/dev/null | grep -i "access-control" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Test 7: Security Headers
echo "[7] SECURITY HEADERS TEST" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
curl -sI "$API_URL/health" 2>/dev/null | grep -E "X-Frame|X-Content|X-XSS|Strict-Transport" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Summary
echo "===============================================" >> $REPORT_FILE
echo "DAY 3 API & DATABASE TESTS COMPLETE" >> $REPORT_FILE
echo "Completed: $(date -Iseconds)" >> $REPORT_FILE
echo "Report: $REPORT_FILE" >> $REPORT_FILE
echo "===============================================" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "Next: Day 4 - Blockchain Security" >> $REPORT_FILE

echo "Day 3 API Security Tests Complete!"
cat $REPORT_FILE
