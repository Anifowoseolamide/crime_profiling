# 🔌 CampusGuard API Specification v2.0

**Complete API Documentation for Frontend Integration**

## 📋 Table of Contents
1. [Base Configuration](#base-configuration)
2. [Authentication & User Management](#authentication--user-management)
3. [Student Self-Registration (NEW)](#student-self-registration-new)
4. [Student Management](#student-management)
5. [Offence Management (UPDATED)](#offence-management-updated)
6. [Face Recognition & Identification](#face-recognition--identification)
7. [Lost & Found Module](#lost--found-module)
8. [Emergency Module](#emergency-module)
9. [Security Logs](#security-logs)
10. [Permission Matrix](#permission-matrix)
11. [Error Responses](#error-responses)

---

## Base Configuration

### Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.campusguard.lasu.edu.ng/api/v1
```

### Authentication
All authenticated endpoints require JWT token:
```http
Authorization: Bearer <access_token>
```

### Pagination
List endpoints support pagination:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

---

## Authentication & User Management

### POST `/auth/login/`
**Description**: User login  
**Permission**: Public  
**Request**:
```json
{
  "username": "string",
  "password": "string"
}
```
**Success Response** (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@campusguard.com",
    "role": "ADMIN",
    "first_name": "Admin",
    "last_name": "User",
    "email_verified": true,
    "is_active": true,
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```
**Error Response** (400):
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```
**Error Response** (403 - Student not verified):
```json
{
  "error": "Please verify your email address first. Check your inbox for the verification link."
}
```

### POST `/auth/logout/`
**Description**: User logout (blacklist refresh token)  
**Permission**: Authenticated  
**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response** (200):
```json
{
  "message": "Successfully logged out"
}
```

### POST `/auth/refresh/`
**Description**: Refresh access token  
**Permission**: Public  
**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response** (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### GET `/auth/profile/`
**Description**: Get current user profile  
**Permission**: Authenticated  
**Response** (200):
```json
{
  "id": "uuid",
  "username": "admin",
  "email": "admin@campusguard.com",
  "role": "ADMIN",
  "first_name": "Admin",
  "last_name": "User",
  "phone_number": "+2348012345678",
  "email_verified": true,
  "student_profile": null
}
```

### POST `/auth/change-password/`
**Description**: Change user password  
**Permission**: Authenticated  
**Request**:
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123",
  "new_password_confirm": "newpass123"
}
```

### GET `/auth/users/`
**Description**: List all users  
**Permission**: Admin only  

### POST `/auth/register/`
**Description**: Register new user (Admin/Security only)  
**Permission**: Admin only  
**Request**:
```json
{
  "username": "security1",
  "email": "security1@campusguard.com",
  "password": "secure123",
  "password_confirm": "secure123",
  "first_name": "Security",
  "last_name": "Officer",
  "role": "SECURITY",
  "phone_number": "+2348012345678"
}
```

---

## Student Self-Registration (NEW)

### Phase 1: Initiate Registration

#### POST `/auth/student/register/initiate/`
**Description**: Student initiates self-registration with matric number  
**Permission**: Public (no authentication)  
**Request**:
```json
{
  "matric_number": "190401001"
}
```
**Success Response** (200):
```json
{
  "message": "Verification email sent to john.doe@student.lasu.edu.ng",
  "email_hint": "jo***@student.lasu.edu.ng",
  "expires_in_minutes": 15
}
```
**Error Responses**:
```json
// Invalid matric number format
{
  "matric_number": ["Invalid matric number format. Please enter a valid LASU matric number."]
}

// Already registered
{
  "matric_number": ["This matric number is already registered. Please login instead."]
}

// Student not found in LASU database
{
  "error": "Matric number not found in LASU database. Please check and try again."
}

// LASU API unavailable
{
  "error": "Unable to verify student at this time. Please try again later or contact support.",
  "details": "Verification service temporarily unavailable"
}
```

### Phase 2: Verify Email

#### GET `/auth/student/register/verify/?token=<token>`
**Description**: Verify email using token from verification email  
**Permission**: Public (no authentication)  
**Query Parameters**:
- `token` (required): Verification token from email

**Success Response** (200):
```json
{
  "message": "Email verified successfully! Please set your password to complete registration.",
  "user_id": "uuid",
  "matric_number": "190401001",
  "next_step": "set_password",
  "linked_offences": 3
}
```
**Note**: `linked_offences` indicates number of pre-existing offences linked to the student

**Error Responses**:
```json
// Missing token
{
  "error": "Token is required"
}

// Invalid token
{
  "error": "Invalid token"
}

// Expired token
{
  "error": "Token has expired"
}

// Already used
{
  "error": "Token has already been used"
}
```

### Phase 3: Set Password

#### POST `/auth/student/set-password/`
**Description**: Set password after email verification  
**Permission**: Public (no authentication)  
**Request**:
```json
{
  "token": "verification-token-from-email",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```
**Success Response** (200):
```json
{
  "message": "Password set successfully! You can now login.",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "username": "190401001",
    "email": "john.doe@student.lasu.edu.ng",
    "role": "STUDENT",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```
**Note**: User is automatically logged in after setting password

**Error Responses**:
```json
// Passwords don't match
{
  "password_confirm": ["Passwords do not match"]
}

// Invalid/expired token
{
  "error": "Invalid or expired token"
}

// User not found
{
  "error": "User account not found. Please complete email verification first."
}
```

### Phase 4: Complete Profile

#### PATCH `/students/me/complete-profile/`
**Description**: Complete student profile with optional details  
**Permission**: Authenticated Student only  
**Request**:
```json
{
  "phone_number": "+2348012345678",
  "date_of_birth": "2002-05-15",
  "gender": "M",
  "address_line1": "123 Main Street",
  "address_line2": "Apt 4B",
  "city": "Lagos",
  "state": "Lagos",
  "country": "Nigeria",
  "postal_code": "100001",
  "program": "Bachelor's",
  "year_of_study": 3,
  "enrollment_date": "2020-09-01",
  "expected_graduation": "2024-06-01"
}
```
**Success Response** (200):
```json
{
  "message": "Profile updated successfully",
  "student": {
    "id": "uuid",
    "student_id": "STU190401001",
    "matric_number": "190401001",
    "full_name": "John Doe",
    "email": "john.doe@student.lasu.edu.ng",
    "phone_number": "+2348012345678",
    "department": "Computer Science",
    "registration_status": "APPROVED"
  }
}
```

### Admin Fallback

#### GET `/auth/pending-verifications/`
**Description**: List students pending manual verification  
**Permission**: Admin only  
**Response** (200):
```json
[
  {
    "id": "uuid",
    "username": "190401002",
    "email": "jane.doe@student.lasu.edu.ng",
    "role": "STUDENT",
    "email_verified": false,
    "verification_source": "FALLBACK",
    "created_at": "2026-01-05T10:30:00Z"
  }
]
```

---

## Student Management

### GET `/students/`
**Description**: List all students (paginated)  
**Permission**: Admin, Security  
**Query Parameters**:
- `page`: Page number
- `page_size`: Items per page
- `search`: Search by name, student_id, matric_number, email
- `department`: Filter by department
- `is_active`: Filter by active status
- `registration_status`: Filter by registration status (PENDING_VERIFICATION, VERIFIED, APPROVED, REJECTED)

**Response** (200):
```json
{
  "count": 100,
  "next": "http://api.../students/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "student_id": "STU190401001",
      "matric_number": "190401001",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "email": "john.doe@student.lasu.edu.ng",
      "phone_number": "+2348012345678",
      "department": "Computer Science",
      "program": "Bachelor's",
      "year_of_study": 2,
      "registration_status": "APPROVED",
      "profile_image": "https://cloudinary.../image.jpg",
      "is_active": true,
      "offence_count": 2,
      "created_at": "2026-01-01T10:00:00Z"
    }
  ]
}
```

### POST `/students/`
**Description**: Create new student (Admin only)  
**Permission**: Admin  
**Request**:
```json
{
  "student_id": "STU2026001",
  "matric_number": "202601001",
  "first_name": "Jane",
  "last_name": "Smith",
  "middle_name": "Marie",
  "email": "jane.smith@student.lasu.edu.ng",
  "phone_number": "+2348098765432",
  "date_of_birth": "2003-08-20",
  "gender": "F",
  "department": "Engineering",
  "program": "Bachelor's",
  "year_of_study": 1,
  "enrollment_date": "2026-09-01",
  "expected_graduation": "2030-06-01"
}
```

### GET `/students/{id}/`
**Description**: Get student details  
**Permission**: Admin, Security  
**Response** (200):
```json
{
  "id": "uuid",
  "student_id": "STU190401001",
  "matric_number": "190401001",
  "full_name": "John Doe",
  "first_name": "John",
  "last_name": "Doe",
  "middle_name": "Michael",
  "email": "john.doe@student.lasu.edu.ng",
  "phone_number": "+2348012345678",
  "date_of_birth": "2002-05-15",
  "gender": "M",
  "department": "Computer Science",
  "program": "Bachelor's",
  "year_of_study": 2,
  "registration_status": "APPROVED",
  "profile_image": "https://cloudinary.../image.jpg",
  "address_line1": "123 Main Street",
  "city": "Lagos",
  "state": "Lagos",
  "country": "Nigeria",
  "emergency_contacts": [...],
  "medical_info": {...},
  "face_embeddings": [...],
  "offence_count": 2,
  "has_pending_offences": true,
  "is_active": true,
  "created_at": "2026-01-01T10:00:00Z"
}
```

### GET `/students/me/`
**Description**: Get own student profile  
**Permission**: Authenticated Student only  
**Response** (200): Same as GET `/students/{id}/`

### PUT/PATCH `/students/{id}/`
**Description**: Update student  
**Permission**: Admin  

### DELETE `/students/{id}/`
**Description**: Soft delete student  
**Permission**: Admin  

---

## Offence Management (UPDATED)

### GET `/offences/`
**Description**: List all offences (paginated)  
**Permission**: Admin, Security  
**Query Parameters**:
- `student_id`: Filter by student UUID
- `matric_number`: Filter by matric number (NEW)
- `status`: Filter by status (PENDING, UNDER_REVIEW, RESOLVED, DISMISSED)
- `severity`: Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)
- `date_from`, `date_to`: Date range filter

**Response** (200):
```json
{
  "count": 50,
  "results": [
    {
      "id": "uuid",
      "student": {
        "id": "uuid",
        "student_id": "STU190401001",
        "matric_number": "190401001",
        "full_name": "John Doe"
      },
      "matric_number": null,
      "student_identifier": "190401001",
      "is_linked_to_student": true,
      "reported_by": {
        "id": "uuid",
        "username": "security1",
        "full_name": "Security Officer"
      },
      "offence_type": "LATE_ENTRY",
      "offence_type_display": "Late Entry",
      "severity": "MEDIUM",
      "severity_display": "Medium",
      "status": "PENDING",
      "status_display": "Pending",
      "title": "Late entry to campus",
      "description": "Student entered campus after 10 PM",
      "location": "Main Gate",
      "incident_date": "2026-01-05T22:30:00Z",
      "reported_date": "2026-01-05T22:35:00Z",
      "evidence_images": ["https://cloudinary.../image1.jpg"],
      "created_at": "2026-01-05T22:35:00Z"
    },
    {
      "id": "uuid",
      "student": null,
      "matric_number": "190401999",
      "student_identifier": "190401999",
      "is_linked_to_student": false,
      "offence_type": "MISCONDUCT",
      "severity": "HIGH",
      "status": "PENDING",
      "title": "Fighting on campus",
      "description": "Student involved in physical altercation",
      "location": "Student Center",
      "incident_date": "2026-01-04T14:00:00Z",
      "reported_date": "2026-01-04T14:10:00Z"
    }
  ]
}
```
**Note**: Pre-registration offences have `student: null` and `matric_number` set

### POST `/offences/`
**Description**: Create new offence  
**Permission**: Security, Admin  
**Request (Registered Student)**:
```json
{
  "student_id": "uuid",
  "offence_type": "LATE_ENTRY",
  "severity": "MEDIUM",
  "title": "Late entry to campus",
  "description": "Student entered campus after 10 PM",
  "location": "Main Gate",
  "incident_date": "2026-01-05T22:30:00Z",
  "evidence_images": ["base64_image1", "base64_image2"],
  "notes": "First offense this semester"
}
```
**Request (Pre-Registration - NEW)**:
```json
{
  "matric_number": "190401999",
  "offence_type": "MISCONDUCT",
  "severity": "HIGH",
  "title": "Fighting on campus",
  "description": "Student involved in physical altercation",
  "location": "Student Center",
  "incident_date": "2026-01-05T14:00:00Z",
  "evidence_images": [],
  "notes": "Student not yet registered in system"
}
```
**Note**: Provide either `student_id` OR `matric_number`, not both

**Success Response** (201):
```json
{
  "id": "uuid",
  "student": {...} or null,
  "matric_number": "190401999" or null,
  "student_identifier": "190401999",
  "is_linked_to_student": false,
  "offence_type": "MISCONDUCT",
  "severity": "HIGH",
  "status": "PENDING",
  "title": "Fighting on campus",
  "incident_date": "2026-01-05T14:00:00Z",
  "reported_by": {...},
  "created_at": "2026-01-05T14:05:00Z"
}
```

**Error Responses**:
```json
// Neither student_id nor matric_number provided
{
  "non_field_errors": ["Either student_id or matric_number must be provided"]
}

// Both provided
{
  "non_field_errors": ["Provide either student_id or matric_number, not both"]
}

// Student not found
{
  "student_id": ["Student not found"]
}
```

### GET `/offences/{id}/`
**Description**: Get offence details  
**Permission**: Admin, Security  

### PATCH `/offences/{id}/`
**Description**: Update offence (change status, add action taken)  
**Permission**: Admin, Security  
**Request**:
```json
{
  "status": "RESOLVED",
  "action_taken": "Student counseled and warned",
  "penalty": "Written warning",
  "resolved_date": "2026-01-06T10:00:00Z",
  "notes": "Student showed remorse"
}
```

### GET `/offences/my-offences/`
**Description**: Get own offences (Student only)  
**Permission**: Authenticated Student  
**Response** (200):
```json
{
  "total_offences": 3,
  "pending_offences": 2,
  "resolved_offences": 1,
  "dismissed_offences": 0,
  "offences": [
    {
      "id": "uuid",
      "offence_type": "LATE_ENTRY",
      "offence_type_display": "Late Entry",
      "severity": "MEDIUM",
      "status": "PENDING",
      "title": "Late entry to campus",
      "description": "Student entered campus after 10 PM",
      "location": "Main Gate",
      "incident_date": "2026-01-03T22:30:00Z",
      "reported_date": "2026-01-03T22:35:00Z"
    }
  ]
}
```

### GET `/offences/student/{student_id}/history/`
**Description**: Get student's offence history  
**Permission**: Admin, Security  

---

## Face Recognition & Identification

### POST `/students/identify/`
**Description**: Identify student from image using AI  
**Permission**: Security, Admin  
**Request**:
```json
{
  "image": "base64_encoded_image_string"
}
```
**Success Response** (200):
```json
{
  "match_found": true,
  "confidence": 0.95,
  "processing_time": 1.23,
  "student": {
    "id": "uuid",
    "student_id": "STU190401001",
    "matric_number": "190401001",
    "full_name": "John Doe",
    "department": "Computer Science",
    "profile_image": "https://cloudinary.../image.jpg",
    "blood_group": "O+",
    "offence_count": 2,
    "has_pending_offences": true
  },
  "recent_offences": [
    {
      "id": "uuid",
      "offence_type": "LATE_ENTRY",
      "severity": "MEDIUM",
      "status": "PENDING",
      "incident_date": "2026-01-01T20:30:00Z"
    }
  ]
}
```
**No Match Response** (200):
```json
{
  "match_found": false,
  "message": "No matching student found",
  "processing_time": 1.15
}
```

### POST `/students/{id}/enroll-face/`
**Description**: Enroll student face for recognition  
**Permission**: Admin, Security  
**Request**:
```json
{
  "image": "base64_encoded_image_string"
}
```

---

## Lost & Found Module

### GET `/lostfound/items/`
**Description**: List all lost/found items  
**Permission**: Authenticated  
**Query Parameters**:
- `report_type`: LOST or FOUND
- `status`: REPORTED, MATCHED, CLAIMED
- `item_type`: Filter by item type

### POST `/lostfound/items/`
**Description**: Report lost or found item  
**Permission**: Authenticated  

### POST `/lostfound/identify-owner/`
**Description**: Identify item owner using AI  
**Permission**: Security, Admin  

---

## Emergency Module

### POST `/emergency/identify/`
**Description**: Emergency student identification  
**Permission**: Security, Admin  
**Request**:
```json
{
  "image": "base64_encoded_image",
  "location": "Sports Complex",
  "emergency_type": "Medical Emergency",
  "description": "Student collapsed during practice"
}
```
**Response** (200):
```json
{
  "identification_successful": true,
  "confidence": 0.96,
  "student": {
    "id": "uuid",
    "student_id": "STU190401001",
    "full_name": "John Doe",
    "blood_group": "O+"
  },
  "emergency_contacts": [...],
  "medical_info": {...}
}
```

---

## Security Logs

### GET `/security/logs/`
**Description**: Get security activity logs  
**Permission**: Admin, Security  
**Query Parameters**:
- `action_type`: Filter by action type
- `user_id`: Filter by user
- `student_id`: Filter by student
- `date_from`, `date_to`: Date range
- `success`: Filter by success status

---

## Permission Matrix

| Endpoint | Admin | Security | Student | Public |
|----------|-------|----------|---------|--------|
| **Authentication** |
| Login | ✅ | ✅ | ✅ | ✅ |
| Logout | ✅ | ✅ | ✅ | - |
| Refresh Token | ✅ | ✅ | ✅ | ✅ |
| Register User | ✅ | ❌ | ❌ | ❌ |
| **Student Self-Registration** |
| Initiate Registration | - | - | - | ✅ |
| Verify Email | - | - | - | ✅ |
| Set Password | - | - | - | ✅ |
| Complete Profile | ❌ | ❌ | ✅ | ❌ |
| Pending Verifications | ✅ | ❌ | ❌ | ❌ |
| **Student Management** |
| List Students | ✅ | ✅ | ❌ | ❌ |
| Create Student | ✅ | ❌ | ❌ | ❌ |
| View Student Details | ✅ | ✅ | ❌ | ❌ |
| View Own Profile | ❌ | ❌ | ✅ | ❌ |
| Update Student | ✅ | ❌ | ❌ | ❌ |
| **Offence Management** |
| List Offences | ✅ | ✅ | ❌ | ❌ |
| Create Offence (student_id) | ✅ | ✅ | ❌ | ❌ |
| Create Offence (matric_number) | ✅ | ✅ | ❌ | ❌ |
| View Own Offences | ❌ | ❌ | ✅ | ❌ |
| Update Offence | ✅ | ✅ | ❌ | ❌ |
| **Face Recognition** |
| Identify Student | ✅ | ✅ | ❌ | ❌ |
| Enroll Face | ✅ | ✅ | ❌ | ❌ |
| **Lost & Found** |
| Report Item | ✅ | ✅ | ✅ | ❌ |
| Identify Owner | ✅ | ✅ | ❌ | ❌ |
| **Emergency** |
| Emergency Identify | ✅ | ✅ | ❌ | ❌ |

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "Only administrators can create users"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error",
  "message": "An unexpected error occurred"
}
```

### 503 Service Unavailable
```json
{
  "error": "Unable to verify student at this time. Please try again later or contact support.",
  "details": "Verification service temporarily unavailable"
}
```

---

## Important Notes for Frontend

### Student Self-Registration Flow
1. Student enters matric number → `POST /auth/student/register/initiate/`
2. Student receives email with verification link
3. Student clicks link → `GET /auth/student/register/verify/?token=<token>`
4. Student sets password → `POST /auth/student/set-password/`
5. Student is auto-logged in with JWT tokens
6. Student can complete profile → `PATCH /students/me/complete-profile/`

### Pre-Registration Offences
- Security can create offences using `matric_number` before student registers
- When student registers, offences are automatically linked
- Frontend should display `student_identifier` field (works for both cases)
- Check `is_linked_to_student` to show registration status

### Token Management
- Access tokens expire after 60 minutes (default)
- Refresh tokens expire after 24 hours (default)
- Use `/auth/refresh/` to get new access token
- Store tokens securely (httpOnly cookies recommended)

### Image Upload
- Images should be base64 encoded
- Maximum image size: 5MB
- Supported formats: JPG, PNG, WEBP
- For face recognition, ensure face is clearly visible

---

**API Version**: 2.0  
**Last Updated**: January 5, 2026  
**Postman Collection**: `CampusGuard_API_Collection.postman_collection.json`
