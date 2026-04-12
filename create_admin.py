import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusguard.settings')
django.setup()

from authentication.models import Officer, PoliceStation

print("Seeding database...")

station, _ = PoliceStation.objects.get_or_create(
    name="Ikeja Division Headquarters",
    division="A",
    lga="Ikeja",
    phone="0800POLICE01"
)

# Admin
admin_user, created = Officer.objects.get_or_create(
    badge_number="LSP-ADMIN",
    defaults={
        'first_name': 'Chief',
        'last_name': 'Admin',
        'rank': 'Commissioner',
        'role': 'ADMIN',
        'station': station,
        'email': 'admin@lagospolice.gov.ng',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("Created Admin user (LSP-ADMIN / admin123)")

# Supervisor
super_user, created = Officer.objects.get_or_create(
    badge_number="LSP-00123",
    defaults={
        'first_name': 'Yemi',
        'last_name': 'Adebayo',
        'rank': 'Inspector',
        'role': 'SUPERVISOR',
        'station': station,
        'email': 'y.adebayo@lagospolice.gov.ng'
    }
)
if created:
    super_user.set_password('police123')
    super_user.save()
    print("Created Supervisor user (LSP-00123 / police123)")

# Field Officer
field_user, created = Officer.objects.get_or_create(
    badge_number="LSP-04821",
    defaults={
        'first_name': 'Adeyemi',
        'last_name': 'Bola',
        'rank': 'Sergeant',
        'role': 'FIELD_OFFICER',
        'station': station,
        'email': 'a.bola@lagospolice.gov.ng'
    }
)
if created:
    field_user.set_password('police123')
    field_user.save()
    print("Created Field Officer (LSP-04821 / police123)")

print("Database seeding complete!")
