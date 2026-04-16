# 🎓 LagosCP — Project Summary

LagosCP is a state-of-the-art **AI-Powered Criminal Identification and Profiling Platform** designed for the Lagos State Police Command. It enables field officers and command centers to identify suspects, track criminal movements through geographic intelligence, and maintain an irrefutable audit trail of police activity.

---

## 🏛️ System Architecture

The platform follows a modern, distributed architecture:

### 1. Backend Core (Django)
*   **Modular API**: Organized into `subjects`, `offences`, `identification`, and `audit` apps.
*   **Secure Auth**: Custom user model tracking Police Station assignments with JWT-based security.
*   **Audit Engine**: A dedicated system that captures every mutation in the database, including the officer's IP and GPS location.

### 2. Frontend Interface (React)
*   **Command Center Dashboard**: Real-time stats and recent sightings.
*   **Field Scan Engine**: Direct camera integration for live biometric identification.
*   **Geo-Intelligence Hub**: Interactive map visualizing crime hotspots and suspect movements using Leaflet.

### 3. Intelligence Layer (AI & GPS)
*   **Biometrics**: Powered by **CompreFace**, providing high-accuracy facial matching with offline fallback support.
*   **Geo-Tracking**: Automatic GPS coordinate capture during every scan, sighting, and report submission.

---

## 📋 Core Capabilities

### ✅ **Module 1: Field Identification**
Officers can capture a photo in the field. The AI instantly identifies the subject, surfaces their full A.K.A. list, and flags active warrants. Every identify request is tied to a GPS coordinate.

### ✅ **Module 2: Crime Profiling**
A unified subject profile that merges personal data (marks, aliases, addresses) with a comprehensive offence history. Automated Case IDs ensure standardized record-keeping across all Lagos divisions.

### ✅ **Module 3: Geographic Intelligence**
Command centers can visualize crime across the state using "Hotspot Heatmaps." These heatmaps are dynamically generated based on incident severity and location coordinates recorded by field officers.

### ✅ **Module 4: Bulletproof Auditing**
Designed for accountability. Every action—from viewing a profile to logging an offence—is captured in an immutable log. Administrators can click on any log entry to see exactly where an officer was when they performed a task.

---

## 🛠️ Technology Stack
*   **Frameworks**: Django Rest Framework (DRF), React 18, Vite.
*   **Mapping**: Leaflet.js with OpenStreetMap.
*   **Databases**: PostgreSQL (Core), Redis (Caching/Speed).
*   **Tools**: Cloudinary (Image Hosting), CompreFace (Biometrics), Lucide Icons.

---

## 🚀 Key Achievements
*   ✅ **Geolocation Mastery**: Full end-to-end GPS capture from browser to backend to admin map links.
*   ✅ **Real-time Map Visuals**: Interactive markers with tooltips and live data refresh.
*   ✅ **Unified Subject Timeline**: A chronological feed of all interactions with a specific individual.
*   ✅ **Mock-Mode Flexibility**: Intelligent fallback for facial recognition when the CompreFace server is unavailable.

---
*LagosCP: Secure, Transparent, Intelligent Policing.*
