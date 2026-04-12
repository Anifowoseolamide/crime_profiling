# CampusGuard Deployment Guide for Render

This guide provides step-by-step instructions for deploying the CampusGuard Django application to Render.

## Prerequisites

- GitHub account with your CampusGuard repository
- Render account (sign up at [render.com](https://render.com))
- Production credentials ready (SECRET_KEY, Cloudinary, LASU API, Email)

## Overview

The deployment consists of:
- **Web Service**: Django application running on Gunicorn
- **PostgreSQL Database**: Managed database instance
- **Static Files**: Served via WhiteNoise

## Step 1: Prepare Your Repository

Ensure these files are in your repository:

```
CampusGuard/
├── build.sh                 # Build script
├── render.yaml              # Infrastructure configuration
├── requirements.txt         # Python dependencies
├── campusguard/
│   ├── settings.py         # Production-ready settings
│   └── wsgi.py             # WSGI application
└── .env.example            # Environment variables template
```

**Important**: Make sure `build.sh` has executable permissions:
```bash
git update-index --chmod=+x build.sh
git commit -m "Make build.sh executable"
git push
```

## Step 2: Create Render Services

### Option A: Using render.yaml (Recommended)

1. **Push to GitHub**: Ensure all changes are committed and pushed
2. **Connect Repository**:
   - Log in to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing CampusGuard
3. **Deploy**: Render will automatically create the web service and database from `render.yaml`

### Option B: Manual Setup

#### Create PostgreSQL Database

1. In Render Dashboard, click "New" → "PostgreSQL"
2. Configure:
   - **Name**: `campusguard-db`
   - **Database**: `campusguard_db`
   - **User**: `campusguard_user`
   - **Region**: Choose closest to your users
   - **Plan**: Start with Free (upgrade for production)
3. Click "Create Database"
4. **Save the Internal Database URL** (found under "Connections")

#### Create Web Service

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `campusguard`
   - **Region**: Same as database
   - **Branch**: `main` (or your default branch)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn campusguard.wsgi:application`
   - **Plan**: Start with Free (upgrade for production)

## Step 3: Configure Environment Variables

In your Web Service settings, go to "Environment" and add these variables:

### Required Variables

```bash
# Django Core
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
PYTHON_VERSION=3.11.0

# Database (automatically set if using Blueprint)
DATABASE_URL=<your-postgres-internal-url>

# Frontend
FRONTEND_URL=https://your-frontend-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com,https://your-frontend-domain.com

# Cloudinary (for image/media storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# LASU API Integration
LASU_API_URL=https://api.lasu.edu.ng/verify
LASU_API_KEY=your_lasu_production_api_key

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password
DEFAULT_FROM_EMAIL=noreply@campusguard.lasu.edu.ng

# JWT Token Lifetimes (optional - defaults in settings.py)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# AI Settings (optional - defaults in settings.py)
FACE_RECOGNITION_THRESHOLD=0.6
MAX_FACE_DISTANCE=0.6
```

### Generate SECRET_KEY

In Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use an online generator (ensure it's secure).

### Get DATABASE_URL

- If using Blueprint: Automatically configured
- If manual setup: Copy from your PostgreSQL instance → "Connections" → "Internal Database URL"

## Step 4: Deploy

1. **Manual Trigger**: Click "Manual Deploy" → "Deploy latest commit"
2. **Monitor Build**: Watch the logs in real-time
3. **Build Process**:
   - Installs dependencies from `requirements.txt`
   - Runs database migrations
   - Collects static files

**Expected Build Time**: 5-10 minutes (TensorFlow/DeepFace are large)

## Step 5: Post-Deployment Verification

### Check Deployment Status

1. **Build Logs**: Ensure no errors during build
2. **Live URL**: Click the generated URL (e.g., `https://campusguard.onrender.com`)
3. **Health Check**: Navigate to `/admin/` - should see Django admin login

### Verify Database

Access Render Shell (in Web Service → "Shell"):

```bash
python manage.py showmigrations
# All migrations should show [X]

python manage.py createsuperuser
# Create an admin account
```

### Test API Endpoints

Using Postman or curl:

```bash
# Health check
curl https://your-app.onrender.com/admin/

# API documentation
curl https://your-app.onrender.com/api/schema/swagger-ui/

# Test authentication endpoint
curl -X POST https://your-app.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

### Check Static Files

- Navigate to `/admin/`
- Verify CSS and styles are loading correctly
- If styles are missing, check WhiteNoise configuration

## Step 6: Update Frontend Configuration

Update your frontend application to use the production API URL:

```javascript
// config.js or similar
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://campusguard.onrender.com';
```

## Troubleshooting

### Build Failures

**Issue**: `build.sh: Permission denied`
```bash
# Solution: Make build.sh executable
git update-index --chmod=+x build.sh
git commit -m "Fix build.sh permissions"
git push
```

**Issue**: `ModuleNotFoundError`
```bash
# Solution: Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Database Issues

**Issue**: `OperationalError: FATAL: password authentication failed`
- Verify `DATABASE_URL` is correctly set in environment variables
- Ensure it's the **Internal Database URL** from Render

**Issue**: Migrations not applied
```bash
# In Render Shell
python manage.py migrate --run-syncdb
```

### Static Files Not Loading

**Issue**: 404 errors for `/static/` files
1. Check `STATIC_ROOT` in `settings.py`: Should be `BASE_DIR / 'staticfiles'`
2. Verify WhiteNoise is in `MIDDLEWARE` (after `SecurityMiddleware`)
3. Check `build.sh` runs `collectstatic --no-input`

### CORS Errors

**Issue**: Frontend can't connect to API
```bash
# In Render Environment Variables
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app,https://your-app.onrender.com
```

### Performance Issues

**Issue**: Slow startup/requests on Free tier
- Render's free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- **Solution**: Upgrade to paid tier for production

### Large Build Size

**Issue**: Build exceeds storage limits
- TensorFlow/DeepFace are large (~1GB)
- Consider removing AI dependencies if not needed in production
- Or use a separate microservice for face recognition

## Environment-Specific Settings

### Development (.env)
```bash
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://postgres:password@localhost:5432/campusguard_db
```

### Production (Render Environment Variables)
```bash
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=<render-provided-url>
```

## Maintenance

### View Logs
- **Build Logs**: Shows deployment process
- **Runtime Logs**: Shows application logs (print statements, errors)
- Access via Render Dashboard → Your Service → "Logs"

### Database Backups
Render automatically backs up PostgreSQL databases on paid plans. For free tier:
1. Use Render Shell to export data
2. Or upgrade to paid plan for automatic backups

### Updating the Application
1. Push changes to GitHub
2. Render automatically redeploys (if auto-deploy is enabled)
3. Or manually trigger deployment from Dashboard

### Scaling
- **Horizontal**: Increase number of instances (paid plans)
- **Vertical**: Upgrade to larger instance types
- **Database**: Upgrade PostgreSQL plan for more storage/connections

## Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` generated
- ✅ HTTPS enabled (automatic on Render)
- ✅ CORS configured for specific origins only
- ✅ Database uses internal URL (not exposed publicly)
- ✅ Sensitive credentials in environment variables (not in code)
- ✅ HSTS headers enabled (automatic when `DEBUG=False`)
- ✅ CSRF protection enabled with trusted origins

## Costs

### Free Tier Limitations
- **Web Service**: 750 hours/month, sleeps after 15 min inactivity
- **PostgreSQL**: 90 days, then deleted (upgrade to keep)
- **Bandwidth**: 100 GB/month
- **Build Minutes**: 500 min/month

### Recommended Production Setup
- **Web Service**: Starter ($7/month) - No sleep, more resources
- **PostgreSQL**: Starter ($7/month) - Persistent, automated backups
- **Total**: ~$14/month

## Support Resources

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **WhiteNoise**: http://whitenoise.evans.io/
- **Community**: Render Community Forum

## Next Steps

1. ✅ Deploy to Render
2. ⬜ Set up custom domain (optional)
3. ⬜ Configure monitoring/alerts
4. ⬜ Set up CI/CD pipeline
5. ⬜ Load test and optimize
6. ⬜ Plan backup strategy
