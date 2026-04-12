# 📬 LagosCP Postman Collection Suite

A comprehensive API collection for testing the Lagos State Crime Profiling System (LagosCP).

## 📦 What's Included

- **LagosCP_API_Collection.postman_collection.json** - Complete API suite with 15+ automated endpoints
- **LagosCP_Local_Environment.json** - Environment configuration for local development

## 🚀 Quick Start

### 1. Import Files

1. Open Postman.
2. Click **Import** and select `LagosCP_API_Collection.postman_collection.json` and `LagosCP_Local_Environment.json`.
3. Select the **LagosCP (Local)** environment from the dropdown in the top-right corner.

### 2. Login as an Officer

1. Navigate to the **Authentication** folder.
2. Open the **Login (Officer)** request.
3. Click **Send**.
4. The test script will automatically capture the `access_token`, `refresh_token`, and `officer_id` and save them to your environment variables.

### 3. Run the Field Scan (Identification) Flow

1. **Step 1: Identify** → Open `Suspect Identification > Identify (Field Scan)`.
   - Send the request (it uses mock base64 data). If a match is found based on the seeded database data, it will return the subject profile and any active warrants.
2. **Step 2: Log Offence** → Open `Offence Tracking > Log New Offence`.
   - The code (e.g., `LG-ARB-2025-00001`) is generated automatically by the backend based on the incident year.
3. **Step 3: Check Audit Trail** → Open `Audit Logs > View Activity Trail`.
   - Verify that your actions have been recorded in the immutable audit log.

---

## 📋 Collection Modules

### 1. Authentication
- ✅ **Login (Officer)** - Automates token saving.
- ✅ **Refresh/Logout** - JWT lifecycle management.
- ✅ **List/Create Stations** - Admin-only management of police divisions.

### 2. Suspect Identification
- ✅ **Identify (Field Scan)** - Core AI recognition endpoint.
- ✅ **Identification Logs** - History of scan attempts.

### 3. Criminal Profiles (Subjects)
- ✅ **Search Subjects** - Filter by status, risk level, or name/alias.
- ✅ **Create Subject** - Onboard a new suspect record.
- ✅ **Enrol Mugshot** - Link a photo to a suspect for future AI matching.

### 4. Offence Tracking
- ✅ **Log Offence** - Link crimes to subjects with auto-sequencing codes.
- ✅ **Update Status** - Supervisor only: mark cases as Resolved, Dismissed, etc.

### 5. Wanted Persons
- ✅ **Issue Warrant** - Flag a subject as WANTED. Sets subject status to WANTED and potentially marks them as "Armed & Dangerous".

---

## 🔑 Environment Variables (Auto-Managed)

| Variable | Description |
|----------|-------------|
| `access_token` | Current JWT token used in headers. |
| `subject_id` | Set automatically after creating a Subject profile. |
| `offence_id` | Set automatically after logging an Offence. |
| `station_id` | Set automatically after creating a Police Station. |

## 🧪 Seeding Reference

The `create_admin.py` script provides these initial credentials:
- **Badge**: `LSP-04821` / **Password**: `police123` (Field Officer)
- **Badge**: `LSP-00123` / **Password**: `police123` (Supervisor)
- **Badge**: `LSP-ADMIN` / **Password**: `admin123` (Admin)
