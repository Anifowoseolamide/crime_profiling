# Frontend Integration Guide — LagosCP

This document outlines how the React/Vite frontend should integrate with the LagosCP Django REST API. 

**UI Aesthetic Goal**: A premium, dark law-enforcement theme (deep navy/charcoal, high-contrast text, smooth animations, glassmorphism UI element components). Needs to be heavily mobile-responsive for field officers, while offering expansive multi-column views for analysts and supervisors on desktops.

---

## 1. Authentication Check

- **Login endpoint**: `POST /api/auth/login/`
- **Body**: `{ "badge_number": "LSP-XXXX", "password": "..." }`
- **Feature**: The backend automatically embeds the full `officer` profile inside the JWT payload and as a JSON dictionary in the auth response. Because of this, the frontend **does not** need to hit `/api/auth/me/` on initialization if the token is valid.

```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "officer": {
    "id": "uuid",
    "badge_number": "LSP-04821",
    "full_name": "Adeyemi Bola",
    "rank": "Sergeant",
    "role": "FIELD_OFFICER",
    "station": "Ikeja Division Headquarters"
  }
}
```

## 2. Core Frontend Pages Required

### Login (`/login`)
- **Action**: Accepts `badge_number` and `password`.
- **UI**: Dark thematic login page. Store tokens in local storage or secure cookie contexts.

### Dashboard (`/dashboard`)
- **UI**: Quick access tiles linking to Field Scan, Wanted List, Recent Subjects.
- **Data Needed**: Pull counts/last modified from endpoints `GET /api/subjects/`, `GET /api/offences/` using length metrics (if requested). Keep it highly visual.

### Field Scan (Camera) (`/field-scan`)
- **Crucial Note**: Must be "mobile-first". Default out to `react-webcam` requesting `facingMode: "environment"` (rear camera) for immediate use by field officers on tablets/phones. 
- **Endpoint**: `POST /api/identify/`
  - Accepts standard JSON payload with a `base64` image representing the photo captured.
  - Automatically handles uploading evidence images internally.
  - Example payload:
    ```json
    {
      "image": "base64_encoded_jpeg_string...",
      "location": "Oshodi Overbridge",
      "latitude": 6.5512,
      "longitude": 3.3384
    }
    ```
- **Response rendering**: The API returns a highly parsed response `match_found: true` accompanied by the `subject` summary, `is_wanted` flag + warrant data, and an `offence_summary` (e.g., `open_cases: 2`). The UI should flash red / trigger an alert modal if `is_wanted` is true.

### Subjects List & Profiles (`/subjects` and `/subjects/:id`)
- **List Endpoint**: `GET /api/subjects/` (supports `?search=` and filter query params).
- **Detail Endpoint**: `GET /api/subjects/:id/` 
- **Action Modules**: Provide a nested UI for:
  - Subject's Offence History (`GET /api/offences/?subject_id=...`)
  - Enrolling new Mugshots (`POST /api/subjects/:id/enrol-mugshot/` - base64 upload).

### Log Offence (`/offences/new`)
- Provide a clean form categorising the offence (`THEFT`, `ASSAULT`, etc).
- Offence codes (e.g. `LG-ARB-2025-00184`) are generated dynamically by the backend; don't post them in the payload. Note that `incident_date` is a required field.
- Takes base64 arrays in the `evidence_images` parameter.

### Wanted List (`/wanted`)
- Table/Grid fetching `GET /api/wanted/?is_active=true`.
- Highlight warrants listed as `priority: "CRITICAL"`.

### Audit Log (`/audit`) - Supervisor/Admin Only
- Endpoint `GET /api/audit/`.
- Display the immutable timeline of events.

---

## 3. Roles and Authorisation Flags

Frontend components (like "Edit Case Status" buttons or "Issue Warrant" buttons) should be heavily protected client-side utilizing the embedded `token.officer.role` data:
- `FIELD_OFFICER`: Can read profiles, scan suspects, log new offences, view warrants. Cannot edit case statuses, emit new warrants, or read audit logs.
- `SUPERVISOR`: Can edit offence status/penalties, issue warrants, and read audit logs.
- `ADMIN`: Full CRUD management, including access to manage other Officers.

## 4. API Error Handling

- The API uses typical DRF format for 400 Bad Requests: `{ "field_name": ["error message..."] }`. 
- 401 Unauthorized denotes expired tokens; standard axios response interceptors should catch this and attempt `POST /api/auth/refresh/`.

## 5. Recommended Frontend NPM Packages

- `react-router-dom` v6+
- `react-webcam` (for taking photos in `/field-scan`)
- `lucide-react` (for icons)
- `zustand` (for global logged-in officer state tracking)
- `axios`
- `tailwindcss` (recommended for rapid dark-mode UX composition)

## 5. Recommended Frontend NPM Packages

- `react-router-dom` v6+
- `react-webcam` (for taking photos in `/field-scan`)
- `lucide-react` (for icons)
- `zustand` (for global logged-in officer state tracking)
- `axios`
- `tailwindcss` (recommended for rapid dark-mode UX composition)
