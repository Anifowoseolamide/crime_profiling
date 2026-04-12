# CampusGuard System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND LAYER                            │
│                         (React Application)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Security   │  │  Lost &      │  │  Emergency   │            │
│  │  Dashboard   │  │  Found UI    │  │  Module UI   │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Camera     │  │    Admin     │  │    Auth      │            │
│  │ Integration  │  │    Panel     │  │    Pages     │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ ↑
                         HTTP REST API
                         (JSON + JWT)
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────────┐
│                          BACKEND LAYER                              │
│                   (Django REST Framework)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                      API Gateway                              │ │
│  │  - Authentication (JWT)                                       │ │
│  │  - Request Validation                                         │ │
│  │  - Response Formatting                                        │ │
│  │  - Error Handling                                             │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  Students    │  │  Offences    │  │  Lost &      │            │
│  │  Module      │  │  Module      │  │  Found       │            │
│  │              │  │              │  │  Module      │            │
│  │ - CRUD Ops   │  │ - Create     │  │ - Report     │            │
│  │ - Bulk       │  │ - Track      │  │ - Match      │            │
│  │   Import     │  │ - History    │  │ - Claim      │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  Emergency   │  │  Auth        │  │  Security    │            │
│  │  Module      │  │  Module      │  │  Logging     │            │
│  │              │  │              │  │              │            │
│  │ - Quick ID   │  │ - Login      │  │ - Audit      │            │
│  │ - Contacts   │  │ - Logout     │  │ - Activity   │            │
│  │ - Medical    │  │ - Roles      │  │ - Reports    │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────────┐
│                          AI LAYER                                   │
│                   (Face Recognition Engine)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              FaceRecognitionService                           │ │
│  │                                                               │ │
│  │  1. Image Decode (Base64 → NumPy Array)                      │ │
│  │  2. Face Detection (OpenCV/MTCNN)                            │ │
│  │  3. Face Alignment & Cropping                                │ │
│  │  4. Embedding Generation (DeepFace + Facenet)                │ │
│  │  5. Similarity Comparison (Euclidean Distance)               │ │
│  │  6. Threshold Matching                                        │ │
│  │  7. Confidence Score Calculation                             │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Technologies:                                                      │
│  - DeepFace (Face Recognition Framework)                           │
│  - TensorFlow (Deep Learning Backend)                              │
│  - OpenCV (Image Processing)                                       │
│  - NumPy (Numerical Computing)                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────────┐  ┌────────────────────────────┐   │
│  │   PostgreSQL Database      │  │   Cloudinary Storage       │   │
│  │                            │  │                            │   │
│  │  Tables:                   │  │  - Student Photos          │   │
│  │  - students                │  │  - ID Card Images          │   │
│  │  - users                   │  │  - Evidence Images         │   │
│  │  - offences                │  │  - Lost Item Photos        │   │
│  │  - lost_found_items        │  │  - Face Crops              │   │
│  │  - emergency_contacts      │  │                            │   │
│  │  - medical_information     │  │  Features:                 │   │
│  │  - face_embeddings         │  │  - CDN Delivery            │   │
│  │  - security_logs           │  │  - Auto Optimization       │   │
│  │  - identification_attempts │  │  - Transformations         │   │
│  │                            │  │  - Secure URLs             │   │
│  └────────────────────────────┘  └────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### 1. Security Gate Identification Flow

```
User Action: Security officer captures student photo at gate
     ↓
Frontend: Camera captures image → Convert to Base64
     ↓
API Call: POST /api/identify/ with {image: "base64..."}
     ↓
Backend: Validate JWT → Decode image → Call AI Service
     ↓
AI Layer: Detect face → Generate embedding → Compare with DB
     ↓
Database: Query face_embeddings → Find best match
     ↓
Backend: Fetch student details → Check offence history
     ↓
Response: {
    match_found: true,
    confidence: 0.95,
    student: {...},
    offences: [...]
}
     ↓
Frontend: Display student info + offence alerts
     ↓
Security Log: Record identification attempt
```

### 2. Lost & Found Matching Flow

```
User Action: Upload found ID card photo
     ↓
Frontend: Select image → Convert to Base64
     ↓
API Call: POST /api/lostfound/identify/ with {image: "base64..."}
     ↓
Backend: Save item → Extract face from ID card
     ↓
AI Layer: Detect face → Generate embedding
     ↓
Database: Compare with all student embeddings
     ↓
AI Layer: Find best match above threshold
     ↓
Backend: Link item to matched student
     ↓
Response: {
    match_found: true,
    student: {...},
    confidence: 0.92
}
     ↓
Frontend: Display matched owner + contact info
```

### 3. Emergency Identification Flow

```
Emergency Situation: Student needs immediate identification
     ↓
Frontend: Quick capture → Send immediately
     ↓
API Call: POST /api/emergency/identify/ (Priority)
     ↓
Backend: Fast-track processing
     ↓
AI Layer: Rapid face matching
     ↓
Database: Fetch student + emergency contacts + medical info
     ↓
Response: {
    student: {...},
    emergency_contacts: [...],
    medical_info: {...}
}
     ↓
Frontend: Display all emergency information
     ↓
Emergency Log: Record incident
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Network Security                                 │
│  - HTTPS/TLS Encryption                                    │
│  - CORS Configuration                                      │
│  - Rate Limiting                                           │
│                                                             │
│  Layer 2: Authentication                                   │
│  - JWT Token-based Auth                                    │
│  - Token Expiration                                        │
│  - Refresh Token Rotation                                  │
│                                                             │
│  Layer 3: Authorization                                    │
│  - Role-Based Access Control (RBAC)                        │
│  - Permission Checks                                       │
│  - Resource-Level Permissions                              │
│                                                             │
│  Layer 4: Data Security                                    │
│  - Password Hashing (PBKDF2)                               │
│  - SQL Injection Prevention                                │
│  - XSS Protection                                          │
│  - CSRF Protection                                         │
│                                                             │
│  Layer 5: Audit & Logging                                  │
│  - Security Logs                                           │
│  - Identification Attempts                                 │
│  - Activity Tracking                                       │
│  - Anomaly Detection                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Module Interactions

```
┌──────────────┐
│  Students    │──────┐
│  Module      │      │
└──────────────┘      │
                      ├──→ ┌──────────────┐
┌──────────────┐      │    │  AI          │
│  Offences    │──────┤    │  Recognition │
│  Module      │      │    │  Service     │
└──────────────┘      │    └──────────────┘
                      │
┌──────────────┐      │
│  Lost &      │──────┤
│  Found       │      │
└──────────────┘      │
                      │
┌──────────────┐      │
│  Emergency   │──────┘
│  Module      │
└──────────────┘

All modules use AI service for face recognition
All modules log to SecurityLog
All modules require authentication
```

## Technology Stack Summary

**Frontend**: React + Vite + Axios + Modern CSS
**Backend**: Django 4.2 + DRF + PostgreSQL
**AI/ML**: DeepFace + TensorFlow + OpenCV
**Storage**: Cloudinary CDN
**Auth**: JWT (Simple JWT)
**Docs**: drf-spectacular (OpenAPI 3.0)

---

**Architecture Version**: 1.0
**Last Updated**: December 7, 2024
