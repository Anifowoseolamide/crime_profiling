# 🔍 LagosCP — Lagos State Crime Profiling System

An **AI-powered criminal identification and profiling platform** built for the Lagos State Police Command. Field officers capture a suspect's photograph, run it against a centralised criminal database via facial recognition, instantly surface the full crime history, and log new offences — all with immutable GPS-stamped audit trails.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Background & Motivation](#-background--motivation)
3. [System Architecture](#-system-architecture)
4. [Core Modules](#-core-modules)
5. [Technology Stack](#️-technology-stack)
6. [Data Models](#-data-models)
7. [API Reference](#-api-reference)
8. [Role-Based Access Control](#-role-based-access-control)
9. [AI Face Recognition Layer](#-ai-face-recognition-layer)
10. [Geographic Intelligence](#-geographic-intelligence)
11. [Audit & Immutability](#-audit--immutability)
12. [Frontend Architecture](#-frontend-architecture)
13. [Setup & Quick Start](#-setup--quick-start)
14. [Environment Variables](#-environment-variables)
15. [Test Accounts](#-test-accounts)
16. [Deployment](#-deployment)
17. [Academic Context](#-academic-context)
18. [Repository Layout](#-repository-layout)
19. [Developer Workflow](#-developer-workflow)
20. [Troubleshooting](#-troubleshooting)
21. [Integration Resources](#-integration-resources)


---

## 🎯 Project Overview

LagosCP is a full-stack web application that equips Lagos State Police Command officers with real-time, AI-augmented tools for:

- **Biometric suspect identification** in the field using camera-captured photos
- **Centralised criminal record management** with structured offence classification
- **Geographic crime intelligence** via interactive hotspot maps
- **Immutable audit logging** of every officer action, GPS-tagged and timestamped

The system is accessible via a React web frontend (desktop and mobile) and exposes a fully documented REST API for future integrations.

---

## 📖 Background & Motivation

Traditional police records in Nigeria are paper-based and siloed per station. A field officer encountering a suspect has no reliable, fast mechanism to determine whether the individual is wanted, has prior convictions, or poses an armed threat.

LagosCP addresses this by:

1. Centralising all criminal records in a PostgreSQL database accessible via REST API
2. Using AI facial recognition so officers only need a photograph — no name or ID required
3. Giving command centres a real-time geographic crime view for resource allocation
4. Logging every officer action with GPS metadata to enforce accountability and prevent data tampering

---

## 🏛 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   FRONTEND (React 18 + Vite)                  │
│  Dashboard · FieldScan · SubjectProfile · GeoMap             │
│  AuditLog · WantedList · LogOffence · DeclareWanted          │
└───────────────────────┬──────────────────────────────────────┘
                        │  HTTP REST  (JSON + JWT Bearer)
                        ▼
┌──────────────────────────────────────────────────────────────┐
│                  BACKEND (Django 4.2 + DRF)                   │
│                                                               │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐  │
│  │  auth   │  │ subjects │  │ offences │  │    wanted   │  │
│  └─────────┘  └──────────┘  └──────────┘  └─────────────┘  │
│  ┌──────────────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │  identification  │  │  audit   │  │    services      │   │
│  └──────────────────┘  └──────────┘  └──────────────────┘   │
└───────────────────────┬──────────────────────────────────────┘
                        │
           ┌────────────┼────────────┐
           ▼            ▼            ▼
    ┌───────────┐  ┌──────────┐  ┌──────────────┐
    │PostgreSQL │  │Cloudinary│  │ CompreFace / │
    │ Database  │  │  (media) │  │   Face++     │
    └───────────┘  └──────────┘  └──────────────┘
```

### Field Scan Request Flow

```
Officer captures photo
  → Base64 encode → POST /api/identify/
  → JWT verified
  → Image decoded + uploaded to Cloudinary (evidence record)
  → Face recognition API queried (CompreFace or Face++)
  → face_recognition_id resolved to Subject in PostgreSQL
  → Subject GPS + last_seen updated atomically
  → Active warrants checked
  → Offence summary compiled
  → IdentificationLog + AuditLog written
  → Full profile + alerts returned to frontend
```

---

## 🧩 Core Modules

### Module 1 — Field Identification
Officers capture a suspect photo via webcam or mobile camera. The system:
- Uploads the image to Cloudinary as an immutable evidence record
- Queries the configured face recognition provider
- Resolves the match to a `Subject` record
- Atomically updates `last_known_location`, `last_known_lat/lng`, `last_seen_date`
- Checks for active arrest warrants and returns an immediate alert
- Creates an `IdentificationLog` and an `AuditLog` entry

### Module 2 — Criminal Profile Management
Complete suspect profiles containing:
- Full name, aliases (A.K.A.s), DOB, gender, nationality, state/LGA of origin
- Physical identifiers: scars, tattoos, distinguishing marks
- Dynamic **Risk Level** (`LOW` → `EXTREME`) and **Status** (`ACTIVE`, `WANTED`, `INCARCERATED`, `DECEASED`)
- `is_armed_dangerous` flag — auto-set when a `CRITICAL` priority warrant is issued
- **Mugshot Gallery**: multiple photos enrolled in face recognition, each geo-tagged

### Module 3 — Offence Tracking
Structured crime records with:
- Auto-generated Case IDs: `LG-{CAT}-{YEAR}-{SEQ}` e.g. `LG-ARB-2026-00184`
- 11 offence categories (Theft, Armed Robbery, Fraud, Homicide, Kidnapping, Cybercrime, …)
- 5 severity levels (`MINOR` → `CAPITAL`)
- Full case lifecycle: `OPEN` → `UNDER_INVESTIGATION` → `RESOLVED` / `ACQUITTED`
- GPS-tagged incident location, arresting officer, linked police station
- Evidence image URLs (Cloudinary), court case number, penalty record

### Module 4 — Wanted Persons & Warrants
- Activating a warrant automatically sets `subject.status = 'WANTED'`
- Priority levels: `ROUTINE`, `URGENT`, `CRITICAL (Armed & Dangerous)`
- `CRITICAL` priority automatically sets `is_armed_dangerous = True`
- Field scans that match a wanted subject trigger an immediate on-screen warrant alert

### Module 5 — Geographic Crime Intelligence
- **Crime Hotspot Map**: circle markers sized by incident count, coloured by severity
- **Wanted Persons Layer**: pulsing red markers for subjects with active warrants
- **Subject Location Layer**: amber/blue markers for high-risk and monitored subjects
- Collision-separation algorithm jitters overlapping GPS coordinates (~30 m)
- Live refresh button with auto-fit viewport on first load

### Module 6 — Immutable Audit Trail
Every significant officer action creates an `AuditLog` record that:
- **Cannot be updated or deleted** — enforced at model level with `PermissionError`
- Captures: officer, action code, target model/ID, metadata JSON, IP address, timestamp
- Supports admin map links showing exactly where an officer was during each action

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Framework | Django 4.2 + DRF 3.14 | REST API, ORM, admin panel |
| Database | PostgreSQL 14+ | Primary relational data store |
| Authentication | SimpleJWT 5.3 | Badge-number JWT login + token blacklist |
| Face Recognition (primary) | Face++ API | Cloud biometric matching |
| Face Recognition (alt) | CompreFace | Self-hosted biometrics + mock mode |
| Media Storage | Cloudinary | Mugshots + field scan evidence |
| Frontend | React 18 + Vite | SPA interface |
| Mapping | Leaflet.js + react-leaflet | Interactive crime map |
| Icons | Lucide React | UI iconography |
| API Docs | drf-spectacular (OpenAPI 3) | Auto Swagger / ReDoc |
| Static Files | WhiteNoise | Production static serving |
| Production Server | Gunicorn | WSGI server |
| Deployment | Render.com | Cloud hosting |

---

## 🗄 Data Models

### `PoliceStation`
| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| name | CharField | Station name |
| division | CharField | Division / area command |
| lga | CharField | Local Government Area |
| address | TextField | Physical address |
| commanding_officer | FK → Officer | Optional |

### `Officer` (Custom User Model)
| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| badge_number | CharField (unique) | Login identifier e.g. `LSP-04821` |
| first_name / last_name | CharField | |
| rank | CharField | e.g. Inspector, Sergeant |
| role | CharField | `FIELD_OFFICER`, `SUPERVISOR`, `ANALYST`, `ADMIN` |
| station | FK → PoliceStation | Assigned station |

### `Subject` (Criminal Profile)
| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| first_name / last_name | CharField | |
| aliases | JSONField | List of A.K.A.s |
| date_of_birth | DateField | |
| gender | CharField | MALE / FEMALE / OTHER |
| identifying_marks | TextField | Scars, tattoos |
| last_known_location | CharField | Human-readable location |
| last_known_lat / lng | FloatField | GPS coordinates |
| last_seen_date | DateTimeField | Last scan timestamp |
| risk_level | CharField | LOW / MEDIUM / HIGH / EXTREME |
| status | CharField | ACTIVE / WANTED / INCARCERATED / DECEASED |
| is_armed_dangerous | BooleanField | Auto-set by CRITICAL warrant |
| face_recognition_id | CharField (unique) | CompreFace / Face++ subject ID |

### `Mugshot`
| Field | Type | Notes |
|---|---|---|
| subject | FK → Subject | |
| image_url | URLField | Cloudinary URL |
| is_primary | BooleanField | Only one primary per subject |
| latitude / longitude | FloatField | Where photo was taken |
| captured_by | FK → Officer | |
| enrolled_in_face_recognition | BooleanField | |

### `Offence`
| Field | Type | Notes |
|---|---|---|
| offence_code | CharField (unique) | e.g. `LG-ARB-2026-00184` — auto-generated |
| subject | FK → Subject | |
| offence_category | CharField | THEFT, ARMED_ROBBERY, FRAUD, HOMICIDE, … |
| severity | CharField | MINOR / MODERATE / SERIOUS / VIOLENT / CAPITAL |
| status | CharField | OPEN / UNDER_INVESTIGATION / RESOLVED / ACQUITTED |
| incident_date | DateTimeField | |
| location / latitude / longitude | | GPS of incident |
| arresting_officer | FK → Officer | |
| station | FK → PoliceStation | |
| evidence_images | JSONField | List of Cloudinary URLs |

### `WantedPerson`
| Field | Type | Notes |
|---|---|---|
| subject | FK → Subject | |
| warrant_number | CharField (unique) | |
| issuing_authority | CharField | e.g. Lagos State High Court |
| priority | CharField | ROUTINE / URGENT / CRITICAL |
| is_active | BooleanField | Triggers status sync on subject |

### `IdentificationLog`
| Field | Type | Notes |
|---|---|---|
| officer | FK → Officer | Who ran the scan |
| subject | FK → Subject (nullable) | Null if no match |
| field_image_url | URLField | Cloudinary evidence URL |
| match_found | BooleanField | |
| confidence_score | FloatField | 0.0 – 1.0 |
| latitude / longitude | FloatField | Where scan was performed |
| timestamp | DateTimeField | Auto, indexed |

### `AuditLog` (Immutable)
| Field | Type | Notes |
|---|---|---|
| officer | FK → Officer | |
| action | CharField | e.g. `OFFENCE_CREATED`, `IDENTIFICATION_ATTEMPTED` |
| target_type | CharField | Model name |
| target_id | UUIDField | PK of affected record |
| metadata | JSONField | Contextual data at time of action |
| ip_address | GenericIPAddressField | |
| timestamp | DateTimeField | auto_now_add — never updated |

---

## 🔌 API Reference

**Base URL**
- Development: `http://localhost:8000/api/`
- Production: `https://<app>.onrender.com/api/`

**Interactive Docs**
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

### Authentication Endpoints

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| POST | `/api/auth/login/` | Public | Badge number + password → JWT |
| POST | `/api/auth/refresh/` | Public | Rotate access token |
| POST | `/api/auth/logout/` | Auth | Blacklist refresh token |
| GET/PATCH | `/api/auth/me/` | Auth | Own officer profile |
| POST | `/api/auth/change-password/` | Auth | Update password |
| GET | `/api/auth/officers/` | Supervisor+ | List officers |
| POST | `/api/auth/officers/` | Admin | Create officer |
| GET/PATCH | `/api/auth/officers/{id}/` | Supervisor+ | Officer detail |
| GET | `/api/auth/stations/` | Auth | List police stations |
| POST | `/api/auth/stations/` | Admin | Create station |

### Subject Endpoints

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/subjects/` | Auth | List / search subjects |
| POST | `/api/subjects/` | Supervisor+ | Create criminal profile |
| GET | `/api/subjects/{id}/` | Auth | Full subject profile |
| PATCH | `/api/subjects/{id}/` | Supervisor+ | Update profile |
| POST | `/api/subjects/{id}/enroll/` | Supervisor+ | Enrol mugshot in face recognition |
| GET | `/api/subjects/{id}/timeline/` | Auth | Chronological event feed |
| GET | `/api/subjects/stats/` | Auth | Dashboard KPI statistics |
| GET | `/api/subjects/hotspots/` | Auth | Crime hotspot data for map |

### Offence Endpoints

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/offences/` | Auth | List offences (filterable) |
| POST | `/api/offences/` | Supervisor+ | Log new offence |
| GET | `/api/offences/{id}/` | Auth | Offence detail |
| PATCH | `/api/offences/{id}/` | Supervisor+ | Update status / notes |

### Identification Endpoints

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| POST | `/api/identify/` | Auth | **Field scan** — match photo to subject |
| GET | `/api/identify/logs/` | Auth | Identification history |

### Wanted / Warrant Endpoints

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/wanted/` | Auth | Active warrants list |
| POST | `/api/wanted/` | Supervisor+ | Issue arrest warrant |
| PATCH | `/api/wanted/{id}/` | Supervisor+ | Update / deactivate warrant |

### Audit Endpoint

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/audit/` | Auth | Immutable activity feed |

---

### Sample — Field Scan

```json
// POST /api/identify/
{
  "image": "<base64 JPEG>",
  "location": "Oshodi Junction",
  "latitude": 6.5565,
  "longitude": 3.3501,
  "notes": "Suspect approached officer near bus stop"
}

// 200 — Match found
{
  "match_found": true,
  "confidence": 0.9312,
  "log_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "timestamp": "2026-05-18T10:00:00Z",
  "subject": {
    "id": "...", "first_name": "Emeka", "last_name": "Obi",
    "status": "WANTED", "risk_level": "HIGH",
    "is_armed_dangerous": false,
    "last_known_location": "Oshodi Junction"
  },
  "is_wanted": true,
  "warrant": {
    "warrant_number": "LGW-2026-00043",
    "priority": "URGENT",
    "reason": "Armed robbery on Lagos Island",
    "issuing_authority": "Lagos State High Court",
    "issued_date": "2026-04-01"
  },
  "offence_summary": {
    "total_offences": 4,
    "open_cases": 2,
    "most_recent": "2026-03-15T18:30:00Z"
  }
}
```

---

## 🔐 Role-Based Access Control

| Action | Field Officer | Supervisor | Analyst | Admin |
|---|:---:|:---:|:---:|:---:|
| Login + view profiles | ✅ | ✅ | ✅ | ✅ |
| Run field scan | ✅ | ✅ | ✅ | ✅ |
| View audit log | ✅ | ✅ | ✅ | ✅ |
| Create / edit subject | ❌ | ✅ | ❌ | ✅ |
| Log offence | ❌ | ✅ | ❌ | ✅ |
| Issue / revoke warrant | ❌ | ✅ | ❌ | ✅ |
| Manage officers | ❌ | View only | ❌ | ✅ |
| Manage stations | ❌ | ❌ | ❌ | ✅ |

---

## 🤖 AI Face Recognition Layer

The system supports **two face recognition providers**, switchable via the `FACE_RECOGNITION_PROVIDER` environment variable.

### Face++ (Primary — Cloud)
- Service file: `services/faceplusplus.py`
- No local deployment required
- FaceSet-based enrolment (`FACEPP_OUTER_ID = lagoscp_faceset`)
- Configurable similarity threshold (`FACEPP_THRESHOLD`, default `80`)

### CompreFace (Alternative — Self-Hosted)
- Service file: `services/compreface.py`
- Run locally via Docker or point to a cloud instance
- Three operations: `enrol_subject()`, `identify()`, `delete_subject()`
- **Mock Mode**: if `COMPREFACE_URL` is blank, returns a realistic no-match response — development proceeds without a live recognition server

### Recognition Pipeline
```
1. Image bytes received from frontend (base64 decoded)
2. Image uploaded to Cloudinary for evidence archiving
3. POST to face recognition provider API
4. Provider returns similarity scores per enrolled face
5. Best score compared against configured threshold
6. If score ≥ threshold → match found, subject_id returned
7. subject_id resolved to Subject record in PostgreSQL
8. Subject GPS + last_seen updated atomically via queryset.update()
9. Warrant check + offence summary compiled
10. IdentificationLog + AuditLog created
```

---

## 🗺 Geographic Intelligence

The `CrimeMap` component (`frontend/src/components/map/CrimeMap.jsx`) uses **react-leaflet** with an Esri World Street Map tile layer.

### Data Layers

| Layer | Colour | API Source |
|---|---|---|
| Crime Hotspots | Sized circles (red/amber/blue by severity) | `GET /api/subjects/hotspots/` |
| Wanted Subjects | 🔴 Solid red markers | `GET /api/subjects/?status=WANTED` |
| High-Risk Subjects | 🟠 Amber markers | All subjects, risk HIGH/EXTREME |
| Monitored Subjects | 🔵 Blue markers | All subjects, risk LOW/MEDIUM |

### Technical Notes
- **Collision separation**: subjects at identical GPS coordinates are jittered ±0.0006° (~30 m) so markers remain individually selectable
- **AutoFit**: viewport auto-fits to all visible markers on first data load
- **Live Refresh**: refresh button re-fetches all layers without page reload
- **Interactive Tooltips**: click any marker for subject name, status, and last-seen time

---

## 📋 Audit & Immutability

```python
# AuditLog.save() — enforces append-only at model level
def save(self, *args, **kwargs):
    if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
        raise PermissionError('AuditLog records are immutable and cannot be updated.')
    super().save(*args, **kwargs)
```

A convenience factory is used throughout the codebase:
```python
AuditLog.log(
    officer=request.user,
    action='OFFENCE_CREATED',
    target_type='Offence',
    target_id=offence.pk,
    metadata={'offence_code': offence.offence_code, 'severity': offence.severity},
    ip_address=request.META.get('REMOTE_ADDR'),
)
```

The `AuditLogMixin` (`audit/mixins.py`) provides `write_audit_log()` for class-based views.

Logged action codes include:
`SUBJECT_VIEWED`, `SUBJECT_CREATED`, `SUBJECT_UPDATED`, `OFFENCE_CREATED`, `OFFENCE_UPDATED`, `IDENTIFICATION_ATTEMPTED`, `FAILED_IDENTIFICATION`, `WANTED_ADDED`, `OFFICER_CREATED`, `OFFICER_UPDATED`

---

## 🖥 Frontend Architecture

**Stack**: React 18 + Vite + Tailwind CSS + Lucide React

### Pages

| File | Route | Description |
|---|---|---|
| `Login.jsx` | `/login` | Badge number + password authentication |
| `Dashboard.jsx` | `/` | Stats cards, active alerts, crime map, activity feed |
| `FieldScan.jsx` | `/field-scan` | Live webcam capture + identification result |
| `SubjectSearch.jsx` | `/subjects` | Searchable / filterable subject index |
| `SubjectProfile.jsx` | `/subjects/:id` | Full profile, mugshot gallery, offence timeline |
| `CreateRecord.jsx` | `/subjects/new` | Create new criminal profile |
| `LogOffence.jsx` | `/offences/new` | Log a new offence against a subject |
| `WantedList.jsx` | `/wanted` | Active warrants dashboard |
| `DeclareWanted.jsx` | `/wanted/new` | Issue a new arrest warrant |
| `GeoMap.jsx` | `/map` | Full-screen crime intelligence map |
| `AuditLog.jsx` | `/audit` | Immutable officer activity feed |

### Key Components

| Component | Purpose |
|---|---|
| `CrimeMap.jsx` | Multi-layer Leaflet map with hotspots, wanted, and subject layers |
| `StatsCard.jsx` | KPI metric card used on Dashboard |
| `StatusBadge.jsx` | Coloured status pill (WANTED, ACTIVE, etc.) |
| `AuthContext.jsx` | JWT token storage + officer profile context |

### API Service Layer (`services/api.js`)
All HTTP calls are centralised:
```javascript
api.getWantedList()             // GET /api/wanted/
api.getAuditLog()               // GET /api/audit/
api.getStats()                  // GET /api/subjects/stats/
api.getHotspots()               // GET /api/subjects/hotspots/
api.searchSubjects(q, status)   // GET /api/subjects/?search=...
api.identify(payload)           // POST /api/identify/
```

---

## 🚀 Setup & Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ / npm 9+

### 1. Clone & create virtual environment
```bash
git clone <repo-url>
cd crime_profiling
python -m venv venv
venv\Scripts\activate              # Windows
# source venv/bin/activate          # macOS / Linux
```

### 2. Install backend dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
# Create a .env file in project root and add required values
```

### 4. Create database
```bash
createdb lagoscp_db -U postgres
```

### 5. Run migrations & seed data
```bash
python manage.py migrate
python create_admin.py       # creates admin officer + default police station
```

### 6. Start backend
```bash
python manage.py runserver   # http://localhost:8000
```

### 7. Start frontend
```bash
cd frontend
npm install
npm run dev                  # http://localhost:5173
```

### Access Points
| URL | Description |
|---|---|
| `http://localhost:5173` | React frontend |
| `http://localhost:8000/admin/` | Django admin panel |
| `http://localhost:8000/api/docs/` | Swagger UI |
| `http://localhost:8000/api/redoc/` | ReDoc |

---

## ⚙️ Environment Variables

Create a `.env` file in the project root and populate the values below.

```ini
# Django core
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (local dev)
DB_NAME=lagoscp_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# JWT token lifetimes (minutes)
JWT_ACCESS_TOKEN_LIFETIME=120
JWT_REFRESH_TOKEN_LIFETIME=1440

# Cloudinary (media storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Face recognition provider: 'facepp' or 'compreface'
FACE_RECOGNITION_PROVIDER=facepp

# Face++ credentials
FACEPP_API_KEY=your-facepp-key
FACEPP_API_SECRET=your-facepp-secret
FACEPP_THRESHOLD=80
FACEPP_OUTER_ID=lagoscp_faceset

# CompreFace (leave COMPREFACE_URL blank to enable Mock Mode)
COMPREFACE_URL=
COMPREFACE_API_KEY=
COMPREFACE_THRESHOLD=0.85
COMPREFACE_DET_PROB_THRESHOLD=0.8

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

---

## 👤 Test Accounts

| Role | Badge Number | Password | Capabilities |
|---|---|---|---|
| **Admin** | `LSP-ADMIN` | `admin123` | Full system access |
| **Supervisor** | `LSP-00123` | `police123` | Create records, issue warrants |
| **Field Officer** | `LSP-04821` | `police123` | Field scans, view profiles |

---

## ☁️ Deployment (Render.com)

The project ships with `render.yaml` and `build.sh` for one-click Render deployment.

**Build command:**
```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**Start command:**
```bash
gunicorn campusguard.wsgi:application
```

**Production environment checklist:**
- `DATABASE_URL` — Render PostgreSQL connection string
- `DEBUG=False`
- `SECRET_KEY` — strong random value (50+ chars)
- `ALLOWED_HOSTS` — includes your Render hostname
- All Cloudinary credentials populated
- `FACE_RECOGNITION_PROVIDER` + respective API keys set

---

## 📁 Repository Layout

| Path | Purpose |
|---|---|
| `campusguard/` | Django project config (`settings.py`, root URL routing, WSGI/ASGI) |
| `authentication/` | Custom officer user model, station management, JWT auth endpoints |
| `subjects/` | Criminal profile and mugshot management |
| `offences/` | Case/offence lifecycle and offence analytics |
| `wanted/` | Warrant issuance, updates, and status synchronization |
| `identification/` | Field identification endpoint + identification logs |
| `audit/` | Immutable audit logging models, serializers, and endpoints |
| `services/` | Face recognition provider integrations (`faceplusplus.py`, `compreface.py`) |
| `frontend/` | React + Vite SPA (pages, map UI, API service layer) |
| `create_admin.py` | Seeds default station and test officers |
| `setup.ps1` | Optional PowerShell setup helper for Windows development |
| `render.yaml` / `build.sh` | Render deployment configuration |

---

## 🧪 Developer Workflow

### Daily startup (Windows)
```powershell
venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

In another terminal:
```powershell
cd frontend
npm install
npm run dev
```

### Seed default users and station
```bash
python create_admin.py
```

### Useful backend commands
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
python manage.py test
```

### Useful frontend commands
```bash
cd frontend
npm run dev
npm run build
npm run lint
npm run preview
```

---

## ✅ First 10 Minutes

Use this checklist when onboarding a new machine or contributor.

1. Clone and enter the repo
```bash
git clone <repo-url>
cd crime_profiling
```

2. Create and activate a Python virtual environment
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install backend dependencies and run migrations
```bash
pip install -r requirements.txt
python manage.py migrate
```

4. Create or update your `.env` file with database and API keys

5. Seed default officers and station
```bash
python create_admin.py
```

6. Start the backend API
```bash
python manage.py runserver
```

7. Start the frontend in a second terminal
```bash
cd frontend
npm install
npm run dev
```

8. Verify all key URLs open successfully
- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/api/docs/`
- Admin: `http://localhost:8000/admin/`

9. Login with a seeded test account from the Test Accounts section

10. Run one smoke test: submit a sample identification request from Swagger or Postman

---

## 🛠 Troubleshooting

### `ModuleNotFoundError` or missing packages
- Ensure your virtual environment is active before running Django commands.
- Reinstall dependencies with `pip install -r requirements.txt`.

### `FATAL: password authentication failed for user "postgres"`
- Confirm `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` in `.env`.
- Ensure PostgreSQL is running and user permissions allow database access.

### `Invalid HTTP_HOST header` on mobile/LAN testing
- Add your local machine IP to `ALLOWED_HOSTS`.
- Add matching origins to `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`.

### Face recognition always returns no match
- Confirm `FACE_RECOGNITION_PROVIDER` is set correctly (`facepp` or `compreface`).
- Verify provider credentials and thresholds (`FACEPP_THRESHOLD` or `COMPREFACE_THRESHOLD`).
- If using CompreFace locally, confirm `COMPREFACE_URL` is reachable.

### Static files not loading in production
- Ensure `python manage.py collectstatic --no-input` runs during build.
- Verify WhiteNoise middleware and `STATIC_ROOT` are configured.

---

## 🔗 Integration Resources

- Postman collection: `LagosCP_API_Collection.postman_collection.json`
- Local environment template: `LagosCP_Local_Environment.json`
- Frontend integration notes: `FRONTEND_INTEGRATION_GUIDE.md`
- Deployment summary: `deployment_prep_summary.md`

---

## 🎓 Academic Context

This project was developed as a **Final Year Project** for the B.Sc. Computer Science degree.

### Research Objectives

1. Design and implement a centralised criminal profiling system for the Lagos State Police Command
2. Evaluate the accuracy and feasibility of cloud AI facial recognition in a Nigerian law-enforcement context
3. Demonstrate how structured GPS data capture and map visualisation improve police situational awareness
4. Build a forensically sound, immutable audit trail that enforces officer accountability

### Key Technical Contributions

| Contribution | Description |
|---|---|
| **Dual-provider AI abstraction** | Hot-swappable `CompreFace` / `Face++` via single env var with mock-mode fallback |
| **Atomic GPS update pattern** | `Subject.objects.filter(pk=...).update(...)` prevents race conditions on concurrent field scans |
| **Model-level audit immutability** | `AuditLog.save()` raises `PermissionError` on updates — enforced at ORM layer, not just policy |
| **Marker collision separation** | Jitter algorithm ensures overlapping GPS points remain individually selectable on map |
| **Auto Case ID generation** | Deterministic, sequence-safe format `LG-{CAT}-{YEAR}-{SEQ:05d}` |
| **Warrant-status synchronisation** | `WantedPerson.save()` automatically syncs `subject.status` and `is_armed_dangerous` |

### Suggested Future Work

- **Celery + Redis** — async mugshot enrolment, report generation, scheduled warrant expiry checks


---

*LagosCP — Secure, Transparent, Intelligent Policing.*
*Built with Django · React · PostgreSQL · Face++ · Leaflet*
## 5. Recommended Frontend NPM Packages

- `react-router-dom` v6+
- `react-webcam` (for taking photos in `/field-scan`)
- `lucide-react` (for icons)
- `zustand` (for global logged-in officer state tracking)
- `axios`
- `tailwindcss` (recommended for rapid dark-mode UX composition)
