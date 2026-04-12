"""
Create test users for CampusGuard API testing
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusguard.settings')
django.setup()

from authentication.models import User

def create_test_users():
    """Create test users for API testing"""
    
    print("Creating test users...")
    
    # Create Admin user
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@campusguard.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='ADMIN'
        )
        print(f"✓ Created admin user: admin / admin123")
    else:
        print("✓ Admin user already exists")
    
    # Create Security user
    if not User.objects.filter(username='security').exists():
        
        security = User.objects.create_user(
            username='security',
            email='security@campusguard.com',
            password='security123',
            first_name='Security',
            last_name='Officer',
            role='SECURITY'
        )
        print(f"✓ Created security user: security / security123")
    else:
        print("✓ Security user already exists")
    
    print("\nTest users ready!")
    print("Admin: admin / admin123")
    print("Security: security / security123")

if __name__ == "__main__":
    create_test_users()
