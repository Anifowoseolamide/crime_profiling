# CampusGuard Setup Guide

## 🔧 Configuration Summary

### ✅ Frontend API Configuration
The frontend is **fully configured** with all necessary API endpoints in `frontend/src/api/axios.js`:

- ✅ **Authentication**: Login, Logout, Registration, Password management
- ✅ **Student API**: CRUD operations, profile management, face enrollment  
- ✅ **Offence API**: List, create, update, student history
- ✅ **Lost & Found API**: Item management, owner identification
- ✅ **Emergency API**: Emergency identification

**Current API Base URL**: `http://localhost:8000/api/v1` (hardcoded)

---

## 🔐 Login Credentials

### Security Personnel / Admin Users

There are **no default credentials**. You must create users first:

**Option 1: Create Superuser (Recommended)**
```bash
cd d:/updated/CampusGuard
python manage.py createsuperuser
```

Then enter:
- Username: `admin` (or your choice)
- Email: `admin@campusguard.com`
- Password: Create a secure password
- Confirm password

**Option 2: Create via Django Admin**
1. Login to Django admin at `http://localhost:8000/admin`
2. Navigate to Users
3. Create new users with role `SECURITY` or `ADMIN`

### Student Login

Students use **self-registration workflow**:
1. Navigate to `/register` on frontend
2. Enter matric number
3. System verifies via LASU API
4. Verification email sent
5. Click email link to verify
6. Set password
7. Login with matric number and password

---

## 📋 Environment Variables Required

### Backend (.env in project root)

Create `d:/updated/CampusGuard/.env` with:

```env
# ===================================
# Django Core Settings
# ===================================
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ===================================
# Database Configuration
# ===================================
DB_NAME=campusguard_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# ===================================
# Cloudinary (Image Storage)
# ===================================
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# ===================================
# JWT Authentication
# ===================================
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# ===================================
# Face Recognition AI
# ===================================
FACE_RECOGNITION_THRESHOLD=0.6
MAX_FACE_DISTANCE=0.6

# ===================================
# CORS & Frontend
# ===================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
FRONTEND_URL=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:5173

# ===================================
# LASU API (Student Verification)
# ===================================
LASU_API_URL=https://api.lasu.edu.ng/verify
LASU_API_KEY=your_lasu_api_key
LASU_API_TIMEOUT=10

# ===================================
# Email Configuration
# ===================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=noreply@campusguard.lasu.edu.ng
```

### Frontend (.env in frontend directory)

**⚠️ CURRENTLY MISSING** - Create `d:/updated/CampusGuard/frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 🚀 Quick Start

### 1. Setup Backend

```bash
# Navigate to project directory
cd d:/updated/CampusGuard

# Copy and configure .env
copy .env.example .env
# Edit .env with your actual values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin

---

## 🐛 Fixed Issues

### TensorFlow Recursion Error ✅

**Problem**: Running `python manage.py createsuperuser` caused:
```
RecursionError: maximum recursion depth exceeded while calling a Python object
```

**Root Cause**: DeepFace was imported at module level in `ai_recognition/services.py`, causing TensorFlow to initialize during Django startup.

**Solution**: Implemented lazy loading for DeepFace:
- Removed module-level import
- Added `@property` decorator for lazy loading
- DeepFace now only loads when face recognition methods are actually called
- Django commands now work without TensorFlow recursion errors

---

## 📦 Required External Services

### 1. PostgreSQL Database
- Install PostgreSQL
- Create database: `campusguard_db`
- Update DB credentials in `.env`

### 2. Cloudinary Account
- Sign up at https://cloudinary.com
- Get Cloud Name, API Key, API Secret
- Add to `.env` file

### 3. Email Service (Gmail)
- Enable 2-Factor Authentication on Gmail
- Generate App Password
- Use App Password in `.env` (not your regular password)

### 4. LASU API Access
- Contact LASU IT department for API credentials
- Get API URL and API Key
- Add to `.env` file

---

## 🔑 API Endpoints Overview

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/refresh/` - Refresh JWT token
- `GET /api/v1/auth/profile/` - Get user profile
- `POST /api/v1/auth/change-password/` - Change password

### Student Self-Registration
- `POST /api/v1/auth/student/register/initiate/` - Initiate registration
- `GET /api/v1/auth/student/register/verify/?token=xxx` - Verify email
- `POST /api/v1/auth/student/set-password/` - Set password

### Students
- `GET /api/v1/students/` - List students
- `GET /api/v1/students/me/` - Get my student profile
- `POST /api/v1/students/` - Create student (admin only)
- `PATCH /api/v1/students/{id}/` - Update student

### Offences
- `GET /api/v1/offences/` - List offences
- `GET /api/v1/offences/my-offences/` - Get my offences
- `POST /api/v1/offences/` - Create offence
- `GET /api/v1/offences/student/{id}/history/` - Get student offence history

---

## 🎯 Next Steps

1. ✅ **Fixed TensorFlow recursion error** - Django commands now work
2. ⚠️ **Create frontend .env file** for API base URL configuration
3. ⚠️ **Configure external services** (PostgreSQL, Cloudinary, Email, LASU API)
4. ✅ **Create superuser** for first login
5. 🚀 **Start both servers** and test the application

---

## 📞 Support

For issues or questions:
- Check Django logs: Terminal where `manage.py runserver` is running
- Check Frontend console: Browser Developer Tools (F12)
- Review `.env` configuration for missing or incorrect values
