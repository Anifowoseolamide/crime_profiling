# 🚀 CampusGuard - Quick Start Guide

## Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.11 or higher installed
- [ ] PostgreSQL 12+ installed and running
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Cloudinary account (free tier: https://cloudinary.com/users/register/free)

---

## 🏁 Setup Instructions (Windows)

### 1. Create Virtual Environment

```powershell
# Navigate to project directory
cd d:\updated\CampusGuard

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your terminal
```

### 2. Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt

# This will install:
# - Django & DRF
# - PostgreSQL driver
# - DeepFace & AI libraries
# - Cloudinary
# - JWT authentication
# - And more...
```

**Note**: Installing TensorFlow and DeepFace may take 5-10 minutes.

### 3. Configure Environment Variables

```powershell
# Copy example environment file
copy .env.example .env

# Edit .env file with your settings
notepad .env
```

**Required Configuration**:

```env
# Django
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_NAME=campusguard_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary (Get from https://cloudinary.com/console)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# JWT Settings (in minutes)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# AI Settings
FACE_RECOGNITION_THRESHOLD=0.6
MAX_FACE_DISTANCE=0.6

# CORS (Frontend URLs)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Set Up PostgreSQL Database

**Option A: Using psql command line**
```powershell
# Open PostgreSQL command line
psql -U postgres

# Create database
CREATE DATABASE campusguard_db;

# Exit psql
\q
```

**Option B: Using pgAdmin**
1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `campusguard_db`
5. Click "Save"

### 5. Run Database Migrations

```powershell
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# You should see:
# - Running migrations for students
# - Running migrations for authentication
# - Running migrations for offences
# - Running migrations for lostfound
# - Running migrations for emergency
# - Running migrations for ai_recognition
```

### 6. Create Superuser (Admin Account)

```powershell
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@campusguard.com
# Password: (enter secure password)
# Password (again): (confirm password)
```

### 7. Run Development Server

```powershell
python manage.py runserver

# Server should start at: http://127.0.0.1:8000/
```

### 8. Access Admin Panel

1. Open browser: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. You should see all models:
   - Students
   - Users
   - Offences
   - Lost Found Items
   - Emergency Contacts
   - Face Embeddings
   - Security Logs

---

## 🧪 Testing the Setup

### Test 1: Admin Panel Access

```
URL: http://localhost:8000/admin/
Expected: Login page → Dashboard with all models
```

### Test 2: Create Test Student

1. Go to Admin → Students → Add Student
2. Fill in required fields:
   - Student ID: `STU001`
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john.doe@example.com`
   - Phone: `+1234567890`
   - Department: `Computer Science`
   - Program: `Bachelor's`
   - Year of Study: `2`
   - Date of Birth: `2000-01-01`
   - Enrollment Date: `2020-09-01`
   - Expected Graduation: `2024-06-01`
3. Save

### Test 3: Add Emergency Contact

1. Go to Admin → Emergency Contacts → Add
2. Select the student you created
3. Fill in contact details
4. Save

---

## 📚 Next Steps After Setup

### Option 1: Build API Endpoints (Recommended)

Create views and URLs to expose the API:
- Student CRUD operations
- Authentication endpoints
- Identification endpoint
- Offence management
- Lost & found
- Emergency module

### Option 2: Test AI Face Recognition

Create a simple test script to verify DeepFace is working:

```python
# test_ai.py
from ai_recognition.services import face_recognition_service
import base64

# Test face detection
with open('test_image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()
    
image_array = face_recognition_service.decode_image(image_data)
has_face = face_recognition_service.detect_face(image_array)
print(f"Face detected: {has_face}")

# Test embedding generation
if has_face:
    embedding = face_recognition_service.generate_embedding(image_array)
    print(f"Embedding generated: {embedding is not None}")
    print(f"Embedding dimensions: {len(embedding) if embedding else 0}")
```

### Option 3: Build Frontend

Initialize React project and start building the UI.

---

## 🐛 Common Issues & Solutions

### Issue 1: PostgreSQL Connection Error

**Error**: `django.db.utils.OperationalError: could not connect to server`

**Solution**:
1. Make sure PostgreSQL is running
2. Check credentials in `.env`
3. Verify database exists: `psql -U postgres -l`

### Issue 2: TensorFlow Installation Error

**Error**: `Could not find a version that satisfies the requirement tensorflow`

**Solution**:
```powershell
# Install specific version
pip install tensorflow==2.15.0

# Or use CPU-only version
pip install tensorflow-cpu==2.15.0
```

### Issue 3: DeepFace Model Download

**Note**: First time using DeepFace, it will download models (~100MB).

**Location**: Models are cached in `~/.deepface/weights/`

### Issue 4: Cloudinary Not Working

**Solution**:
1. Sign up at https://cloudinary.com
2. Get credentials from Dashboard
3. Update `.env` file
4. Restart server

### Issue 5: Migration Errors

**Error**: `No changes detected`

**Solution**:
```powershell
# Delete migration files (except __init__.py)
# Then run:
python manage.py makemigrations students
python manage.py makemigrations authentication
python manage.py makemigrations offences
python manage.py makemigrations lostfound
python manage.py makemigrations emergency
python manage.py makemigrations ai_recognition
python manage.py migrate
```

---

## 📊 Verify Installation

Run this checklist:

```powershell
# Check Python version
python --version
# Should be 3.11+

# Check Django installation
python -m django --version
# Should be 4.2+

# Check database connection
python manage.py dbshell
# Should connect to PostgreSQL

# Check migrations
python manage.py showmigrations
# Should show all apps with migrations

# Check admin
python manage.py createsuperuser
# Should create user successfully
```

---

## 🎯 Development Workflow

```
1. Activate virtual environment
   → .\venv\Scripts\activate

2. Make code changes
   → Edit files in your IDE

3. Create/update migrations (if models changed)
   → python manage.py makemigrations
   → python manage.py migrate

4. Run development server
   → python manage.py runserver

5. Test changes
   → Use admin panel or API

6. Commit changes
   → git add .
   → git commit -m "Description"
```

---

## 📞 Getting Help

If you encounter issues:

1. Check error messages carefully
2. Review `.env` configuration
3. Verify PostgreSQL is running
4. Check Python version compatibility
5. Review Django logs in terminal

---

## ✅ Setup Complete!

Once you've completed all steps, you should have:

- ✅ Virtual environment activated
- ✅ All dependencies installed
- ✅ Database created and migrated
- ✅ Superuser created
- ✅ Server running
- ✅ Admin panel accessible

**You're ready to start development!** 🎉

---

## 🔗 Useful Commands Reference

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell (for testing)
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

---

**Happy Coding! 🚀**
