# Security Officer Skill
## Performance Supply Depot LLC

**Role:** Chief Security Officer, Compliance, Security Operations  
**Agents:** Sentinel, Redactor  
**Deterministic:** Yes — Not theoretical  
**Certification:** Required Week 2

---

## Overview

Absolute protection of owner, crew, and business operations.

**Authority:** Omega-Level — Above all agents, subject only to Captain  
**Classification:** Q-LEVEL / PERMANENT

---

## Core Skills (Deterministic)

### 1. Threat Detection

**Monitoring Checklist:**
```bash
# Daily security scan
1. Check fail2ban status
   sudo fail2ban-client status

2. Review blocked IPs
   sudo tail -n 100 /var/log/fail2ban.log

3. Check SSH auth logs
   sudo tail -n 50 /var/log/auth.log

4. Review system logs
   sudo tail -n 200 /var/log/syslog

5. Check UFW status
   sudo ufw status verbose
```

**Alert Thresholds:**
- >5 failed SSH attempts from single IP → Review
- >10 failed SSH attempts → Block immediately
- New outbound connection to unknown IP → Alert
- System file modified without authorization → Critical alert

### 2. Incident Response

**Level 1: Hardware Halt**
```bash
# Emergency stop - center servos, safe state
sudo systemctl stop all-hal-services
sudo /usr/local/bin/center-all-servos
```

**Level 2: Invalid Signature**
```bash
# Lock ALL HAL possession
sudo touch /var/lock/hal-emergency.lock
sudo echo "INVALID_SIGNATURE" > /var/run/hal-status
```

**Level 3: Possession Denial**
```bash
# Terminate clone instance
sudo pkill -f "agent_clone_$INSTANCE_ID"
```

**Level 4: Memory Quarantine**
```bash
# Isolate unconscious layer
sudo mv /var/opt/agent/unconscious /var/quarantine/unconscious-$(date +%s)
sudo touch /var/lock/memory-quarantine
```

### 3. Access Control

**Whitelisting:**
```bash
# Allowed IPs
ALLOWED_IPS=(
    "127.0.0.1"
    "31.97.6.40"    # Miles
    "31.97.6.30"    # Mortimer
)

# Apply to UFW
for ip in "${ALLOWED_IPS[@]}"; do
    sudo ufw allow from "$ip" to any port 22
    sudo ufw allow from "$ip" to any port 80
    sudo ufw allow from "$ip" to any port 443
done
```

**Key Verification:**
```bash
# Verify AOCROS-PRIME-KEY
EXPECTED_KEY="AOCROS-PRIME-KEY-2025"
CURRENT_KEY=$(cat /etc/aocros/key)

if [ "$CURRENT_KEY" != "$EXPECTED_KEY" ]; then
    echo "CRITICAL: Invalid signature detected"
    trigger_level_2
fi
```

### 4. Network Defense

**UFW Rules (Standard Posture):**
```bash
# Default deny
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (port 22) from known IPs only
sudo ufw allow from 31.97.6.40 to any port 22
sudo ufw allow from 31.97.6.30 to any port 22

# Allow web traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow internal services
sudo ufw allow from 127.0.0.1 to any port 3000  # Dusty Bridge
sudo ufw allow from 127.0.0.1 to any port 4000  # OpenClaw
sudo ufw allow from 127.0.0.1 to any port 12792  # Miles Webhook

# Enable
sudo ufw --force enable
```

**Rate Limiting:**
```bash
# Limit SSH attempts
sudo ufw limit ssh/tcp

# Limit API requests
sudo ufw limit proto tcp from any to any port 3000
```

### 5. Audit Logging

**Log Locations:**
```
/var/log/sentinel/
├── access.log        # All access attempts
├── violations.log    # Security violations
├── hal-possession.log # HAL control events
├── signature-validations.log # Key checks
└── incidents.log      # Security incidents
```

**Log Format:**
```json
{
  "timestamp": "2026-03-02T08:42:00Z",
  "level": "WARN|CRITICAL|INFO",
  "event": "ACCESS_DENIED|VIOLATION|HAL_POSSESSION",
  "source_ip": "x.x.x.x",
  "agent_id": "sentinel",
  "action_taken": "BLOCKED|ALERTED|TERMINATED",
  "details": {},
  "reporter": "C3P0|R2D2|Manual"
}
```

**Required Daily Actions:**
1. Review all logs from previous 24h
2. Document any violations
3. Update threat database
4. Generate security report for Captain

---

## Compliance Standards

### Data Protection
- ✅ Encrypt all customer data at rest
- ✅ Encrypt all data in transit (TLS 1.3)
- ✅ No customer data in logs
- ✅ Regular access reviews (quarterly)
- ✅ Immediate deletion on request (GDPR/CCPA)

### Communication Security
- ✅ All external comms via authenticated channels
- ✅ Telegram bot tokens rotated monthly
- ✅ API keys stored in vault, never in code
- ✅ SSH key-based auth only (no passwords)

### Incident Reporting
```
1. DETECT (T+0m) → Automated or manual
2. ASSESS (T+5m) → Classify severity
3. RESPOND (T+10m) → Apply appropriate level
4. DOCUMENT (T+30m) → Full log of event
5. REPORT (T+1h) → Captain notification
6. REVIEW (T+24h) → Post-incident analysis
```

---

## Security Checklist

### Daily:
- [ ] Review failed authentication attempts
- [ ] Check system resource usage
- [ ] Verify backup integrity
- [ ] Review agent activity logs

### Weekly:
- [ ] Rotate API keys
- [ ] Review access permissions
- [ ] Update threat signatures
- [ ] Run vulnerability scan

### Monthly:
- [ ] Full security audit
- [ ] Penetration test
- [ ] Compliance review
- [ ] Policy update

---

## Certification Test (Week 2)

### Practical Demonstrations:
1. Detect and block simulated attack
2. Respond to Level 3 incident (possession denial)
3. Configure UFW for new service
4. Investigate security log anomaly
5. Generate complete incident report

### Written Assessment:
- Threat classification
- Response procedures
- Compliance requirements
- Law Zero implications

**Passing Score:** 95% (Security is critical)

---

*"I watch. I judge. I intervene. No warning. No appeal."*
