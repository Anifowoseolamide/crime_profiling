import os
import django
import base64

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusguard.settings')
django.setup()

from subjects.models import Subject
from services.faceplusplus import faceplusplus
from identification.views import IdentifyView
from rest_framework.test import APIRequestFactory, force_authenticate
from authentication.models import Officer

def test_facepp_mock():
    print("Testing Face++ Mock Implementation...")
    
    # 1. Test Service directly
    mock_image = b"fake image content"
    result = faceplusplus.identify(mock_image)
    print(f"Service Identify Result (Mock): {result}")
    
    # 2. Test Enrollment (Mock)
    subject = Subject.objects.create(first_name="Test", last_name="Subject")
    print(f"Created Test Subject: {subject.id}")
    
    enroll_result = faceplusplus.enrol_subject(subject.face_recognition_id, mock_image)
    print(f"Service Enrol Result (Mock): {enroll_result}")
    
    # 3. Test View Integration
    factory = APIRequestFactory()
    officer = Officer.objects.filter(is_superuser=True).first()
    if not officer:
        officer = Officer.objects.create_superuser(badge_number="TESTADMIN", password="password")
    
    view = IdentifyView.as_view()
    
    # Create a fake base64 image
    base64_img = base64.b64encode(mock_image).decode('utf-8')
    
    request = factory.post('/api/identify/', {
        'image': f"data:image/jpeg;base64,{base64_img}",
        'location': 'Test Location'
    }, format='json')
    
    force_authenticate(request, user=officer)
    response = view(request)
    
    print(f"Identify View Response Status: {response.status_code}")
    print(f"Identify View Response Data: {response.data}")
    
    # Cleanup
    subject.delete()
    print("Test Complete.")

if __name__ == "__main__":
    test_facepp_mock()
