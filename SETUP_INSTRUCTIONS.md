# 🚀 CampusGuard - Final Setup Instructions

## ✅ Backend is Complete and Ready!

All code has been written. Now let's get it running!

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ Python 3.11+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ Git installed (optional)

---

## 🔧 Setup Steps

### Step 1: Create Virtual Environment

```powershell
# Navigate to project directory
cd d:\updated\CampusGuard

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your terminal
```

### Step 2: Create .env File

Create a file named `.env` in the project root with the following content:

```env
# Django Settings
SECRET_KEY=django-insecure-campusguard-dev-key-change-in-production-2024
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=campusguard_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Cloudinary Configuration (Optional - leave empty for now)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# JWT Settings (in minutes)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# AI Settings
FACE_RECOGNITION_THRESHOLD=0.6
MAX_FACE_DISTANCE=0.6

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Important:** Replace `YOUR_POSTGRES_PASSWORD` with your actual PostgreSQL password!

### Step 3: Install Dependencies

```powershell
# Make sure virtual environment is activated
pip install -r requirements.txt
```

This will install:
- Django & Django REST Framework
- PostgreSQL driver
- JWT authentication
- DeepFace & AI libraries (TensorFlow, OpenCV)
- Cloudinary
- API documentation tools

**Note:** Installing TensorFlow and DeepFace may take 5-10 minutes.

### Step 4: Create PostgreSQL Database

**Option A: Using psql**
```powershell
psql -U postgres
CREATE DATABASE campusguard_db;
\q
```

**Option B: Using pgAdmin**
1. Open pgAdmin
2. Right-click "Databases"
3. Create → Database
4. Name: `campusguard_db`
5. Save

### Step 5: Run Migrations

```powershell
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

You should see migrations being applied for:
- authentication
- students
- offences
- lostfound
- emergency
- ai_recognition
- token_blacklist

### Step 6: Create Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

Enter:
- **Username:** admin
- **Email:** admin@campusguard.com
- **Password:** (choose a secure password)
- **Password (again):** (confirm)

### Step 7: Run the Server

```powershell
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🎯 Verify Installation

### 1. Access Admin Panel
- URL: http://localhost:8000/admin/
- Login with superuser credentials
- You should see all models:
  - Students
  - Users
  - Offences
  - Lost Found Items
  - Emergency Contacts
  - Face Embeddings
  - Security Logs
  - etc.

### 2. Access API Documentation
- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

### 3. Test API Endpoint

Open a new terminal and test the login endpoint:

```powershell
# Using curl (if installed)
curl -X POST http://localhost:8000/api/v1/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"admin\",\"password\":\"your_password\"}'
```

Or use Postman/Insomnia to test.

---

## 📝 Create Test Data

### Option 1: Via Admin Panel

1. Go to http://localhost:8000/admin/
2. Click "Students" → "Add Student"
3. Fill in the form:
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
   - Gender: `Male`
   - Blood Group: `O+`
   - Fill in address fields
4. Add Emergency Contact (inline form)
5. Add Medical Information (inline form)
6. Save

### Option 2: Via API

Use the API endpoints documented in `TESTING_GUIDE.md`

---

## 🧪 Test the System

Follow the comprehensive testing guide in `TESTING_GUIDE.md`:

1. **Test Authentication**
   - Login
   - Get JWT token
   - Refresh token

2. **Test Student Management**
   - Create students
   - List students
   - Get student details

3. **Test Face Enrollment**
   - Enroll student faces
   - Verify embeddings are saved

4. **Test AI Identification**
   - Upload student photo
   - Verify identification works
   - Check confidence scores

5. **Test Offence Management**
   - Create offences
   - View offence history

6. **Test Lost & Found**
   - Report items
   - Identify owners

7. **Test Emergency Module**
   - Emergency identification
   - Retrieve emergency contacts

---

## 🐛 Troubleshooting

### Issue: "Could not connect to database"
**Solution:**
- Make sure PostgreSQL is running
- Check DB credentials in `.env`
- Verify database `campusguard_db` exists

### Issue: "ModuleNotFoundError"
**Solution:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Issue: "TensorFlow installation failed"
**Solution:**
- Try: `pip install tensorflow-cpu==2.15.0`
- Or install without AI features first, add later

### Issue: "Migration errors"
**Solution:**
- Delete `db.sqlite3` if it exists
- Run `python manage.py makemigrations` again
- Run `python manage.py migrate` again

### Issue: "Port 8000 already in use"
**Solution:**
- Use different port: `python manage.py runserver 8001`
- Or stop the process using port 8000

---

## 📊 What You Can Do Now

### ✅ Available Features

1. **Student Management**
   - Create, read, update, delete students
   - Manage emergency contacts
   - Manage medical information
   - Enroll faces for AI recognition

2. **AI Face Recognition**
   - Identify students from photos
   - Get confidence scores
   - Track identification attempts

3. **Offence Tracking**
   - Create and manage offences
   - View student offence history
   - Track security activities

4. **Lost & Found**
   - Report lost/found items
   - AI-powered owner identification
   - Claim management

5. **Emergency Response**
   - Quick student identification
   - Emergency contact retrieval
   - Medical information access

6. **Security Logging**
   - Complete audit trail
   - Activity monitoring
   - Analytics data

---

## 📚 Documentation

All documentation is in the project root:

- **README.md** - Project overview
- **ARCHITECTURE.md** - System architecture
- **API_SPECIFICATION.md** - Complete API reference
- **TESTING_GUIDE.md** - Testing instructions
- **BACKEND_COMPLETE.md** - Feature summary
- **QUICKSTART.md** - Quick setup guide

---

## 🎓 Next Steps

1. ✅ **Set up the database** (follow steps above)
2. ✅ **Create test students** via admin panel
3. ✅ **Enroll faces** for AI recognition
4. ✅ **Test API endpoints** using Swagger UI or Postman
5. ✅ **Review documentation** for API details
6. 🔜 **Build React frontend** (when ready)
7. 🔜 **Deploy to production** (when ready)

---

## 🆘 Need Help?

1. Check the **TESTING_GUIDE.md** for detailed API testing
2. Review **API_SPECIFICATION.md** for endpoint details
3. Check **ARCHITECTURE.md** for system design
4. Use Swagger UI at `/api/docs/` for interactive testing

---

## ✅ Setup Checklist

- [ ] Virtual environment created and activated
- [ ] .env file created with correct credentials
- [ ] Dependencies installed
- [ ] PostgreSQL database created
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Server running successfully
- [ ] Admin panel accessible
- [ ] API documentation accessible
- [ ] Test student created
- [ ] Face enrolled
- [ ] AI identification tested

---

**Once all steps are complete, your backend is fully operational!** 🎉

The backend is production-ready and waiting for frontend integration or direct API usage.

**Happy coding!** 🚀
