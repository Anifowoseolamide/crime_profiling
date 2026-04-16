import requests
import json
import base64
import time

BASE_URL = "http://localhost:8000/api/v1"

def get_admin_token():
    res = requests.post(f"{BASE_URL}/auth/login/", json={"username": "admin", "password": "admin123"})
    return res.json().get("access")

def test_gps_logging():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Test Identification GPS
    print("\n--- Testing Identification GPS ---")
    # Base64 for a 1x1 pixel grey JPEG
    minimal_jpeg = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKVVZW2ZgzhYWVjGGlJic3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpq6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5/ooov//Z"
    
    scan_data = {
        "image": minimal_jpeg,
        "location": "Test Lab",
        "latitude": 6.4523,
        "longitude": 3.3908,
        "notes": "Automated GPS Test"
    }
    
    res = requests.post(f"{BASE_URL}/identify/", json=scan_data, headers=headers)
    if res.status_code == 200:
        print("✓ Identification Scan Successful")
        log_id = res.json().get("log_id")
        # Verify log
        log_res = requests.get(f"{BASE_URL}/identify/logs/", headers=headers)
        logs = log_res.json().get("results", [])
        latest = logs[0] if logs else {}
        if latest.get("latitude") == 6.4523:
            print("✓ Coordinates saved in IdentificationLog")
        else:
            print(f"✗ Coordinates mismatch: {latest.get('latitude')}")
    else:
        print(f"✗ Identification failed: {res.text}")

    # 2. Test Offence GPS
    print("\n--- Testing Offence GPS ---")
    # Get a subject ID first
    subj_res = requests.get(f"{BASE_URL}/subjects/", headers=headers)
    subjects = subj_res.json().get("results", [])
    if not subjects:
        print("✗ No subjects found for testing")
        return
        
    subject_id = subjects[0]["id"]
    # Get a station ID
    stat_res = requests.get(f"{BASE_URL}/auth/stations/", headers=headers)
    stations = stat_res.json()
    station_id = stations[0]["id"] if stations else None

    offence_data = {
        "subject_id": subject_id,
        "station_id": station_id,
        "offence_category": "OTHER",
        "offence_title": "GPS Test Offence",
        "description": "Testing latitude/longitude capture",
        "severity": "MINOR",
        "incident_date": "2026-04-15T12:00:00Z",
        "location": "GPS Test Field",
        "latitude": 6.5555,
        "longitude": 3.4444
    }
    
    res = requests.post(f"{BASE_URL}/offences/", json=offence_data, headers=headers)
    if res.status_code == 201:
        print("✓ Offence Logging Successful")
        if res.json().get("latitude") == 6.5555:
             print("✓ Coordinates saved in Offence")
        else:
             print(f"✗ Coordinates mismatch in Offence: {res.json().get('latitude')}")
    else:
        print(f"✗ Offence logging failed: {res.text}")

    # 3. Test Mugshot Enrollment GPS
    print("\n--- Testing Mugshot GPS ---")
    enrol_data = {
        "image": minimal_jpeg,
        "latitude": 6.7777,
        "longitude": 3.8888
    }
    res = requests.post(f"{BASE_URL}/subjects/{subject_id}/enrol-mugshot/", json=enrol_data, headers=headers)
    if res.status_code == 201:
        print("✓ Mugshot Enrollment Successful")
        if res.json().get("latitude") == 6.7777:
            print("✓ Coordinates saved in Mugshot")
        else:
            print(f"✗ Coordinates mismatch in Mugshot: {res.json().get('latitude')}")
    else:
        print(f"✗ Mugshot enrollment failed: {res.text}")

if __name__ == "__main__":
    test_gps_logging()
