# LagosCP Backend Setup Script
# Run this script to set up the database and create initial data

Write-Host "🎓 LagosCP Backend Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create one first: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Copying .env.example to .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env with your database credentials before continuing!" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter when you've updated .env file"
}

Write-Host ""
Write-Host "Step 1: Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Creating migrations..." -ForegroundColor Cyan
python manage.py makemigrations

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create migrations!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Migrations created" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Applying migrations..." -ForegroundColor Cyan
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to apply migrations!" -ForegroundColor Red
    Write-Host "Make sure PostgreSQL is running and credentials in .env are correct" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Migrations applied" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4: Creating superuser..." -ForegroundColor Cyan
Write-Host "Please enter superuser details:" -ForegroundColor Yellow
python manage.py createsuperuser

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Superuser creation skipped or failed" -ForegroundColor Yellow
} else {
    Write-Host "✅ Superuser created" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run the server: python manage.py runserver" -ForegroundColor White
Write-Host "2. Access admin panel: http://localhost:8000/admin/" -ForegroundColor White
Write-Host "3. Access API docs: http://localhost:8000/api/docs/" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green
