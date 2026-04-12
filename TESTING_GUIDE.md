# 🧪 CampusGuard API Testing Guide

## Quick Start Testing

### Prerequisites
- Backend server running (`python manage.py runserver`)
- Postman or similar API testing tool
- Sample images for testing face recognition

---

## 1. Setup & Authentication

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@campusguard.com
# Password: (your secure password)
```

### Login to Get JWT Token
```http
POST http://localhost:8000/api/v1/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid",
    "username": "admin",
    "role": "ADMIN"
  }
}
```

**Save the `access` token** - you'll need it for all subsequent requests!

---

## 2. Create Test Student

### Add Student via Admin Panel
1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Click "Students" → "Add Student"
4. Fill in required fields:
   - Student ID: `STU001`
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john.doe@test.com`
   - Phone: `+1234567890`
   - Department: `Computer Science`
   - Program: `Bachelor's`
   - Year of Study: `2`
   - Date of Birth: `2000-01-01`
   - Enrollment Date: `2020-09-01`
   - Expected Graduation: `2024-06-01`
   - Gender: `M`
   - Blood Group: `O+`
   - Address fields
5. Add Emergency Contact (inline)
6. Add Medical Information (inline)
7. Save

### OR Create via API
```http
POST http://localhost:8000/api/v1/students/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "student_id": "STU001",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2000-01-01",
  "gender": "M",
  "blood_group": "O+",
  "phone_number": "+1234567890",
  "email": "john.doe@test.com",
  "address_line1": "123 Main St",
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "postal_code": "10001",
  "department": "Computer Science",
  "program": "Bachelor's",
  "year_of_study": 2,
  "enrollment_date": "2020-09-01",
  "expected_graduation": "2024-06-01",
  "emergency_contacts": [
    {
      "name": "Jane Doe",
      "relationship": "PARENT",
      "phone_number": "+1234567891",
      "email": "jane@test.com",
      "is_primary": true
    }
  ],
  "medical_info": {
    "allergies": "Penicillin",
    "medications": "None",
    "medical_conditions": "Asthma",
    "blood_group": "O+"
  }
}
```

---

## 3. Enroll Student Face

### Convert Image to Base64
**Python:**
```python
import base64

with open('student_photo.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()
    print(image_data)
```

**JavaScript:**
```javascript
const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];
const reader = new FileReader();

reader.onloadend = () => {
  const base64 = reader.result.split(',')[1];
  console.log(base64);
};

reader.readAsDataURL(file);
```

### Enroll Face via API
```http
POST http://localhost:8000/api/v1/students/{student_id}/enroll-face/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "image": "BASE64_ENCODED_IMAGE_STRING"
}

Response:
{
  "id": "uuid",
  "student_id": "STU001",
  "embedding_id": "uuid",
  "image_url": "cloudinary_url",
  "model_name": "Facenet",
  "message": "Face enrolled successfully"
}
```

---

## 4. Test Student Identification (Module A)

### Identify Student from Image
```http
POST http://localhost:8000/api/v1/students/identify/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "image": "BASE64_ENCODED_IMAGE_STRING"
}

Success Response:
{
  "match_found": true,
  "confidence": 0.95,
  "processing_time": 1.23,
  "student": {
    "id": "uuid",
    "student_id": "STU001",
    "full_name": "John Doe",
    "department": "Computer Science",
    "profile_image": "url",
    "offence_count": 0,
    "has_pending_offences": false
  },
  "recent_offences": []
}

No Match Response:
{
  "match_found": false,
  "message": "No matching student found",
  "processing_time": 1.15
}
```

---

## 5. Test Offence Management

### Create Offence
```http
POST http://localhost:8000/api/v1/offences/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "student_id": "STUDENT_UUID",
  "offence_type": "LATE_ENTRY",
  "severity": "MEDIUM",
  "title": "Late entry to campus",
  "description": "Student arrived at 9:30 PM",
  "location": "Main Gate",
  "incident_date": "2024-12-07T21:30:00Z",
  "notes": "First offense this semester"
}
```

### Get Student Offence History
```http
GET http://localhost:8000/api/v1/offences/student/{student_id}/
Authorization: Bearer YOUR_ACCESS_TOKEN

Response:
{
  "student": {...},
  "total_offences": 1,
  "pending_offences": 1,
  "resolved_offences": 0,
  "dismissed_offences": 0,
  "offences": [...]
}
```

---

## 6. Test Lost & Found (Module B)

### Report Found Item
```http
POST http://localhost:8000/api/v1/lostfound/items/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "report_type": "FOUND",
  "item_type": "ID_CARD",
  "item_name": "Student ID Card",
  "description": "Found near library entrance",
  "found_location": "Library Entrance",
  "found_date": "2024-12-07T14:00:00Z",
  "images": [],
  "contact_name": "Security Officer",
  "contact_phone": "+1234567890"
}
```

### Identify Owner from ID Card Photo
```http
POST http://localhost:8000/api/v1/lostfound/identify-owner/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "item_id": "ITEM_UUID",
  "image": "BASE64_ENCODED_ID_CARD_IMAGE"
}

Response:
{
  "match_found": true,
  "confidence": 0.92,
  "processing_time": 1.45,
  "student": {
    "id": "uuid",
    "student_id": "STU001",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "email": "john.doe@test.com"
  },
  "item": {...}
}
```

### Claim Item
```http
POST http://localhost:8000/api/v1/lostfound/items/{item_id}/claim/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "claimed_by_student_id": "STUDENT_UUID",
  "notes": "ID verified, item returned to student"
}
```

---

## 7. Test Emergency Identification (Module C)

### Emergency Scan
```http
POST http://localhost:8000/api/v1/emergency/identify/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "image": "BASE64_ENCODED_IMAGE",
  "location": "Sports Complex",
  "emergency_type": "Medical Emergency",
  "description": "Student collapsed during practice"
}

Response:
{
  "identification_successful": true,
  "confidence": 0.96,
  "processing_time": 0.89,
  "student": {
    "id": "uuid",
    "student_id": "STU001",
    "full_name": "John Doe",
    "blood_group": "O+"
  },
  "emergency_contacts": [
    {
      "name": "Jane Doe",
      "relationship": "PARENT",
      "phone_number": "+1234567891",
      "is_primary": true
    }
  ],
  "medical_info": {
    "allergies": "Penicillin",
    "medications": "None",
    "medical_conditions": "Asthma"
  },
  "emergency_log_id": "uuid"
}
```

---

## 8. Test Security Logs

### View Security Logs
```http
GET http://localhost:8000/api/v1/offences/security/logs/
Authorization: Bearer YOUR_ACCESS_TOKEN

Query Parameters:
- action_type: IDENTIFICATION, EMERGENCY_SCAN, etc.
- success: true/false
- date_from: 2024-12-01
- date_to: 2024-12-31
```

---

## 9. Test API Documentation

### Access Swagger UI
```
http://localhost:8000/api/docs/
```

### Access ReDoc
```
http://localhost:8000/api/redoc/
```

### Download OpenAPI Schema
```
http://localhost:8000/api/schema/
```

---

## 🧪 Testing Checklist

### Authentication ✅
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (should fail)
- [ ] Refresh JWT token
- [ ] Logout and blacklist token
- [ ] Access protected endpoint without token (should fail)
- [ ] Access protected endpoint with valid token

### Students ✅
- [ ] Create student (Admin only)
- [ ] List all students
- [ ] Get student details
- [ ] Update student (Admin only)
- [ ] Delete student (Admin only)
- [ ] Search students by name/ID
- [ ] Filter students by department

### Face Recognition ✅
- [ ] Enroll student face
- [ ] Identify student from good quality image
- [ ] Try identification with no face in image
- [ ] Try identification with unknown person
- [ ] Check confidence scores
- [ ] Verify processing times

### Offences ✅
- [ ] Create offence (Security/Admin)
- [ ] List all offences
- [ ] Get offence details
- [ ] Update offence status
- [ ] Get student offence history
- [ ] Filter offences by status/severity

### Lost & Found ✅
- [ ] Report found item
- [ ] Report lost item
- [ ] Identify owner from ID card photo
- [ ] Claim item
- [ ] List all items
- [ ] Filter items by type/status

### Emergency ✅
- [ ] Perform emergency identification
- [ ] Verify emergency contacts retrieved
- [ ] Verify medical info retrieved
- [ ] View emergency logs (Admin)

### Security Logs ✅
- [ ] View all security logs
- [ ] Filter logs by action type
- [ ] Filter logs by success status
- [ ] Filter logs by date range

---

## 📊 Performance Testing

### Expected Response Times
- Authentication: < 200ms
- Student CRUD: < 100ms
- Face Enrollment: 2-3 seconds
- Face Identification: 1-2 seconds
- Emergency Identification: < 1 second (priority)

### Load Testing
Test with multiple concurrent requests:
```bash
# Using Apache Bench
ab -n 100 -c 10 -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/students/
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "No face detected"
**Solution**: Ensure image contains a clear, front-facing face

### Issue 2: "No matching student found"
**Solution**: Make sure student face is enrolled first

### Issue 3: "Authentication required"
**Solution**: Include `Authorization: Bearer TOKEN` header

### Issue 4: "Permission denied"
**Solution**: Check user role (some endpoints are Admin/Security only)

### Issue 5: Low confidence scores
**Solution**: Use high-quality, well-lit images for enrollment and identification

---

## 📝 Sample Test Data

### Test Students
```json
[
  {
    "student_id": "STU001",
    "name": "John Doe",
    "department": "Computer Science"
  },
  {
    "student_id": "STU002",
    "name": "Jane Smith",
    "department": "Engineering"
  },
  {
    "student_id": "STU003",
    "name": "Bob Johnson",
    "department": "Business"
  }
]
```

### Test Offences
```json
[
  {
    "type": "LATE_ENTRY",
    "severity": "LOW"
  },
  {
    "type": "UNAUTHORIZED_ACCESS",
    "severity": "HIGH"
  },
  {
    "type": "MISCONDUCT",
    "severity": "MEDIUM"
  }
]
```

---

## 🎯 Testing Workflow

1. **Setup**
   - Start server
   - Create superuser
   - Login and get token

2. **Create Test Data**
   - Add 3-5 test students
   - Enroll faces for each student

3. **Test Core Features**
   - Test identification with enrolled faces
   - Create offences
   - Report lost items
   - Perform emergency scans

4. **Test Edge Cases**
   - Unknown faces
   - No face in image
   - Invalid tokens
   - Permission restrictions

5. **Verify Logs**
   - Check security logs
   - Verify identification attempts
   - Review emergency logs

---

**Happy Testing!** 🧪✅

For issues or questions, check the API documentation at `/api/docs/`
