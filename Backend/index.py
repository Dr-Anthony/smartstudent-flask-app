from flask import Flask, request, jsonify
from flask_cors import CORS

from student_data import add_student, get_student_by_matric, update_student
from course_data import add_course, get_courses
from result_data import save_student_result, get_student_result
from notice_data import add_notice, get_notices_for_department
from auth import verify_student_login, verify_admin_login, generate_matric_number, generate_staff_id
from speak import speak_text
from listen import listen_command
from profile_manager import get_profile, update_profile, check_duplicate_fullname

app = Flask(__name__)
CORS(app)

# ---- Student APIs ----

@app.route("/api/student/register", methods=["POST"])
def register_student():
    data = request.json
    add_student(data)
    return jsonify({"message": "Student registered successfully"}), 201

@app.route("/api/student/<matric_no>", methods=["GET"])
def get_student(matric_no):
    student = get_student_by_matric(matric_no)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route("/api/student/<matric_no>", methods=["PUT"])
def update_student_profile(matric_no):
    updates = request.json
    if update_student(matric_no, updates):
        return jsonify({"message": "Profile updated"})
    return jsonify({"error": "Student not found"}), 404

# ---- Course APIs ----

@app.route("/api/course/add", methods=["POST"])
def post_course():
    data = request.json
    dept = data["department"]
    level = data["level"]
    semester = data["semester"]
    course = data["course"]
    add_course(dept, level, semester, course)
    return jsonify({"message": "Course added"})

@app.route("/api/course/get", methods=["GET"])
def fetch_courses():
    dept = request.args.get("department")
    level = request.args.get("level")
    semester = request.args.get("semester")
    courses = get_courses(dept, level, semester)
    return jsonify(courses)

# ---- Result APIs ----

@app.route("/api/result/save", methods=["POST"])
def save_result():
    data = request.json
    save_student_result(data["matric_no"], data["semester"], data["session"], data)
    return jsonify({"message": "Result saved successfully"})

@app.route("/api/result/get", methods=["GET"])
def fetch_result():
    matric = request.args.get("matric_no")
    semester = request.args.get("semester")
    session = request.args.get("session")
    result = get_student_result(matric, semester, session)
    if result:
        return jsonify(result)
    return jsonify({"error": "No result found"}), 404

# ---- Notice APIs ----

@app.route("/api/notice/post", methods=["POST"])
def post_notice():
    data = request.json
    add_notice(data["title"], data["body"], data.get("department", "all"), data.get("attachment"))
    return jsonify({"message": "Notice posted"})

@app.route("/api/notice/get", methods=["GET"])
def get_notices():
    dept = request.args.get("department", "all")
    return jsonify(get_notices_for_department(dept))

# ---- Auth APIs ----

@app.route("/api/login/student", methods=["POST"])
def student_login():
    data = request.json
    student = verify_student_login(data["matric"], data["password"])
    if student:
        return jsonify(student)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/login/admin", methods=["POST"])
def admin_login():
    data = request.json
    admin = verify_admin_login(data["email"], data["password"])
    if admin:
        return jsonify(admin)
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/id/matric", methods=["POST"])
def get_new_matric():
    data = request.json
    matric = generate_matric_number(data["department"], data["year"])
    return jsonify({"matric": matric})

@app.route("/api/id/staff", methods=["GET"])
def get_new_staff_id():
    staff_id = generate_staff_id()
    return jsonify({"staff_id": staff_id})

# ---- Profile APIs ----

@app.route("/api/profile/<matric_no>", methods=["GET"])
def view_profile(matric_no):
    profile = get_profile(matric_no)
    if profile:
        return jsonify(profile)
    return jsonify({"error": "Profile not found"}), 404

@app.route("/api/profile/<matric_no>", methods=["PATCH"])
def update_profile_data(matric_no):
    updates = request.json
    if update_profile(matric_no, updates):
        return jsonify({"message": "Profile updated successfully"})
    return jsonify({"error": "Failed to update profile"}), 400

@app.route("/api/profile/duplicate-check", methods=["POST"])
def check_duplicate():
    data = request.json
    if check_duplicate_fullname(data["fullname"], data["dob"]):
        return jsonify({"duplicate": True})
    return jsonify({"duplicate": False})

@app.route("/api/admin/register", methods=["POST"])
def register_admin():
    data = request.json
    admins = load_json(ADMIN_FILE, [])
    admins.append(data)
    save_json(ADMIN_FILE, admins)
    return jsonify({"message": "Admin registered"})

@app.route("/api/voice/speak", methods=["POST"])
def api_speak():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    speak_text(text)
    return jsonify({"message": f"Speaking: {text}"})

@app.route("/api/voice/listen", methods=["GET"])
def api_listen():
    result = listen_command()
    return jsonify({"result": result})

@app.route("/")
def home():
    return render_template("index.html")

app.run(debug=True)



