"""
Mock LASU API Server for Testing Student Registration
Simulates the LASU verification API for testing purposes
"""

from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Mock student database
MOCK_STUDENTS = {
    "190401001": {
        "exists": True,
        "status": "ACTIVE",
        "full_name": "John Doe",
        "email": "john.doe@student.lasu.edu.ng",
        "department": "Computer Science"
    },
    "190401002": {
        "exists": True,
        "status": "ACTIVE",
        "full_name": "Jane Smith",
        "email": "jane.smith@student.lasu.edu.ng",
        "department": "Engineering"
    },
    "190401003": {
        "exists": True,
        "status": "ACTIVE",
        "full_name": "Bob Johnson",
        "email": "bob.johnson@student.lasu.edu.ng",
        "department": "Business Administration"
    },
    "190401999": {
        "exists": True,
        "status": "ACTIVE",
        "full_name": "Test Student",
        "email": "test.student@student.lasu.edu.ng",
        "department": "Computer Science"
    }
}

@app.route('/verify-student', methods=['GET'])
def verify_student():
    """
    Verify student by matric number
    Query params: matric
    """
    # Check API key
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    matric = request.args.get('matric')
    if not matric:
        return jsonify({"error": "Matric number is required"}), 400
    
    logging.info(f"Verifying matric number: {matric}")
    
    # Check if student exists in mock database
    if matric in MOCK_STUDENTS:
        student_data = MOCK_STUDENTS[matric]
        logging.info(f"Student found: {student_data['full_name']}")
        return jsonify(student_data), 200
    
    # For any matric number starting with specific patterns, auto-generate
    if matric.startswith('1904') or matric.startswith('2026'):
        # Auto-generate student data for testing
        student_data = {
            "exists": True,
            "status": "ACTIVE",
            "full_name": f"Test Student {matric[-4:]}",
            "email": f"student.{matric}@student.lasu.edu.ng",
            "department": "Computer Science"
        }
        logging.info(f"Auto-generated student data for {matric}")
        return jsonify(student_data), 200
    
    # Student not found
    logging.warning(f"Student not found: {matric}")
    return jsonify({
        "exists": False,
        "status": "NOT_FOUND"
    }), 404

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Mock LASU API"}), 200

if __name__ == '__main__':
    print("=" * 60)
    print("  Mock LASU API Server")
    print("  Running on http://localhost:5000")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET /verify-student?matric=<matric_number>")
    print("  GET /health")
    print("\nAuthentication:")
    print("  Header: Authorization: Bearer <any_token>")
    print("\nMock Students:")
    for matric, data in MOCK_STUDENTS.items():
        print(f"  {matric}: {data['full_name']} ({data['email']})")
    print("\nAuto-generates data for matric numbers starting with 1904 or 2026")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
