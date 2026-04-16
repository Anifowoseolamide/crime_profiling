# 🔍 LagosCP — Lagos State Crime Profiling System

An AI-powered criminal identification and profiling platform built for the Lagos State Police Command. Officers in the field can capture a suspect's photograph, run it against a centralised criminal database using facial recognition, instantly pull up the suspect's full crime history, and log new offences — all with full timestamping and immutable audit trails.

## 🌟 Core Modules

### 1. Suspect Identification (Field Scan)
- Field officers capture a photo via mobile or desktop webcam.
- The image is sent to **CompreFace** facial recognition for matching.
- **Geographic Tracking**: Every scan automatically updates the subject's `last_known_location` and real-time GPS coordinates.
- Instantly surfaces the full criminal record and highlights active warrants if found.

### 2. Crime Record & Offence Tracking
- Full offence history with classification (Theft, Armed Robbery, Kidnapping, etc.) and severity levels.
- Auto-generated Case IDs (e.g. `LG-ARB-2026-00184`).
- **Subject Timeline**: A unified, chronological feed merging offences, sightings, and warrants.
- **Mugshot Gallery**: Chronological archive of all suspect photos, each stamped with capture date and a clickable GPS location map link.

### 3. Geographic Crime Intelligence
- **Crime Hotspots**: Aggregated map visualization showing incident density and severity.
- **Real-time Map**: Track sightings of Wanted Persons with **Live Refresh** and **Interactive Tooltips**.
- **Admin Audit Maps**: Administrators can view officer activity locations directly via clickable Google Maps links in the audit logs.

### 4. Criminal Profile Management
- Comprehensive records (A.K.A.s, identifiable marks, known addresses).
- Multiple mugshots per subject for robust CompreFace AI enrolment.
- Dynamic Risk Levels (`LOW` to `EXTREME`) and Status (`CLEARED`, `WANTED`, `WATCHLIST`).

### 5. Access Control & Audit Log
- **Role-Based Access**: 
    - `Field Officer`: Localized scanning and profiling.
    - `Supervisor`: Status management, case resolution, and record creation.
    - `Admin`: Full command access, officer management, and global audit oversight.
- **Immutable Audit Feed**: Every action is irrefutably logged with timestamp, officer ID, and GPS metadata.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 4.2+ with Django REST Framework |
| **Database** | PostgreSQL 14+ |
| **Authentication** | JWT via Simple JWT (Badge Number login) |
| **Face Recognition**| CompreFace REST API (with offline Dev-Mock support) |
| **Media Storage** | Cloudinary |
| **Frontend** | React 18+ with Vite (Tailwind CSS + Leaflet Maps) |

---

## 🚀 Quick Start (Development)

### 1. Database Setup
Ensure PostgreSQL is running and create the database:
```bash
createdb lagoscp_db -U postgres
```

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations & seed stations
python manage.py migrate
python create_admin.py

# Start Django (Port 8000)
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
# Ensure .env has VITE_API_BASE_URL=http://localhost:8000/api

# Start Dev Server (Port 5173)
npm run dev
```

### 4. Test Accounts
| Role | Badge Number | Password |
|---|---|---|
| Admin / Superuser | `LSP-ADMIN` | `admin123` |
| Supervisor | `LSP-00123` | `police123` |
| Field Officer | `LSP-04821` | `police123` |

---

## 🤖 CompreFace Configuration
To use real Face Recognition instead of the mock simulator, you must run the CompreFace Docker stack locally or point the `.env` configuration to an active CompreFace Cloud deployment.

If `COMPREFACE_URL` is left blank in your `.env`, the system defaults to **Mock Mode**, simulating a "No Match" result so frontend development and general testing can proceed seamlessly.
