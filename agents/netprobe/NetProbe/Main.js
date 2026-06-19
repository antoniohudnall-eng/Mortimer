// ═══════════════════════════════════════════════════════════
// NETPROBE MOBILE — DroidScript Edition
// GMAOC Tactical Command Center
// Captain's Personal HUD
// ═══════════════════════════════════════════════════════════

// App configuration
const APP_NAME = "NetProbe";
const APP_VERSION = "1.0.0-OMEGA";
const GMAOC_ID = "General Mortimer";

// Initialize app
app.SetOrientation("Landscape");
app.SetStatusBarColor("#000000");
app.SetTitleBarColor("#0d1117");
app.SetStatusBarLightTheme(false);
app.SetBackgroundColor("#0d1117");
app.EnableBackKey(false);
app.SetAppName("NetProbe");

// Global state
var g_state = {
    authorized: false,
    captainKey: "",
    sentinalKey: "",
    activeProbes: [],
    beacons: [],
    selectedTarget: null,
    hudMode: "globe" // globe, list, tactical
};

// ═══════════════════════════════════════════════════════════
// MAIN LAYOUT
// ═══════════════════════════════════════════════════════════

function OnStart() {
    // Create main layout
    layMain = app.CreateLayout("Linear", "Vertical,FillXY");
    layMain.SetBackgroundColor("#0d1117");
    
    // Header
    CreateHeader(layMain);
    
    // Tab bar
    CreateTabBar(layMain);
    
    // Content area (switches based on tab)
    layContent = app.CreateLayout("Frame", "FillXY");
    layContent.SetMargins(0, 0.01, 0, 0);
    layMain.AddChild(layContent);
    
    // Initialize tabs
    g_tabs = {
        globe: CreateGlobeView(),
        probes: CreateProbeControl(),
        beacons: CreateBeaconMonitor(),
        ears: CreateEARSInterface(),
        tactical: CreateTacticalView()
    };
    
    // Show default tab
    ShowTab("globe");
    
    // Add main layout
    app.AddLayout(layMain);
    
    // Authentication check
    ShowAuthDialog();
    
    // Start background services
    StartBeaconListener();
    StartProbeHeartbeat();
}

function CreateHeader(parent) {
    var layHeader = app.CreateLayout("Linear", "Horizontal,FillX");
    layHeader.SetBackgroundColor("#161b22");
    layHeader.SetPadding(0.02, 0.015, 0.02, 0.015);
    
    // Logo/icon
    var imgLogo = app.CreateImage(null, 0.08, -1, "Icon");
    imgLogo.SetImage("Img/Satellite.png"); // Will use fallback if not found
    layHeader.AddChild(imgLogo);
    
    // Title
    var txtTitle = app.CreateText("NETPROBE", 0.3, -1, "Bold,Left");
    txtTitle.SetTextColor("#58a6ff");
    txtTitle.SetTextSize(22);
    txtTitle.SetMargins(0.02, 0, 0, 0);
    layHeader.AddChild(txtTitle);
    
    // Status indicator
    g_txtStatus = app.CreateText("🔴 STANDBY", 0.25, -1, "Right");
    g_txtStatus.SetTextColor("#f85149");
    g_txtStatus.SetTextSize(14);
    layHeader.AddChild(g_txtStatus);
    
    // Menu button
    var btnMenu = app.CreateButton("☰", 0.12, 0.08, "Custom");
    btnMenu.SetStyle("#21262d", "#21262d", 5, "#30363d", 1, 0);
    btnMenu.SetTextColor("#c9d1d9");
    btnMenu.SetOnTouch(ShowMenu);
    layHeader.AddChild(btnMenu);
    
    parent.AddChild(layHeader);
}

function CreateTabBar(parent) {
    var layTabs = app.CreateLayout("Linear", "Horizontal,FillX");
    layTabs.SetBackgroundColor("#161b22");
    
    var tabs = [
        { id: "globe", icon: "🌐", label: "GLOBE" },
        { id: "probes", icon: "🛰️", label: "PROBES" },
        { id: "beacons", icon: "📡", label: "BEACONS" },
        { id: "ears", icon: "👂", label: "EARS" },
        { id: "tactical", icon: "⚔️", label: "TACTICAL" }
    ];
    
    g_tabButtons = {};
    
    for (var i = 0; i < tabs.length; i++) {
        var tab = tabs[i];
        var btn = app.CreateButton(tab.icon + " " + tab.label, 0.18, 0.07, "Custom");
        btn.SetStyle("#0d1117", "#0d1117", 0, "#30363d", 1, 0);
        btn.SetTextColor("#8b949e");
        btn.SetTextSize(11);
        btn.SetOnTouch(function(id) { return function() { ShowTab(id); }; }(tab.id));
        layTabs.AddChild(btn);
        g_tabButtons[tab.id] = btn;
    }
    
    parent.AddChild(layTabs);
}

// ═══════════════════════════════════════════════════════════
// GLOBE VIEW — Earth with scout/probe markers
// ═══════════════════════════════════════════════════════════

function CreateGlobeView() {
    var lay = app.CreateLayout("Frame", "FillXY");
    
    // Canvas for globe visualization
    var canvas = app.CreateImage(null, 1.0, 0.85);
    canvas.SetAutoUpdate(true);
    canvas.SetName("globeCanvas");
    lay.AddChild(canvas);
    
    // Draw globe
    setInterval(function() {
        DrawGlobe(canvas);
    }, 1000);
    
    // Info panel at bottom
    var layInfo = app.CreateLayout("Linear", "Vertical,FillX");
    layInfo.SetPosition(0, 0.75);
    layInfo.SetBackgroundColor("rgba(13,17,23,0.9)");
    layInfo.SetPadding(0.02, 0.01, 0.02, 0.01);
    
    g_txtGlobeInfo = app.CreateText("Select a marker...", 0.96, -1, "Left");
    g_txtGlobeInfo.SetTextColor("#c9d1d9");
    g_txtGlobeInfo.SetTextSize(12);
    layInfo.AddChild(g_txtGlobeInfo);
    
    lay.AddChild(layInfo);
    
    return lay;
}

function DrawGlobe(canvas) {
    // Clear canvas
    canvas.Clear("#0d1117");
    
    var w = canvas.GetWidth();
    var h = canvas.GetHeight();
    var cx = w / 2;
    var cy = h / 2;
    var radius = Math.min(w, h) * 0.35;
    
    // Draw Earth outline (simple circle representation)
    canvas.DrawCircle(cx, cy, radius, "#21262d", 2);
    
    // Draw continents (simplified as dots for performance)
    DrawContinents(canvas, cx, cy, radius);
    
    // Draw markers for beacons and probes
    DrawMarkers(canvas, cx, cy, radius);
    
    // Draw grid lines
    DrawGlobeGrid(canvas, cx, cy, radius);
    
    // Update
    canvas.Update();
}

function DrawContinents(canvas, cx, cy, r) {
    // Simplified continent points (lat/lon converted to screen)
    var continents = [
        // North America
        {lat: 45, lon: -100, color: "#30363d"},
        {lat: 35, lon: -95, color: "#30363d"},
        {lat: 40, lon: -75, color: "#30363d"},
        // Europe
        {lat: 50, lon: 10, color: "#30363d"},
        {lat: 45, lon: 15, color: "#30363d"},
        // Asia
        {lat: 35, lon: 105, color: "#30363d"},
        {lat: 1, lon: 104, color: "#30363d"}, // Singapore
        // Add more points as needed
    ];
    
    for (var i = 0; i < continents.length; i++) {
        var pt = LatLonToXY(continents[i].lat, continents[i].lon, cx, cy, r);
        canvas.DrawCircle(pt.x, pt.y, r * 0.03, continents[i].color, 0, continents[i].color);
    }
}

function DrawMarkers(canvas, cx, cy, r) {
    // Command base (center dot, no coordinates)
    canvas.DrawCircle(cx, cy, r * 0.05, "#21262d", 2, "#58a6ff");
    canvas.DrawText("🏠", cx - r*0.02, cy + r*0.015, "#58a6ff");
    
    // External beacons/scouts
    g_state.beacons.forEach(function(beacon) {
        if (beacon.external && beacon.lat && beacon.lon) {
            var pt = LatLonToXY(beacon.lat, beacon.lon, cx, cy, r);
            var color = beacon.status === "overdue" ? "#f85149" : 
                       beacon.status === "wounded" ? "#d29922" : "#3fb950";
            
            canvas.DrawCircle(pt.x, pt.y, r * 0.03, color, 0, color);
            canvas.DrawText(beacon.icon || "📡", pt.x - r*0.015, pt.y + r*0.012, color);
            
            // Add click handler (simulated with touch detection)
        }
    });
    
    // Active probes
    g_state.activeProbes.forEach(function(probe) {
        if (probe.lat && probe.lon) {
            var pt = LatLonToXY(probe.lat, probe.lon, cx, cy, r);
            canvas.DrawCircle(pt.x, pt.y, r * 0.04, "#a371f7", 2, "#8957e5");
            canvas.DrawText("🛰️", pt.x - r*0.02, pt.y + r*0.015, "#a371f7");
        }
    });
}

function DrawGlobeGrid(canvas, cx, cy, r) {
    // Draw longitude lines
    for (var i = -180; i <= 180; i += 30) {
        var start = LatLonToXY(-90, i, cx, cy, r);
        var end = LatLonToXY(90, i, cx, cy, r);
        canvas.DrawLine(start.x, start.y, end.x, end.y, "#21262d", 1);
    }
    
    // Draw latitude lines
    for (var i = -90; i <= 90; i += 30) {
        var start = LatLonToXY(i, -180, cx, cy, r);
        var end = LatLonToXY(i, 180, cx, cy, r);
        canvas.DrawLine(start.x, start.y, end.x, end.y, "#21262d", 1);
    }
}

function LatLonToXY(lat, lon, cx, cy, r) {
    // Equirectangular projection (simplified)
    var x = cx + (lon / 180) * r * 0.9;
    var y = cy - (lat / 90) * r * 0.45;
    return {x: x, y: y};
}

// ═══════════════════════════════════════════════════════════
// PROBE CONTROL — Launch NetProbes
// ═══════════════════════════════════════════════════════════

function CreateProbeControl() {
    var lay = app.CreateLayout("Linear", "Vertical,FillXY");
    lay.SetPadding(0.02, 0.01, 0.02, 0.01);
    
    // Title
    var txtTitle = app.CreateText("🛰️ NETPROBE LAUNCH CONTROL", -1, -1, "Bold,Left");
    txtTitle.SetTextColor("#58a6ff");
    txtTitle.SetTextSize(16);
    lay.AddChild(txtTitle);
    
    // Divider
    var div1 = app.CreateText("", -1, 0.002);
    div1.SetBackColor("#30363d");
    lay.AddChild(div1);
    
    // Target selection
    var txtTarget = app.CreateText("TARGET SELECTION", -1, -1, "Bold,Left");
    txtTarget.SetTextColor("#8b949e");
    txtTarget.SetTextSize(12);
    txtTarget.SetMargins(0, 0.02, 0, 0.01);
    lay.AddChild(txtTarget);
    
    // IP input
    var layIP = app.CreateLayout("Linear", "Horizontal,FillX");
    var txtIPLabel = app.CreateText("IP: ", 0.08, -1, "Left");
    txtIPLabel.SetTextColor("#c9d1d9");
    layIP.AddChild(txtIPLabel);
    
    g_inpTargetIP = app.CreateTextEdit("138.68.179.165", 0.6, -1, "Number");
    g_inpTargetIP.SetTextColor("#c9d1d9");
    g_inpTargetIP.SetBackColor("#21262d");
    g_inpTargetIP.SetHint("Enter target IP");
    layIP.AddChild(g_inpTargetIP);
    
    // Lookup button
    var btnLookup = app.CreateButton("🔍", 0.15, 0.07, "Custom");
    btnLookup.SetStyle("#238636", "#238636", 5, "#2ea043", 1, 0);
    btnLookup.SetTextColor("#ffffff");
    btnLookup.SetOnTouch(LookupIPGeolocation);
    layIP.AddChild(btnLookup);
    
    lay.AddChild(layIP);
    
    // Mode selection
    var txtMode = app.CreateText("OPERATION MODE", -1, -1, "Bold,Left");
    txtMode.SetTextColor("#8b949e");
    txtMode.SetTextSize(12);
    txtMode.SetMargins(0, 0.02, 0, 0.01);
    lay.AddChild(txtMode);
    
    // Mode buttons
    var layModes = app.CreateLayout("Linear", "Horizontal,FillX");
    
    g_btnModes = {};
    var modes = [
        { id: "passive", icon: "👁️", name: "EYES" },
        { id: "ears", icon: "👂", name: "EARS" },
        { id: "both", icon: "👁️👂", name: "BOTH" },
        { id: "honeypot", icon: "🍯", name: "HONEYPOT" }
    ];
    
    modes.forEach(function(mode) {
        var btn = app.CreateButton(mode.icon + "\n" + mode.name, 0.22, 0.12, "Custom,Multiline");
        btn.SetStyle("#21262d", "#30363d", 5, "#30363d", 1, 0);
        btn.SetTextColor("#c9d1d9");
        btn.SetTextSize(10);
        btn.SetOnTouch(function() { SelectMode(mode.id); });
        layModes.AddChild(btn);
        g_btnModes[mode.id] = btn;
    });
    
    lay.AddChild(layModes);
    g_selectedMode = "passive";
    UpdateModeButtons();
    
    // Duration slider
    var txtDuration = app.CreateText("DURATION: 1 HOUR", -1, -1, "Bold,Left");
    txtDuration.SetTextColor("#8b949e");
    txtDuration.SetTextSize(12);
    txtDuration.SetMargins(0, 0.02, 0, 0);
    lay.AddChild(txtDuration);
    g_txtDuration = txtDuration;
    
    var sldDuration = app.CreateSeekBar(0.9, -1);
    sldDuration.SetRange(3600); // 1 hour max in seconds
    sldDuration.SetValue(3600);
    sldDuration.SetOnChange(function(value) {
        var hours = Math.floor(value / 3600);
        var mins = Math.floor((value % 3600) / 60);
        g_txtDuration.SetText("DURATION: " + hours + "h " + mins + "m");
        g_probeDuration = value;
    });
    lay.AddChild(sldDuration);
    g_probeDuration = 3600;
    
    // MNEMOSYNE option
    var layMN = app.CreateLayout("Linear", "Horizontal,FillX");
    layMN.SetMargins(0, 0.02, 0, 0);
    
    g_chkMNEMOSYNE = app.CreateCheckBox("🧠⚔️ MNEMOSYNE Protection");
    g_chkMNEMOSYNE.SetTextColor("#d29922");
    g_chkMNEMOSYNE.SetChecked(true);
    layMN.AddChild(g_chkMNEMOSYNE);
    
    lay.AddChild(layMN);
    
    // Launch button
    var btnLaunch = app.CreateButton("🚀 LAUNCH NETPROBE", -1, 0.1, "Custom");
    btnLaunch.SetStyle("#238636", "#2ea043", 10, "#3fb950", 2, 0);
    btnLaunch.SetTextColor("#ffffff");
    btnLaunch.SetTextSize(16);
    btnLaunch.SetMargins(0, 0.03, 0, 0);
    btnLaunch.SetOnTouch(LaunchProbe);
    lay.AddChild(btnLaunch);
    
    // Active probes list
    var txtActive = app.CreateText("ACTIVE PROBES", -1, -1, "Bold,Left");
    txtActive.SetTextColor("#8b949e");
    txtActive.SetTextSize(12);
    txtActive.SetMargins(0, 0.03, 0, 0.01);
    lay.AddChild(txtActive);
    
    g_layActiveProbes = app.CreateLayout("Linear", "Vertical,FillX");
    lay.AddChild(g_layActiveProbes);
    
    return lay;
}

function SelectMode(mode) {
    g_selectedMode = mode;
    UpdateModeButtons();
}

function UpdateModeButtons() {
    for (var id in g_btnModes) {
        var btn = g_btnModes[id];
        if (id === g_selectedMode) {
            btn.SetStyle("#238636", "#2ea043", 5, "#3fb950", 2, 0);
            btn.SetTextColor("#ffffff");
        } else {
            btn.SetStyle("#21262d", "#30363d", 5, "#30363d", 1, 0);
            btn.SetTextColor("#c9d1d9");
        }
    }
}

function LaunchProbe() {
    if (!g_state.authorized) {
        app.ShowPopup("⛔ NOT AUTHORIZED — Authenticate first!");
        return;
    }
    
    var ip = g_inpTargetIP.GetText();
    if (!ValidateIP(ip)) {
        app.ShowPopup("❌ Invalid IP address");
        return;
    }
    
    // Check if target on authorized list
    if (!IsAuthorizedTarget(ip)) {
        app.ShowPopup("⛔ TARGET NOT AUTHORIZED\nRequires Captain + Sentinal");
        return;
    }
    
    var mode = g_selectedMode;
    var duration = g_probeDuration;
    var mnemosyne = g_chkMNEMOSYNE.GetChecked();
    
    // Build probe config
    var probe = {
        id: "probe-" + ip.replace(/\./g, "-") + "-" + Date.now(),
        target: ip,
        mode: mode,
        duration: duration,
        mnemosyne: mnemosyne,
        launched: new Date().toISOString(),
        status: "launching",
        lat: null,
        lon: null
    };
    
    // Launch via API
    LaunchNetProbeAPI(probe);
    
    // Add to active probes
    g_state.activeProbes.push(probe);
    
    // Show confirmation
    app.ShowPopup("🚀 NETPROBE LAUNCHED\nTarget: " + ip + "\nMode: " + mode.toUpperCase());
    
    // Update UI
    UpdateActiveProbesList();
    UpdateStatus("🟢 " + g_state.activeProbes.length + " PROBES ACTIVE");
}

// ═══════════════════════════════════════════════════════════
// BEACON MONITOR — Scout tracking
// ═══════════════════════════════════════════════════════════

function CreateBeaconMonitor() {
    var lay = app.CreateLayout("Linear", "Vertical,FillXY");
    lay.SetPadding(0.02, 0.01, 0.02, 0.01);
    
    // Title
    var txtTitle = app.CreateText("📡 SCOUT BEACON NETWORK", -1, -1, "Bold,Left");
    txtTitle.SetTextColor("#58a6ff");
    txtTitle.SetTextSize(16);
    lay.AddChild(txtTitle);
    
    // Divider
    lay.AddChild(app.CreateText("", -1, 0.002, "", "#30363d"));
    
    // Summary stats
    var layStats = app.CreateLayout("Linear", "Horizontal,FillX");
    layStats.SetMargins(0, 0.02, 0, 0.01);
    
    g_txtBeaconStats = app.CreateText("🟢 0 Active | 🟡 0 Warning | 🔴 0 Overdue", -1, -1, "Left");
    g_txtBeaconStats.SetTextColor("#c9d1d9");
    g_txtBeaconStats.SetTextSize(12);
    layStats.AddChild(g_txtBeaconStats);
    
    lay.AddChild(layStats);
    
    // Beacon list
    g_layBeaconList = app.CreateLayout("Linear", "Vertical,FillX");
    lay.AddChild(g_layBeaconList);
    
    // Refresh button
    var btnRefresh = app.CreateButton("🔄 CHECK BEACONS", -1, 0.08, "Custom");
    btnRefresh.SetStyle("#21262d", "#30363d", 10, "#30363d", 1, 0);
    btnRefresh.SetTextColor("#58a6ff");
    btnRefresh.SetMargins(0, 0.02, 0, 0);
    btnRefresh.SetOnTouch(RefreshBeacons);
    lay.AddChild(btnRefresh);
    
    // Emergency ping
    var btnPing = app.CreateButton("📢 EMERGENCY PING MYLONEN", -1, 0.08, "Custom");
    btnPing.SetStyle("#da3633", "#f85149", 10, "#f85149", 1, 0);
    btnPing.SetTextColor("#ffffff");
    btnPing.SetMargins(0, 0.02, 0, 0);
    btnPing.SetOnTouch(EmergencyPingMylonen);
    lay.AddChild(btnPing);
    
    return lay;
}

// ═══════════════════════════════════════════════════════════
// EARS INTERFACE — Audio intercept
// ═══════════════════════════════════════════════════════════

function CreateEARSInterface() {
    var lay = app.CreateLayout("Linear", "Vertical,FillXY");
    lay.SetPadding(0.02, 0.01, 0.02, 0.01);
    
    // Title
    var txtTitle = app.CreateText("👂 EARS — AUDIO INTELLIGENCE", -1, -1, "Bold,Left");
    txtTitle.SetTextColor("#a371f7");
    txtTitle.SetTextSize(16);
    lay.AddChild(txtTitle);
    
    // Divider
    lay.AddChild(app.CreateText("", -1, 0.002, "", "#a371f7"));
    
    // Active intercepts
    var txtIntercepts = app.CreateText("🎧 ACTIVE INTERCEPTS", -1, -1, "Bold,Left");
    txtIntercepts.SetTextColor("#8b949e");
    txtIntercepts.SetTextSize(12);
    txtIntercepts.SetMargins(0, 0.02, 0, 0.01);
    lay.AddChild(txtIntercepts);
    
    g_layEARSList = app.CreateLayout("Linear", "Vertical,FillX");
    lay.AddChild(g_layEARSList);
    
    // Keyword filter
    var txtFilter = app.CreateText("KEYWORD ALERTS", -1, -1, "Bold,Left");
    txtFilter.SetTextColor("#8b949e");
    txtFilter.SetTextSize(12);
    txtFilter.SetMargins(0, 0.03, 0, 0.01);
    lay.AddChild(txtFilter);
    
    var keywords = ["brute force", "password", "exploit", "root", "attack"];
    var layKeywords = app.CreateLayout("Linear", "Horizontal,FillX");
    
    keywords.forEach(function(kw) {
        var chip = app.CreateText("⚠️ " + kw, -1, -1, "Left");
        chip.SetTextColor("#d29922");
        chip.SetMargins(0.01, 0.005, 0.01, 0.005);
        layKeywords.AddChild(chip);
    });
    
    lay.AddChild(layKeywords);
    
    return lay;
}

// ═══════════════════════════════════════════════════════════
// TACTICAL VIEW — Combined status
// ═══════════════════════════════════════════════════════════

function CreateTacticalView() {
    var lay = app.CreateLayout("Linear", "Vertical,FillXY");
    lay.SetPadding(0.02, 0.01, 0.02, 0.01);
    
    // Title
    var txtTitle = app.CreateText("⚔️ GMAOC TACTICAL OVERVIEW", -1, -1, "Bold,Left");
    txtTitle.SetTextColor("#f85149");
    txtTitle.SetTextSize(16);
    lay.AddChild(txtTitle);
    
    // Status boxes
    var layGrid = app.CreateLayout("Linear", "Horizontal,FillX");
    
    // Box 1: Probes
    var boxProbes = CreateStatusBox("🛰️ PROBES", "0", "#238636");
    layGrid.AddChild(boxProbes);
    
    // Box 2: Beacons  
    var boxBeacons = CreateStatusBox("📡 BEACONS", "0", "#58a6ff");
    layGrid.AddChild(boxBeacons);
    
    // Box 3: Alerts
    var boxAlerts = CreateStatusBox("🚨 ALERTS", "0", "#da3633");
    layGrid.AddChild(boxAlerts);
    
    lay.AddChild(layGrid);
    
    // Recent events
    var txtEvents = app.CreateText("📝 RECENT EVENTS", -1, -1, "Bold,Left");
    txtEvents.SetTextColor("#8b949e");
    txtEvents.SetTextSize(12);
    txtEvents.SetMargins(0, 0.02, 0, 0.01);
    lay.AddChild(txtEvents);
    
    g_layEvents = app.CreateLayout("Linear", "Vertical,FillX");
    lay.AddChild(g_layEvents);
    
    AddEvent("14:24 UTC — NetProbe system initialized");
    AddEvent("14:24 UTC — DroidScript app launched");
    
    return lay;
}

function CreateStatusBox(title, value, color) {
    var lay = app.CreateLayout("Linear", "Vertical");
    lay.SetBackgroundColor("#161b22");
    lay.SetPadding(0.02, 0.02, 0.02, 0.02);
    lay.SetMargins(0.005, 0.005, 0.005, 0.005);
    
    var txtTitle = app.CreateText(title, 0.25, -1, "Center");
    txtTitle.SetTextColor("#8b949e");
    txtTitle.SetTextSize(10);
    lay.AddChild(txtTitle);
    
    var txtValue = app.CreateText(value, 0.25, -1, "Bold,Center");
    txtValue.SetTextColor(color);
    txtValue.SetTextSize(28);
    lay.AddChild(txtValue);
    
    return lay;
}

// ═══════════════════════════════════════════════════════════
// CORE FUNCTIONS
// ═══════════════════════════════════════════════════════════

function ShowTab(tabId) {
    // Hide all tab content
    layContent.RemoveChild(g_tabs[g_currentTab]);
    
    // Update button colors
    for (var id in g_tabButtons) {
        var btn = g_tabButtons[id];
        if (id === tabId) {
            btn.SetBackgroundColor("#238636");
            btn.SetTextColor("#ffffff");
        } else {
            btn.SetBackgroundColor("#0d1117");
            btn.SetTextColor("#8b949e");
        }
    }
    
    // Show selected tab
    layContent.AddChild(g_tabs[tabId]);
    g_currentTab = tabId;
}

function ShowAuthDialog() {
    var dlg = app.CreateDialog("🔐 DUAL-KEY AUTHENTICATION");
    dlg.SetBackColor("#161b22");
    
    var layDlg = app.CreateLayout("Linear", "Vertical");
    layDlg.SetPadding(0.05, 0.05, 0.05, 0.05);
    
    var txtInfo = app.CreateText("Enter Captain + Sentinal keys", -1, -1, "Left,Multiline");
    txtInfo.SetTextColor("#8b949e");
    txtInfo.SetTextSize(12);
    layDlg.AddChild(txtInfo);
    
    // Captain key
    var txtCap = app.CreateText("Captain Key:", -1, -1, "Left");
    txtCap.SetTextColor("#c9d1d9");
    layDlg.AddChild(txtCap);
    
    var inpCaptain = app.CreateTextEdit("", -1, 0.08);
    inpCaptain.SetBackColor("#0d1117");
    inpCaptain.SetTextColor("#58a6ff");
    inpCaptain.SetHint("Daily passphrase");
    layDlg.AddChild(inpCaptain);
    
    // Sentinal key
    var txtSent = app.CreateText("Sentinal Key:", -1, -1, "Left");
    txtSent.SetTextColor("#c9d1d9");
    layDlg.AddChild(txtSent);
    
    var inpSentinal = app.CreateTextEdit("", -1, 0.08);
    inpSentinal.SetBackColor("#0d1117");
    inpSentinal.SetTextColor("#f85149");
    inpSentinal.SetHint("CSO authorization");
    layDlg.AddChild(inpSentinal);
    
    // Authenticate button
    var btnAuth = app.CreateButton("🔓 AUTHENTICATE", -1, 0.1, "Custom");
    btnAuth.SetStyle("#238636", "#2ea043", 10, "#3fb950", 2, 0);
    btnAuth.SetTextColor("#ffffff");
    btnAuth.SetOnTouch(function() {
        // In production, validate against secure keys
        g_state.authorized = true;
        g_state.captainKey = inpCaptain.GetText();
        g_state.sentinalKey = inpSentinal.GetText();
        dlg.Hide();
        UpdateStatus("🟢 AUTHORIZED");
        app.ShowPopup("✅ DUAL-KEY AUTHENTICATED");
    });
    layDlg.AddChild(btnAuth);
    
    dlg.AddLayout(layDlg);
    dlg.Show();
}

function UpdateStatus(status) {
    if (g_txtStatus) {
        g_txtStatus.SetText(status);
        g_txtStatus.SetTextColor(status.includes("🟢") ? "#3fb950" : 
                                 status.includes("🟡") ? "#d29922" : "#f85149");
    }
}

function AddEvent(message) {
    if (g_layEvents) {
        var txt = app.CreateText("• " + message, -1, -1, "Left");
        txt.SetTextColor("#8b949e");
        txt.SetTextSize(11);
        g_layEvents.AddChild(txt);
    }
}

// ═══════════════════════════════════════════════════════════
// API & NETWORK FUNCTIONS
// ═══════════════════════════════════════════════════════════

function LaunchNetProbeAPI(probe) {
    // In production, this calls the actual NetProbe launcher
    // For now, simulate with timeout
    setTimeout(function() {
        probe.status = "active";
        probe.lat = 1.35 + (Math.random() * 0.1 - 0.05); // Simulated Singapore
        probe.lon = 103.8 + (Math.random() * 0.1 - 0.05);
        AddEvent(probe.target + " — Probe ACTIVE");
        app.ShowPopup("🛰️ Probe " + probe.id + " ACTIVE");
    }, 2000);
}

function LookupIPGeolocation() {
    var ip = g_inpTargetIP.GetText();
    app.ShowPopup("🔍 Looking up " + ip + "...");
    
    // Simulate geolocation lookup
    setTimeout(function() {
        app.ShowPopup("📍 " + ip + " → Singapore (1.35°N, 103.8°E)");
    }, 1500);
}

function IsAuthorizedTarget(ip) {
    // Check against authorized threat list
    var authorized = ["138.68.179.165", "170.64.213.42", "170.64.228.51"];
    return authorized.indexOf(ip) !== -1;
}

function ValidateIP(ip) {
    return /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(ip);
}

function StartBeaconListener() {
    // Background service to check for beacon signals
    setInterval(function() {
        // In production, check actual beacon endpoint
        CheckBeaconUpdates();
    }, 30000); // Every 30 seconds
}

function CheckBeaconUpdates() {
    // Simulate beacon data
    g_state.beacons = [
        { id: "mylonen", name: "Mylonen", status: "overdue", lat: 1.35, lon: 103.8, external: true, icon: "🔴" },
        { id: "mylthreess", name: "Mylthreess", status: "nominal", lat: 51.5, lon: -0.1, external: true, icon: "🟢" },
        { id: "mylfours", name: "Mylfours", status: "nominal", lat: 50.1, lon: 8.7, external: true, icon: "🟢" }
    ];
}

function StartProbeHeartbeat() {
    // Update probe status periodically
    setInterval(function() {
        UpdateActiveProbesList();
        UpdateBeaconStats();
    }, 10000);
}

function UpdateActiveProbesList() {
    // Update UI with active probes
    if (g_layActiveProbes) {
        g_layActiveProbes.RemoveAllChildren();
        
        g_state.activeProbes.forEach(function(probe) {
            var layProbe = app.CreateLayout("Linear", "Horizontal,FillX");
            layProbe.SetBackgroundColor("#21262d");
            layProbe.SetMargins(0, 0.005, 0, 0.005);
            
            var statusIcon = probe.status === "active" ? "🟢" : "🟡";
            var txt = app.CreateText(statusIcon + " " + probe.target + " [" + probe.mode + "]", -1, -1, "Left");
            txt.SetTextColor("#c9d1d9");
            layProbe.AddChild(txt);
            
            g_layActiveProbes.AddChild(layProbe);
        });
    }
}

function UpdateBeaconStats() {
    if (g_txtBeaconStats) {
        var active = g_state.beacons.filter(b => b.status === "nominal").length;
        var warning = g_state.beacons.filter(b => b.status === "wounded").length;
        var overdue = g_state.beacons.filter(b => b.status === "overdue").length;
        g_txtBeaconStats.SetText("🟢 " + active + " Active | 🟡 " + warning + " Warning | 🔴 " + overdue + " Overdue");
    }
}

function RefreshBeacons() {
    app.ShowPopup("🔄 Refreshing beacon status...");
    CheckBeaconUpdates();
    UpdateBeaconStats();
}

function EmergencyPingMylonen() {
    if (!g_state.authorized) {
        app.ShowPopup("⛔ AUTHENTICATION REQUIRED");
        return;
    }
    
    var dlg = app.CreateDialog("🚨 EMERGENCY PING — MYLONEN");
    dlg.SetBackColor("#da3633");
    
    var layDlg = app.CreateLayout("Linear", "Vertical");
    layDlg.SetPadding(0.05, 0.05, 0.05, 0.05);
    
    var txt = app.CreateText("Send SOS ping to Mylonen?\n\nThis will:"
        + "\n• Send high-priority beacon request"
        + "\n• Alert all Command channels"
        + "\n• Begin extraction protocols if no response", 
        -1, -1, "Center,Multiline");
    txt.SetTextColor("#ffffff");
    layDlg.AddChild(txt);
    
    var btnSend = app.CreateButton("📢 SEND EMERGENCY PING", -1, 0.1, "Custom");
    btnSend.SetStyle("#ffffff", "#ffffff", 10, "#ffffff", 2, 0);
    btnSend.SetTextColor("#da3633");
    btnSend.SetOnTouch(function() {
        app.ShowPopup("🚨 EMERGENCY PING SENT TO MYLONEN");
        AddEvent("14:" + new Date().getMinutes() + " — EMERGENCY PING to Mylonen");
        dlg.Hide();
    });
    layDlg.AddChild(btnSend);
    
    dlg.AddLayout(layDlg);
    dlg.Show();
}

function ShowMenu() {
    var opts = ["Settings", "Authorized Targets", "MNEMOSYNE Status", "About", "Exit"];
    app.ListDialog("Menu", opts, function(item) {
        if (item === "Exit") app.Exit();
        else if (item === "About") app.ShowPopup("NetProbe v" + APP_VERSION + "\nGMAOC Tactical Command");
    });
}

// Global variables
var layMain, layContent;
var g_tabs = {}, g_tabButtons = {}, g_currentTab = "globe";
var g_txtStatus, g_txtGlobeInfo, g_txtDuration, g_txtBeaconStats;
var g_inpTargetIP;
var g_layActiveProbes, g_layBeaconList, g_layEARSList, g_layEvents;
var g_btnModes = {}, g_selectedMode = "passive";
var g_chkMNEMOSYNE;
var g_probeDuration = 3600;

// Start the app
OnStart();
