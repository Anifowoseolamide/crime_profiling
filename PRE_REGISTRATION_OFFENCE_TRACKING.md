# Pre-Registration Offence Tracking - Implementation Guide

## Overview

The CampusGuard system now supports **pre-registration offence tracking**, allowing security officers to record offences for students who haven't registered yet. When the student eventually registers, all their pre-existing offences are automatically linked to their account.

## 🎯 Key Feature

**Problem Solved**: Security officers can now record offences immediately using just the student's matric number (from ID card or face recognition), even if the student hasn't created an account yet.

**Solution**: Offences are stored with the matric_number field. When the student registers, the system automatically links all matching offences to their new Student record.

---

## 📊 Database Changes

### Offence Model Updates

| Field | Type | Description |
|-------|------|-------------|
| `student` | ForeignKey (nullable) | Link to Student record (null if student hasn't registered) |
| `matric_number` | CharField (nullable) | Student's matric number for pre-registration offences |

**Constraint**: Either `student` OR `matric_number` must be set (enforced at database level)

**Indexes**: Added index on `(matric_number, status)` for efficient querying

---

## 🔄 How It Works

### Scenario 1: Student Already Registered

```python
# Security officer creates offence for registered student
POST /api/v1/offences/
{
  "student_id": "uuid-of-student",
  "offence_type": "LATE_ENTRY",
  "severity": "MEDIUM",
  "title": "Late entry to campus",
  "description": "Student entered campus after 10 PM",
  "location": "Main Gate",
  "incident_date": "2026-01-05T22:30:00Z"
}
```

**Result**: Offence is immediately linked to the Student record.

---

### Scenario 2: Student NOT Registered Yet

```python
# Security officer creates offence using matric number
POST /api/v1/offences/
{
  "matric_number": "190401001",  # From student ID card
  "offence_type": "LATE_ENTRY",
  "severity": "MEDIUM",
  "title": "Late entry to campus",
  "description": "Student entered campus after 10 PM",
  "location": "Main Gate",
  "incident_date": "2026-01-05T22:30:00Z"
}
```

**Result**: Offence is created with `matric_number` field set, `student` field is null.

---

### Scenario 3: Student Registers Later

```python
# Student registers via email verification
GET /api/v1/auth/student/register/verify/?token=abc123
```

**What Happens Automatically**:
1. System creates User and Student records
2. **Searches for all offences with matching matric_number**
3. **Links those offences to the new Student record**
4. Clears the matric_number field (offence is now linked via student FK)
5. Returns count of linked offences in response

**Response**:
```json
{
  "message": "Email verified successfully!",
  "user_id": "uuid",
  "matric_number": "190401001",
  "next_step": "set_password",
  "linked_offences": 3  // ← Number of pre-existing offences linked
}
```

---

## 💻 API Usage Examples

### Creating Offence with Student ID (Registered Student)

```http
POST /api/v1/offences/
Authorization: Bearer <security_officer_token>
Content-Type: application/json

{
  "student_id": "550e8400-e29b-41d4-a716-446655440000",
  "offence_type": "MISCONDUCT",
  "severity": "HIGH",
  "title": "Fighting on campus",
  "description": "Student involved in physical altercation",
  "location": "Student Center",
  "incident_date": "2026-01-05T14:00:00Z"
}
```

### Creating Offence with Matric Number (Unregistered Student)

```http
POST /api/v1/offences/
Authorization: Bearer <security_officer_token>
Content-Type: application/json

{
  "matric_number": "190401002",
  "offence_type": "DRESS_CODE",
  "severity": "LOW",
  "title": "Dress code violation",
  "description": "Student not wearing proper uniform",
  "location": "Library",
  "incident_date": "2026-01-05T09:00:00Z"
}
```

### Validation Rules

❌ **Error**: Providing neither student_id nor matric_number
```json
{
  "error": "Either student_id or matric_number must be provided"
}
```

❌ **Error**: Providing both student_id and matric_number
```json
{
  "error": "Provide either student_id or matric_number, not both"
}
```

---

## 🔍 Viewing Offences

### List All Offences (Admin/Security)

```http
GET /api/v1/offences/
Authorization: Bearer <token>
```

**Response** includes pre-registration offences:
```json
[
  {
    "id": "uuid",
    "student": {
      "id": "uuid",
      "student_id": "STU190401001",
      "full_name": "John Doe"
    },
    "matric_number": null,
    "student_identifier": "190401001",
    "is_linked_to_student": true,
    "offence_type": "LATE_ENTRY",
    "status": "PENDING",
    ...
  },
  {
    "id": "uuid",
    "student": null,  // ← Not registered yet
    "matric_number": "190401003",
    "student_identifier": "190401003",
    "is_linked_to_student": false,  // ← Pre-registration offence
    "offence_type": "MISCONDUCT",
    "status": "PENDING",
    ...
  }
]
```

### Student Views Own Offences

```http
GET /api/v1/offences/my-offences/
Authorization: Bearer <student_token>
```

**Response** includes offences created before registration:
```json
{
  "total_offences": 3,
  "pending_offences": 2,
  "resolved_offences": 1,
  "offences": [
    {
      "id": "uuid",
      "offence_type": "LATE_ENTRY",
      "incident_date": "2026-01-03T22:30:00Z",  // ← Before registration
      "status": "PENDING"
    },
    {
      "id": "uuid",
      "offence_type": "DRESS_CODE",
      "incident_date": "2026-01-04T09:00:00Z",  // ← Before registration
      "status": "RESOLVED"
    },
    {
      "id": "uuid",
      "offence_type": "MISCONDUCT",
      "incident_date": "2026-01-05T14:00:00Z",  // ← After registration
      "status": "PENDING"
    }
  ]
}
```

---

## 🛠️ Helper Methods

### Programmatically Link Offences

```python
from offences.models import Offence
from students.models import Student

# Get student
student = Student.objects.get(matric_number='190401001')

# Link all offences for this matric number
count = Offence.link_offences_to_student('190401001', student)
print(f"Linked {count} offences")
```

### Check if Offence is Linked

```python
offence = Offence.objects.get(id=offence_id)

if offence.is_linked_to_student:
    print(f"Linked to: {offence.student.full_name}")
else:
    print(f"Pre-registration offence for: {offence.matric_number}")

# Get student identifier (works for both cases)
print(f"Student: {offence.student_identifier}")
```

---

## 🧪 Testing

### Test Pre-Registration Offence Creation

```python
# Create offence before student registers
response = client.post('/api/v1/offences/', {
    'matric_number': '190401999',
    'offence_type': 'LATE_ENTRY',
    'severity': 'MEDIUM',
    'title': 'Late entry',
    'description': 'Test offence',
    'location': 'Main Gate',
    'incident_date': '2026-01-05T22:00:00Z'
}, headers={'Authorization': f'Bearer {security_token}'})

assert response.status_code == 201
offence_id = response.json()['id']

# Verify offence is not linked yet
offence = Offence.objects.get(id=offence_id)
assert offence.student is None
assert offence.matric_number == '190401999'
assert not offence.is_linked_to_student
```

### Test Auto-Linking on Registration

```python
# Student registers
response = client.post('/api/v1/auth/student/register/initiate/', {
    'matric_number': '190401999'
})

# Verify email (simulate)
token = RegistrationToken.objects.get(matric_number='190401999')
response = client.get(f'/api/v1/auth/student/register/verify/?token={token.token}')

# Check response includes linked offences
assert response.json()['linked_offences'] == 1

# Verify offence is now linked
offence.refresh_from_db()
assert offence.student is not None
assert offence.matric_number is None
assert offence.is_linked_to_student
```

---

## 📋 Admin Dashboard Considerations

### Filtering Pre-Registration Offences

```python
# Get all offences for unregistered students
unlinked_offences = Offence.objects.filter(
    student__isnull=True,
    matric_number__isnull=False
)

# Group by matric number
from django.db.models import Count
offence_counts = unlinked_offences.values('matric_number').annotate(
    count=Count('id')
).order_by('-count')

# Example output:
# [
#   {'matric_number': '190401005', 'count': 5},
#   {'matric_number': '190401010', 'count': 3},
#   ...
# ]
```

### Identifying Students with Offences Who Haven't Registered

```python
# Get unique matric numbers with offences but no student account
unregistered_with_offences = Offence.objects.filter(
    student__isnull=True
).values_list('matric_number', flat=True).distinct()

# Send reminder emails to register
for matric in unregistered_with_offences:
    # Look up email from LASU API
    # Send registration reminder
    pass
```

---

## 🔒 Security Considerations

1. **Validation**: Database constraint ensures either student OR matric_number is set
2. **Atomic Linking**: Offence linking happens in the same transaction as student creation
3. **Audit Trail**: All offence creation is logged with `reported_by` field
4. **No Orphans**: Offences always have an identifier (student or matric_number)

---

## 🚀 Benefits

✅ **Immediate Recording**: Security can record offences instantly without waiting for student registration  
✅ **No Data Loss**: All offences are preserved and automatically linked when student registers  
✅ **Seamless Experience**: Students see complete offence history from day one  
✅ **Better Enforcement**: Offences can be tracked even for students who delay registration  
✅ **Audit Trail**: Complete record of when offences were created vs when student registered  

---

## 📝 Migration

Run the migration to apply database changes:

```bash
python manage.py migrate offences
```

**Migration includes**:
- Add `matric_number` field to Offence model
- Make `student` field nullable
- Add database constraint
- Create index on `(matric_number, status)`

---

## ✅ Summary

The pre-registration offence tracking system is now fully implemented and ready to use. Security officers can record offences using either:

1. **student_id** for registered students
2. **matric_number** for unregistered students

The system automatically links offences when students register, providing a seamless experience for both security staff and students.
