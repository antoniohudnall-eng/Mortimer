#!/bin/bash
# CREW CRON SCHEDULE - SEED3 Fleet
# Install with: crontab ~/mortimer/crew_schedule/cron_schedule.sh

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MORNING OPS (06:00-08:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 6 * * * ~/mortimer/crew_schedule/activate_agent.sh miles wake_up "System health check initiated"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SALES TEAM (08:00-09:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 8 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh pulp start_shift "Good morning! New day, new opportunities."
0 8 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh c3p0 start_shift "Protocol droid online. Monitoring communications."
0 9 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh jane start_shift "Jane reporting for duty."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OPERATIONS (09:00-10:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 9 * * * ~/mortimer/crew_schedule/activate_agent.sh dusty start_shift "Crypto markets, time to trade."
0 9 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh hume start_shift "Regional operations commencing."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENGINEERING (10:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 10 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh stacktrace start_shift "Architecture review commencing."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LUNCH CHECK (12:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 12 * * * ~/mortimer/crew_schedule/check_status.sh "Lunch roll call"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AFTERNOON OPS (14:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 14 * * * ~/mortimer/crew_schedule/heartbeat_check.sh "Afternoon systems check"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# END OF DAY (17:00-18:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 17 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh pulp end_shift "End of day report."
0 17 * * * ~/mortimer/crew_schedule/activate_agent.sh dusty end_shift "Market close analysis."
0 18 * * 1-5 ~/mortimer/crew_schedule/activate_agent.sh hume end_shift "Daily wrap-up."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EVENING (22:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 22 * * * ~/mortimer/crew_schedule/activate_agent.sh miles night_mode "Entering night operations."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MIDNIGHT (00:00)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0 0 * * * ~/mortimer/crew_schedule/activate_agent.sh sentinel midnight_report "Security log review."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EVERY 30 MINUTES - HEALTH CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*/30 * * * * ~/mortimer/crew_schedule/quick_health.sh

