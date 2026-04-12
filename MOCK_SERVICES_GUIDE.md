# Mock Services Configuration Guide

## Overview

This guide explains how to set up and use the mock LASU API and SMTP servers for testing the student self-registration workflow.

## Mock Services

### 1. Mock LASU API Server

**File**: `mock_lasu_api.py`

**Purpose**: Simulates the LASU student verification API

**Features**:
- Verifies student matric numbers
- Returns student data (name, email, department, status)
- Auto-generates data for test matric numbers (1904xxxxx, 2026xxxxx)
- Includes pre-configured mock students

**Running**:
```bash
python mock_lasu_api.py
```

**Endpoint**: `http://localhost:5000/verify-student?matric=<matric_number>`

**Mock Students**:
- `190401001`: John Doe (john.doe@student.lasu.edu.ng)
- `190401002`: Jane Smith (jane.smith@student.lasu.edu.ng)
- `190401003`: Bob Johnson (bob.johnson@student.lasu.edu.ng)
- `190401999`: Test Student (test.student@student.lasu.edu.ng)
- Any matric starting with `1904` or `2026` auto-generates

---

### 2. Mock SMTP Server

**File**: `mock_smtp_server.py`

**Purpose**: Captures verification emails instead of sending them

**Features**:
- Captures all outgoing emails
- Displays email content in console
- Extracts verification links and tokens
- No actual email sending required

**Requirements**:
```bash
pip install aiosmtpd
```

**Running**:
```bash
python mock_smtp_server.py
```

**Server**: `localhost:1025`

---

## Configuration

### Update Django Settings

Add to your `.env` file or `settings.py`:

```env
# Mock LASU API
LASU_API_URL=http://localhost:5000
LASU_API_KEY=mock_api_key_for_testing

# Mock SMTP Server
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@campusguard.lasu.edu.ng

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

---

## Testing Workflow

### Step 1: Start Mock Services

**Terminal 1** - Start Mock LASU API:
```bash
python mock_lasu_api.py
```

**Terminal 2** - Start Mock SMTP Server:
```bash
python mock_smtp_server.py
```

**Terminal 3** - Start Django Server:
```bash
python manage.py runserver
```

### Step 2: Test Student Registration

**Terminal 4** - Run Tests:
```bash
python test_api_endpoints.py
```

Or use Postman:

1. **Initiate Registration**:
   ```
   POST http://localhost:8000/api/v1/auth/student/register/initiate/
   {
     "matric_number": "190401001"
   }
   ```

2. **Check Mock SMTP Console** for verification email and token

3. **Verify Email**:
   ```
   GET http://localhost:8000/api/v1/auth/student/register/verify/?token=<token_from_email>
   ```

4. **Set Password**:
   ```
   POST http://localhost:8000/api/v1/auth/student/set-password/
   {
     "token": "<token_from_email>",
     "password": "student123",
     "password_confirm": "student123"
   }
   ```

---

## Example Output

### Mock LASU API
```
============================================================
  Mock LASU API Server
  Running on http://localhost:5000
============================================================

Endpoints:
  GET /verify-student?matric=<matric_number>
  GET /health

Authentication:
  Header: Authorization: Bearer <any_token>

Mock Students:
  190401001: John Doe (john.doe@student.lasu.edu.ng)
  190401002: Jane Smith (jane.smith@student.lasu.edu.ng)
  ...
============================================================

INFO:werkzeug:127.0.0.1 - - [05/Jan/2026 14:45:00] "GET /verify-student?matric=190401001 HTTP/1.1" 200 -
```

### Mock SMTP Server
```
============================================================
  📧 Email Captured - 14:45:05
============================================================
From: noreply@campusguard.lasu.edu.ng
To: john.doe@student.lasu.edu.ng
Subject: Verify Your LASU CampusGuard Account

🔗 Verification Link Found:
   http://localhost:3000/verify?token=abc123def456

🎫 Token: abc123def456

📝 Total Emails Captured: 1
============================================================
```

---

## Troubleshooting

### Mock LASU API Not Responding
- Check if port 5000 is available
- Verify LASU_API_URL in settings points to `http://localhost:5000`
- Check firewall settings

### Mock SMTP Not Capturing Emails
- Verify EMAIL_HOST='localhost' and EMAIL_PORT=1025
- Ensure EMAIL_USE_TLS=False
- Check if port 1025 is available

### Verification Token Not Found
- Check mock SMTP console output
- Token is in the verification link: `?token=<token>`
- Copy token from console and use in verify endpoint

---

## Production vs Testing

| Setting | Production | Testing (Mock) |
|---------|-----------|----------------|
| LASU_API_URL | https://api.lasu.edu.ng | http://localhost:5000 |
| EMAIL_HOST | smtp.gmail.com | localhost |
| EMAIL_PORT | 587 | 1025 |
| EMAIL_USE_TLS | True | False |

**Important**: Never use mock services in production!

---

## Benefits of Mock Services

✅ **No External Dependencies**: Test without real LASU API or email server  
✅ **Faster Testing**: Instant responses, no network delays  
✅ **Offline Testing**: Work without internet connection  
✅ **Debugging**: See exact email content and verification tokens  
✅ **Repeatable**: Same test data every time  
✅ **Safe**: No risk of sending real emails or hitting API rate limits  

---

## Next Steps

1. Start both mock services
2. Update `.env` with mock configurations
3. Run `python test_api_endpoints.py`
4. Watch the complete registration flow work end-to-end!
