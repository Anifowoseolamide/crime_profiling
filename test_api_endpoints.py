"""
Automated API Endpoint Testing Script
Tests major CampusGuard endpoints including student registration and offence tracking
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:8000/api/v1"

# Generate unique identifiers for this test run
TEST_RUN_ID = int(time.time())  # Unix timestamp
UNIQUE_MATRIC = f"2026{TEST_RUN_ID % 100000:05d}"  # e.g., 202612345
UNIQUE_STUDENT_ID = f"STU{TEST_RUN_ID % 1000000:06d}"  # e.g., STU012345
UNIQUE_EMAIL = f"test.student.{TEST_RUN_ID}@student.lasu.edu.ng"
UNIQUE_PRE_REG_MATRIC = f"1904{TEST_RUN_ID % 100000:05d}"  # For pre-registration test

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, status, details=""):
    """Print test result with color"""
    color = Colors.GREEN if status == "PASS" else Colors.RED
    print(f"{color}{'✓' if status == 'PASS' else '✗'} {name}{Colors.END}")
    if details:
        print(f"  {details}")

def print_section(name):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}{Colors.END}\n")

# Test results storage
results = {
    "passed": 0,
    "failed": 0,
    "tests": []
}

def test_endpoint(name, method, endpoint, data=None, headers=None, expected_status=200):
    """Generic endpoint tester"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers)
        else:
            response = requests.request(method, url, json=data, headers=headers)
        
        if response.status_code == expected_status:
            results["passed"] += 1
            results["tests"].append({"name": name, "status": "PASS"})
            print_test(name, "PASS", f"Status: {response.status_code}")
            return response.json() if response.content else {}
        else:
            results["failed"] += 1
            results["tests"].append({"name": name, "status": "FAIL"})
            print_test(name, "FAIL", f"Expected {expected_status}, got {response.status_code}")
            if response.content:
                print(f"  Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        results["failed"] += 1
        results["tests"].append({"name": name, "status": "ERROR"})
        print_test(name, "FAIL", f"Error: {str(e)}")
        return None

def main():
    """Run all endpoint tests"""
    
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("  CampusGuard API Endpoint Testing")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Test Run ID: {TEST_RUN_ID}")
    print(f"{'='*60}{Colors.END}")
    
    # Global variables for test data
    admin_token = None
    security_token = None
    student_token = None
    student_id = None
    offence_id = None
    
    # ========================================================================
    # 1. AUTHENTICATION TESTS
    # ========================================================================
    print_section("1. Authentication Tests")
    
    # Test 1.1: Admin Login
    admin_data = test_endpoint(
        "Admin Login",
        "POST",
        "/auth/login/",
        data={"username": "admin", "password": "admin123"}
    )
    
    if admin_data:
        admin_token = admin_data.get("access")
        print(f"  {Colors.GREEN}Admin token obtained{Colors.END}")
    
    # Test 1.2: Invalid Login
    test_endpoint(
        "Invalid Login (Should Fail)",
        "POST",
        "/auth/login/",
        data={"username": "invalid", "password": "wrong"},
        expected_status=400
    )
    
    # Test 1.3: Get Profile
    if admin_token:
        test_endpoint(
            "Get User Profile",
            "GET",
            "/auth/profile/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    # ========================================================================
    # 2. STUDENT MANAGEMENT TESTS
    # ========================================================================
    print_section("2. Student Management Tests")
    
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Test 2.1: List Students
        test_endpoint(
            "List Students",
            "GET",
            "/students/",
            headers=headers
        )
        
        # Test 2.2: Create Student (Admin) - with unique identifiers
        print(f"  {Colors.YELLOW}Creating student with unique ID: {UNIQUE_STUDENT_ID}{Colors.END}")
        student_data = test_endpoint(
            "Create Student (Admin)",
            "POST",
            "/students/",
            data={
                "student_id": UNIQUE_STUDENT_ID,
                "matric_number": UNIQUE_MATRIC,
                "first_name": "Test",
                "last_name": "Student",
                "email": UNIQUE_EMAIL,
                "phone_number": "+2348012345678",
                "date_of_birth": "2003-01-15",
                "gender": "M",
                "department": "Computer Science"
            },
            headers=headers,
            expected_status=201
        )
        
        if student_data:
            student_id = student_data.get("id")
            print(f"  {Colors.GREEN}Student ID: {student_id}{Colors.END}")
    
    # ========================================================================
    # 3. PRE-REGISTRATION OFFENCE TESTS
    # ========================================================================
    print_section("3. Pre-Registration Offence Tracking Tests")
    
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Test 3.1: Create Pre-Registration Offence - with unique matric number
        print(f"  {Colors.YELLOW}Creating pre-registration offence for matric: {UNIQUE_PRE_REG_MATRIC}{Colors.END}")
        offence_data = test_endpoint(
            "Create Pre-Registration Offence (Matric Number)",
            "POST",
            "/offences/",
            data={
                "matric_number": UNIQUE_PRE_REG_MATRIC,
                "offence_type": "LATE_ENTRY",
                "severity": "MEDIUM",
                "title": "Late entry to campus",
                "description": "Student entered campus after 10 PM",
                "location": "Main Gate",
                "incident_date": "2026-01-05T22:30:00Z"
            },
            headers=headers,
            expected_status=201
        )
        
        if offence_data:
            offence_id = offence_data.get("id")
            print(f"  {Colors.GREEN}Pre-registration offence created{Colors.END}")
            print(f"  Matric Number: {offence_data.get('matric_number')}")
            print(f"  Linked to student: {offence_data.get('is_linked_to_student')}")
        
        # Test 3.2: Create Offence for Registered Student
        if student_id:
            test_endpoint(
                "Create Offence (Registered Student)",
                "POST",
                "/offences/",
                data={
                    "student_id": student_id,
                    "offence_type": "DRESS_CODE",
                    "severity": "LOW",
                    "title": "Dress code violation",
                    "description": "Student not wearing proper uniform",
                    "location": "Library",
                    "incident_date": "2026-01-05T09:00:00Z"
                },
                headers=headers,
                expected_status=201
            )
        
        # Test 3.3: List All Offences
        test_endpoint(
            "List All Offences",
            "GET",
            "/offences/",
            headers=headers
        )
        
        # Test 3.4: Update Offence Status
        if offence_id:
            test_endpoint(
                "Update Offence Status",
                "PATCH",
                f"/offences/{offence_id}/",
                data={
                    "status": "RESOLVED",
                    "action_taken": "Student counseled",
                    "penalty": "Written warning"
                },
                headers=headers
            )
    
    # ========================================================================
    # 4. STUDENT SELF-REGISTRATION TESTS (Simulated)
    # ========================================================================
    print_section("4. Student Self-Registration Tests")
    
    # Test 4.1: Initiate Registration (No Auth Required)
    print(f"{Colors.YELLOW}Note: Email verification requires LASU API and SMTP configuration{Colors.END}")
    test_endpoint(
        "Initiate Student Registration",
        "POST",
        "/auth/student/register/initiate/",
        data={"matric_number": "190401001"},
        expected_status=503  # Expected to fail without LASU API
    )
    
    # ========================================================================
    # 5. ADMIN ENDPOINTS TESTS
    # ========================================================================
    print_section("5. Admin Endpoints Tests")
    
    if admin_token:
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Test 5.1: List All Users
        test_endpoint(
            "List All Users (Admin)",
            "GET",
            "/auth/users/",
            headers=headers
        )
        
        # Test 5.2: Pending Verifications
        test_endpoint(
            "List Pending Verifications",
            "GET",
            "/auth/pending-verifications/",
            headers=headers
        )
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print(f"\n{Colors.BLUE}{'='*60}")
    print("  Test Summary")
    print(f"{'='*60}{Colors.END}\n")
    
    total = results["passed"] + results["failed"]
    pass_rate = (results["passed"] / total * 100) if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.END}")
    print(f"Pass Rate: {pass_rate:.1f}%\n")
    
    if results["failed"] == 0:
        print(f"{Colors.GREEN}✓ All tests passed!{Colors.END}\n")
    else:
        print(f"{Colors.YELLOW}⚠ Some tests failed. Check details above.{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Test suite error: {str(e)}{Colors.END}")
