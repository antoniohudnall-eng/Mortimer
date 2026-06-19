# CREAM PIM - Time & Chaos Clone

A superior standalone version of CREAM (Comprehensive Real Estate Agent Management) reimagined as a Time & Chaos PIM (Personal Information Manager) clone.

## Overview

CREAM PIM is a powerful, cross-platform personal information manager with features inspired by the classic Time & Chaos software.

## Features

### 📇 Contacts
- Add, edit, delete contacts with multiple fields
- Custom labels for emails, phones, addresses
- Contact history tracking
- Linked items (appointments/tasks/projects)
- Categories and groups
- Duplicate detection and merging
- Find/Replace functionality

### 📅 Calendar
- Day, Week, Month views
- Weekly planner
- Appointments with custom colors
- Recurring events support
- Reminders
- Link to contacts

### ✅ Tasks
- Due dates and priorities (High/Medium/Low with colors)
- Recurring tasks
- Mark complete
- Link to contacts/appointments/projects
- Filter by status/priority

### 📊 Projects
- Create projects to group tasks/appointments
- Progress tracking
- Color coding
- Status management (Active/Completed/On Hold/Cancelled)

### 💾 Data Management
- Import/Export CSV and JSON
- Backup and restore
- Archive old data
- Quick search across all data types

## Project Structure

```
cream-standalone/
├── shared/                 # Shared core logic (TypeScript)
│   └── src/
│       ├── types.ts       # Data models
│       └── store.ts       # Data store with persistence
├── desktop/               # Desktop app (Tauri + React)
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Contacts.tsx
│   │   │   ├── Calendar.tsx
│   │   │   ├── Tasks.tsx
│   │   │   ├── Projects.tsx
│   │   │   └── Settings.tsx
│   │   └── components/
│   │       └── SearchModal.tsx
│   └── src-tauri/         # Tauri configuration
├── mobile/                # Mobile app (React Native)
│   └── src/
│       └── screens/
│           ├── ContactsScreen.tsx
│           ├── CalendarScreen.tsx
│           ├── TasksScreen.tsx
│           ├── ProjectsScreen.tsx
│           └── SettingsScreen.tsx
├── build-desktop.sh       # Desktop build script
├── build-mobile.sh        # Mobile build script
└── DarkFactoryJob.json    # Dark Factory job definition
```

## Build Instructions

### Desktop (.exe for Windows)

```bash
cd cream-standalone
chmod +x build-desktop.sh
./build-desktop.sh
```

Requirements:
- Node.js 18+
- Rust/Cargo
- Tauri CLI

### Mobile (.apk for Android)

```bash
cd cream-standalone
chmod +x build-mobile.sh
./build-mobile.sh
```

Requirements:
- Node.js 18+
- JDK 17+
- Android SDK

## Dark Factory Integration

This project is configured for automated building via the Dark Factory system.

Job ID: `CREAM-Standalone-Build`

## License

Performance Supply Depot LLC - All Rights Reserved
