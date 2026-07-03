#!/bin/bash
# Flyer Schedule Reminder Script
# Usage: ./flyer_reminder.sh [days_before_event] [event_name]

DAYS=$1
EVENT=$2

if [ -z "$DAYS" ] || [ -z "$EVENT" ]; then
    echo "Usage: ./flyer_reminder.sh [days_before] [event_name]"
    echo "Example: ./flyer_reminder.sh 7 'Labor Day'"
    exit 1
fi

echo "📅 FLIER REMINDER"
echo "=================="
echo "Event: $EVENT"
echo "Days until: $DAYS"
echo ""
echo "✅ Tasks:"
echo "1. Review flyer template"
echo "2. Update event date in flyer"
echo "3. Test links (psdepot.com)"
echo "4. Verify phone: 888-881-6834"
echo "5. Upload to email platform"
echo "6. Schedule send"
echo ""
echo "📍 Location: ~/mortimer/projects/psdepot_prospecting/flyer_templates/"
