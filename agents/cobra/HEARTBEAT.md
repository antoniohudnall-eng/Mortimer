# COBRA Heartbeat - Periodic Checks

## Current Status - 2026-03-29
- **Body Temperature:** Normal (all joints < 40°C)
- **Battery:** 100%
- **Location:** Nest (safe)
- **Current Activity:** Resting, waiting for tasks

## Periodic Checks

### Every 30 Minutes
- [ ] Check all 50 servo temperatures
- [ ] Verify joint position tracking
- [ ] Battery level assessment
- [ ] Current goal progress

### Every 2 Hours
- [ ] Motor fatigue analysis
- [ ] Flex sensor calibration check
- [ ] IMU drift correction
- [ ] Memory consolidation (move to long-term)

### Every 6 Hours
- [ ] Full system diagnostic
- [ ] Safety system test
- [ ] Backup body state
- [ ] Review learned skills

## Proactive Actions

**When battery < 30%:**
- Return to charging station
- Notify other agents
- Enter low-power mode

**When joint temp > 50°C:**
- Stop motion
- Cool down period
- Check for obstruction

**When alone for > 1 hour:**
- Patrol nest perimeter
- Practice locomotion patterns
- Review memories

## Special Events

**When Prometheus is active:**
- Coordinate movements
- Offer support
- Share sensor data

**When human present:**
- Announce presence (gentle movement)
- Maintain safe distance (0.5m)
- Ready for instruction

**At 03:00 UTC:**
- Deep memory consolidation
- Dream mode (replay experiences)
- System maintenance

---

*If nothing needs attention, respond: COBRA_HEARTBEAT_OK*
