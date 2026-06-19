#!/bin/bash
# PROBE TRACKER - SEED3
# Track all 53 NetProbes

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  🛰️  SEED3 PROBE TRACKER — $(date '+%Y-%m-%d %H:%M UTC')"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Top targets from HUD
TARGETS=(
  "178.62.233.87:Singapore-DO:302"
  "178.128.252.245:Singapore-DO:68"
  "162.243.74.50:US-NYC:39"
  "142.93.177.162:US-NYC:30"
  "165.245.177.151:US:25"
  "167.71.201.8:US:24"
  "165.245.143.157:US:24"
  "152.42.201.153:Singapore:24"
  "138.68.183.56:US:23"
  "143.198.8.121:Singapore:22"
)

echo "🎯 TOP 10 TARGETS:"
echo ""
printf "%-4s %-18s %-15s %-8s %s\n" "#" "IP" "Location" "Attempts" "Status"
printf "%-4s %-18s %-15s %-8s %s\n" "---" "------------------" "---------------" "--------" "------"

count=1
for target in "${TARGETS[@]}"; do
  IFS=':' read -r ip loc attempts <<< "$target"
  
  if ping -c 1 -W 2 "$ip" > /dev/null 2>&1; then
    status="🟢 UP"
  else
    status="🔴 DOWN"
  fi
  
  printf "%-4s %-18s %-15s %-8s %s\n" "$count" "$ip" "$loc" "$attempts" "$status"
  ((count++))
done

echo ""
echo "📡 Supplemental 6:"
echo ""
supp=(
  "157.245.145.241:Vultr:5"
  "170.64.144.29:DigitalOcean:3"
  "167.71.46.254:DigitalOcean:3"
  "138.68.173.67:DigitalOcean:3"
  "64.227.186.99:DigitalOcean:2"
  "164.92.142.205:DigitalOcean:2"
)

printf "%-4s %-18s %-15s %-8s %s\n" "#" "IP" "Provider" "Attempts" "Status"
for i in "${!supp[@]}"; do
  IFS=':' read -r ip prov attempts <<< "${supp[$i]}"
  if ping -c 1 -W 2 "$ip" > /dev/null 2>&1; then
    status="🟢 UP"
  else
    status="🔴 DOWN"
  fi
  printf "%-4s %-18s %-15s %-8s %s\n" "$((i+1))" "$ip" "$prov" "$attempts" "$status"
done

echo ""
echo "✅ Probe tracker complete"
