# Dark Factory - Free Software Stack
## Zero-Cost Production Tools

**Date:** March 29, 2026  
**Requirement:** Best free software for hybrid production model  
**Total Cost:** $0

---

## 1. PRINTER MANAGEMENT

### OctoPrint (ESSENTIAL)
- **Cost:** FREE (GPLv3)
- **OS:** Linux (Raspberry Pi)
- **Features:**
  - Web interface for printer control
  - Upload and print G-code remotely
  - Monitor prints via webcam
  - Plugin ecosystem
  - Time-lapse recording
- **Install:** `pip install octoprint`
- **URL:** octoprint.org

### Alternative: Mainsail (Klipper-based)
- **Cost:** FREE
- **Better for:** Advanced users
- **Features:** Faster, more modern UI

---

## 2. 3D DESIGN/CAD

### FreeCAD (RECOMMENDED)
- **Cost:** FREE (LGPL)
- **OS:** Windows, Mac, Linux
- **Features:**
  - Parametric modeling
  - Professional-grade CAD
  - Export to STL/OBJ
  - CAM workbench (CNC paths)
- **URL:** freecad.org

### Blender (Organic shapes)
- **Cost:** FREE (GPL)
- **OS:** All platforms
- **Features:**
  - Advanced modeling
  - Sculpting
  - Great for artistic parts
- **URL:** blender.org

### Tinkercad (Beginner-friendly)
- **Cost:** FREE (browser-based)
- **Best for:** Quick prototypes, learning
- **URL:** tinkercad.com

---

## 3. SLICING SOFTWARE

### PrusaSlicer (BEST for Prusa printers)
- **Cost:** FREE
- **OS:** All platforms
- **Features:**
  - Optimized for Prusa
  - Auto supports
  - Variable layer height
  - Multi-material
- **URL:** prusa3d.com/prusaslicer

### Cura (Universal)
- **Cost:** FREE (LGPL)
- **OS:** All platforms
- **Features:**
  - Works with all printers
  - Extensive settings
  - Marketplace for plugins
  - Tree supports
- **URL:** ultimaker.com/software/cura

### OrcaSlicer (Advanced)
- **Cost:** FREE
- **Features:**
  - Based on Bambu Studio
  - Calibration tools
  - Klipper integration
- **URL:** github.com/SoftFever/OrcaSlicer

---

## 4. CNC MACHINING (When outsourcing CNC)

### FreeCAD Path Workbench
- **Cost:** FREE (included in FreeCAD)
- **Features:**
  - Generate G-code
  - 3-axis milling
  - Tool library
  - Post-processors

### CAMotics (Simulation)
- **Cost:** FREE
- **Features:**
  - Simulate G-code
  - Prevent crashes
  - Visualize toolpaths
- **URL:** camotics.org

---

## 5. JOB MANAGEMENT (Dark Factory)

### Already Built (Our Software)
- Dark Factory Scheduler ✅
- Job queue ✅
- Vendor management ✅
- **Cost:** $0 (already built)

---

## 6. COMMUNICATION/COLLABORATION

### Discord (Team chat)
- **Cost:** FREE tier sufficient
- **Features:**
  - Channels for projects
  - File sharing
  - Voice/video calls
- **URL:** discord.com

### Signal (Secure messaging)
- **Cost:** FREE
- **Features:**
  - End-to-end encryption
  - Group chats
- **URL:** signal.org

---

## 7. FILE STORAGE/SYNC

### Syncthing (Self-hosted)
- **Cost:** FREE
- **Features:**
  - P2P file sync
  - No cloud required
  - Cross-platform
- **URL:** syncthing.net

### Nextcloud (Self-hosted cloud)
- **Cost:** FREE
- **Features:**
  - File sync
  - Document editing
  - Calendar
  - Install on Raspberry Pi
- **URL:** nextcloud.com

---

## 8. MONITORING/ANALYTICS

### Grafana + Prometheus
- **Cost:** FREE
- **Features:**
  - Production dashboards
  - Job metrics
  - Printer status
  - Vendor performance
- **URL:** grafana.com

### Uptime Kuma
- **Cost:** FREE
- **Features:**
  - Monitor services
  - Alerts via Discord/email
  - Simple setup
- **URL:** github.com/louislam/uptime-kuma

---

## 9. DOCUMENTATION

### Obsidian (Knowledge base)
- **Cost:** FREE (personal use)
- **Features:**
  - Markdown notes
  - Graph view
  - Plugins
- **URL:** obsidian.md

### Docusaurus (Documentation site)
- **Cost:** FREE
- **Features:**
  - Professional docs
  - Version control
  - Search
- **URL:** docusaurus.io

---

## 10. FINANCIAL TRACKING

### Actual Budget (Self-hosted)
- **Cost:** FREE
- **Features:**
  - Budget tracking
  - Bank sync
  - Reports
- **URL:** actualbudget.org

### GnuCash
- **Cost:** FREE
- **Features:**
  - Double-entry accounting
  - Business features
- **URL:** gnucash.org

---

## COMPLETE SOFTWARE STACK

| Purpose | Software | Cost |
|---------|----------|------|
| Printer Control | OctoPrint | $0 |
| 3D Design | FreeCAD | $0 |
| Slicing | PrusaSlicer/Cura | $0 |
| CNC | FreeCAD Path | $0 |
| Job Management | Dark Factory | $0 |
| Communication | Discord/Signal | $0 |
| Storage | Syncthing | $0 |
| Monitoring | Grafana | $0 |
| Docs | Obsidian | $0 |
| Accounting | Actual | $0 |
| **TOTAL** | | **$0** |

---

## INSTALLATION ORDER

### On Raspberry Pi (OctoPrint):
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install OctoPrint
pip install octoprint

# Install Syncthing
curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
echo "deb https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
sudo apt update
sudo apt install syncthing

# Install Uptime Kuma (optional)
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
```

### On Workstation:
```bash
# Install FreeCAD
sudo apt install freecad

# Install PrusaSlicer
# Download from prusa3d.com

# Install Cura
# Download from ultimaker.com
```

---

## RECOMMENDED SETUP

### Minimum Viable (Free):
1. **OctoPrint** - Control printer
2. **Cura** - Slice models
3. **Tinkercad** - Basic design
4. **Dark Factory** - Job management

### Professional (Free):
1. **OctoPrint** - Printer control
2. **FreeCAD** - Advanced CAD
3. **PrusaSlicer** - Optimized slicing
4. **Syncthing** - File sync
5. **Dark Factory** - Complete system

---

**Prepared by:** Miles  
**Date:** 2026-03-29 03:07 UTC  
**Status:** All software identified, ready to install
