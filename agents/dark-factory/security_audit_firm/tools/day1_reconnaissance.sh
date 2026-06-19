#!/bin/bash
# Sentinel Security - Day 1 Reconnaissance
# Dusty Wallet Penetration Test

OUTPUT_DIR="/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/security_audit_firm/reports"
mkdir -p $OUTPUT_DIR

REPORT_FILE="$OUTPUT_DIR/day1_recon_$(date +%Y%m%d_%H%M).txt"

echo "===============================================" > $REPORT_FILE
echo "SENTINEL SECURITY - DAY 1 RECONNAISSANCE" >> $REPORT_FILE
echo "Target: Dusty Wallet" >> $REPORT_FILE
echo "Started: $(date -Iseconds)" >> $REPORT_FILE
echo "===============================================" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# 1. API Endpoint Discovery
echo "[1] API ENDPOINT DISCOVERY" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
DUSTY_DIR="/root/.openclaw/workspace/aocros/dusty/backend/routes"
if [ -d "$DUSTY_DIR" ]; then
    echo "Routes found:" >> $REPORT_FILE
    ls -1 $DUSTY_DIR/*.js 2>/dev/null | while read route; do
        basename "$route" >> $REPORT_FILE
    done
    echo "" >> $REPORT_FILE
    
    # Extract endpoints from files
    echo "Endpoints discovered:" >> $REPORT_FILE
    grep -h "router\\.get\\|router\\.post\\|router\\.put\\|router\\.delete" $DUSTY_DIR/*.js 2>/dev/null | sed 's/^/  /' >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# 2. Authentication Flow Analysis
echo "[2] AUTHENTICATION FLOW ANALYSIS" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
AUTH_FILE="$DUSTY_DIR/auth.js"
if [ -f "$AUTH_FILE" ]; then
    echo "✓ Authentication module found" >> $REPORT_FILE
    grep -n "jwt\\|token\\|password\\|authenticate" $AUTH_FILE | head -20 >> $REPORT_FILE
else
    echo "⚠ Auth file not found" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# 3. Package Vulnerability Scan
echo "[3] DEPENDENCY VULNERABILITY SCAN" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
cd /root/.openclaw/workspace/aocros/dusty/backend
npm audit --json 2>/dev/null | python3 -c "
import json,sys
try:
    data=json.load(sys.stdin)
    print(f'Total dependencies: {data.get(\"metadata\", {}).get(\"dependencies\", {}).get(\"total\", \"N/A\")}')
    vulns = data.get('vulnerabilities', {})
    if vulns:
        print(f'Vulnerabilities found: {len(vulns)}')
        for id, info in vulns.items():
            print(f'  - {id}: {info.get(\"severity\")}')
    else:
        print('✓ No vulnerabilities found')
except Exception as e:
    print(f'Error parsing audit: {e}')
" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# 4. Configuration Review
echo "[4] CONFIGURATION REVIEW" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
ENV_FILE="/root/.openclaw/workspace/aocros/dusty/.env.production"
if [ -f "$ENV_FILE" ]; then
    echo "✓ Production environment file found" >> $REPORT_FILE
    echo "Variables configured:" >> $REPORT_FILE
    grep -E "^[A-Z_]+=" $ENV_FILE | cut -d= -f1 | sed 's/^/  - /' >> $REPORT_FILE
else
    echo "⚠ No .env.production file found" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# 5. Database Connection Security
echo "[5] DATABASE CONNECTION SECURITY" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
grep -n "MONGODB_URI\\|mongodb" /root/.openclaw/workspace/aocros/dusty/backend/services/database.js | head -10 >> $REPORT_FILE
echo "" >> $REPORT_FILE

# 6. Encryption Implementation Check
echo "[6] ENCRYPTION IMPLEMENTATION" >> $REPORT_FILE
echo "-------------------------------------------" >> $REPORT_FILE
ENCRYPT_FILE="/root/.openclaw/workspace/aocros/dusty/backend/services/encryption.js"
if [ -f "$ENCRYPT_FILE" ]; then
    echo "✓ Encryption service found" >> $REPORT_FILE
    grep -n "PBKDF2\\|AES-256\\|iterations\\|deriveKey" $ENCRYPT_FILE | head -10 >> $REPORT_FILE
else
    echo "⚠ Encryption service not found" >> $REPORT_FILE
fi
echo "" >> $REPORT_FILE

# 7. Summary
echo "===============================================" >> $REPORT_FILE
echo "DAY 1 RECONNAISSANCE COMPLETE" >> $REPORT_FILE
echo "Completed: $(date -Iseconds)" >> $REPORT_FILE
echo "Report: $REPORT_FILE" >> $REPORT_FILE
echo "===============================================" >> $REPORT_FILE

echo "Day 1 Reconnaissance Complete!"
echo "Report saved to: $REPORT_FILE"
cat $REPORT_FILE
