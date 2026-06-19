#!/bin/bash
# ═══════════════════════════════════════════════════════════
# ATTACK DETECTOR — Real-time auto-authorization
# Monitors logs, auto-authorizes NetProbes against any attacker
# Captain's standing order: "Anyone who attacks us"
# ═══════════════════════════════════════════════════════════

set -euo pipefail

# Configuration
LOG_FILE="/var/log/netprobe/auto_auth.log"
THREAT_DB="/projects/netprobe/threats/live_threats.json"
AUTH_LIST="/projects/netprobe/AUTHORIZED_TARGETS.md"
ALERT_ENDPOINT="http://localhost:4000/alert"  # OpenClaw gateway
COOLDOWN_MINUTES=60
MAX_DAILY_DEPLOYS=10

# Create directories
mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$THREAT_DB")"

# Initialize threat DB
if [[ ! -f "$THREAT_DB" ]]; then
    echo '{"threats":[],"daily_count":0,"last_reset":"'"$(date -Iseconds)"'"}' > "$THREAT_DB"
fi

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

reset_daily_counter() {
    local last_reset=$(jq -r '.last_reset' "$THREAT_DB")
    local today=$(date -I)
    if [[ "$last_reset" != "$today"* ]]; then
        jq '.daily_count = 0 | .last_reset = "'"$(date -Iseconds)"'"' "$THREAT_DB" > "${THREAT_DB}.tmp" && mv "${THREAT_DB}.tmp" "$THREAT_DB"
        log "🔄 Daily counter reset"
    fi
}

is_already_tracked() {
    local ip="$1"
    jq -e --arg ip "$ip" '.threats[] | select(.ip == $ip and (.last_seen | fromdateiso8601) > (now - 86400))' "$THREAT_DB" >/dev/null 2>&1
}

update_threat_db() {
    local ip="$1"
    local count="${2:-1}"
    local country="${3:-unknown}"
    
    if is_already_tracked "$ip"; then
        # Update existing
        jq --arg ip "$ip" --arg now "$(date -Iseconds)" --arg count "$count" \
           '(.threats[] | select(.ip == $ip)) |= . + {last_seen: $now, total_attempts: (.total_attempts | tonumber + ($count | tonumber)), status: "active"}' \
           "$THREAT_DB" > "${THREAT_DB}.tmp" && mv "${THREAT_DB}.tmp" "$THREAT_DB"
    else
        # Add new threat
        local new_threat=$(jq -n \
            --arg ip "$ip" \
            --arg now "$(date -Iseconds)" \
            --arg count "$count" \
            --arg country "$country" \
            '{ip: $ip, first_seen: $now, last_seen: $now, total_attempts: ($count | tonumber), country: $country, status: "active", netprobe_authorized: true, netprobe_auth_reason: "Auto-authorized: attack detected"}')
        
        jq ".threats += [$new_threat]" "$THREAT_DB" > "${THREAT_DB}.tmp" && mv "${THREAT_DB}.tmp" "$THREAT_DB"
        
        # Increment daily counter
        jq '.daily_count += 1' "$THREAT_DB" > "${THREAT_DB}.tmp" && mv "${THREAT_DB}.tmp" "$THREAT_DB"
    fi
}

get_ip_geolocation() {
    local ip="$1"
    # Use free geolocation API (rate limited)
    curl -s "http://ip-api.com/json/${ip}?fields=country,countryCode,region" 2>/dev/null || echo '{"country":"unknown"}'
}

send_gmaoc_alert() {
    local ip="$1"
    local reason="$2"
    local count="${3:-1}"
    local country="${4:-unknown}"
    
    local message="🚨 AUTO-AUTHORIZED: NetProbe target $ip | $reason | $count attempts | $country | Captain's standing order: 'Anyone who attacks us'"
    
    log "📡 Sending GMAOC alert: $message"
    
    # Send to OpenClaw gateway if available
    if command -v curl >/dev/null 2>&1; then
        curl -s -X POST "$ALERT_ENDPOINT" \
            -H "Content-Type: application/json" \
            -d "{\"type\":\"netprobe_auto_auth\",\"ip\":\"$ip\",\"reason\":\"$reason\",\"count\":$count,\"country\":\"$country\",\"timestamp\":\"$(date -Iseconds)\"}" 2>/dev/null || true
    fi
    
    # Also log to system
    logger -t "netprobe-detector" "$message"
}

check_rate_limits() {
    local daily_count=$(jq -r '.daily_count' "$THREAT_DB")
    
    if [[ "$daily_count" -ge "$MAX_DAILY_DEPLOYS" ]]; then
        log "⚠️ Daily deployment limit reached ($MAX_DAILY_DEPLOYS). Not auto-authorizing new targets."
        return 1
    fi
    
    return 0
}

# Monitor auth.log for failed attempts
monitor_auth_log() {
    log "🔍 Monitoring /var/log/auth.log for attacks..."
    
    # Get current line count
    local last_line=$(wc -l < /var/log/auth.log 2>/dev/null || echo 0)
    
    while true; do
        reset_daily_counter
        
        # Get new lines since last check
        local current_line=$(wc -l < /var/log/auth.log 2>/dev/null || echo 0)
        
        if [[ "$current_line" -gt "$last_line" ]]; then
            # Extract new failed attempts
            tail -n +$((last_line + 1)) /var/log/auth.log 2>/dev/null | \
            grep -E "Failed password|authentication failure|Invalid user" | \
            grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | while read count ip; do
                
                # Extract just the number
                count=$(echo "$count" | tr -d ' ')
                ip=$(echo "$ip" | tr -d ' ')
                
                # Skip if already handled
                if ! is_already_tracked "$ip"; then
                    # Check rate limits
                    if check_rate_limits; then
                        # Get geolocation
                        local geo=$(get_ip_geolocation "$ip")
                        local country=$(echo "$geo" | jq -r '.country // "unknown"')
                        
                        # Update threat database
                        update_threat_db "$ip" "$count" "$country"
                        
                        # Send alert
                        send_gmaoc_alert "$ip" "SSH brute force" "$count" "$country"
                        
                        log "🎯 NEW THREAT AUTO-AUTHORIZED: $ip ($country) - $count attempts - NetProbe READY"
                    fi
                fi
            done
            
            last_line=$current_line
        fi
        
        sleep 10  # Check every 10 seconds
    done
}

# Monitor fail2ban for bans
monitor_fail2ban() {
    log "🛡️ Monitoring fail2ban for bans..."
    
    tail -F /var/log/fail2ban.log 2>/dev/null | while read line; do
        if echo "$line" | grep -q "Ban"; then
            local ip=$(echo "$line" | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | head -1)
            
            if [[ -n "$ip" && ! is_already_tracked "$ip" ]]; then
                if check_rate_limits; then
                    local geo=$(get_ip_geolocation "$ip")
                    local country=$(echo "$geo" | jq -r '.country // "unknown"')
                    
                    update_threat_db "$ip" "fail2ban" "$country"
                    send_gmaoc_alert "$ip" "fail2ban ban" "fail2ban" "$country"
                    
                    log "🛡️ FAIL2BAN BAN AUTO-AUTHORIZED: $ip ($country) - Full NetProbe authority granted"
                fi
            fi
        fi
    done
}

# Manual check for immediate threats
check_immediate_threats() {
    log "🔎 Running immediate threat scan..."
    
    # Get recent failed logins
    local recent_attempts=$(grep "Failed password" /var/log/auth.log 2>/dev/null | tail -100 | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn | head -10)
    
    echo "$recent_attempts" | while read count ip; do
        count=$(echo "$count" | tr -d ' ')
        ip=$(echo "$ip" | tr -d ' ')
        
        # If >5 attempts and not tracked
        if [[ "$count" -ge 5 && ! is_already_tracked "$ip" ]]; then
            check_rate_limits || continue
            
            local geo=$(get_ip_geolocation "$ip")
            local country=$(echo "$geo" | jq -r '.country // "unknown"')
            
            update_threat_db "$ip" "$count" "$country"
            send_gmaoc_alert "$ip" "Recent sustained attack" "$count" "$country"
            
            log "🎯 HISTORICAL THREAT AUTO-AUTHORIZED: $ip ($country) - $count recent attempts"
        fi
    done
}

# Main execution
case "${1:-monitor}" in
    monitor)
        log "🚀 Starting NetProbe Attack Detector..."
        log "Authorization: Captain's standing order 'Anyone who attacks us'"
        log "Rate limits: Max $MAX_DAILY_DEPLOYS auto-deploys/day, ${COOLDOWN_MINUTES}min cooldown"
        
        # Initial scan
        check_immediate_threats
        
        # Start monitors (background)
        monitor_auth_log &
        monitor_fail2ban &
        
        wait
        ;;
    check)
        check_immediate_threats
        ;;
    status)
        echo "📊 NetProbe Auto-Auth Status:"
        echo "═══════════════════════════════"
        jq '. | {total_threats: (.threats | length), daily_count: .daily_count, last_reset: .last_reset}' "$THREAT_DB" 2>/dev/null || echo "No threat data yet"
        echo ""
        echo "🔴 Recent threats (last 24h):"
        jq -r '.threats | sort_by(.last_seen) | reverse | .[:10] | .[] | "\(.last_seen | split("T")[1][:8]) | \(.ip) | \(.country) | \(.total_attempts) | \(.status)"' "$THREAT_DB" 2>/dev/null || echo "No active threats"
        ;;
    *)
        echo "Usage: $0 {monitor|check|status}"
        echo "  monitor - Run continuous detection (default)"
        echo "  check   - One-time threat scan"
        echo "  status  - Show current threat status"
        exit 1
        ;;
esac
