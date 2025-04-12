import json
import os

STUDENT_FILE = os.path.join('Data', 'students.json')
ADMIN_FILE = os.path.join('Data', 'admins.json')
COUNTER_FILE = os.path.join('Data', 'counters.json')

def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def generate_matric_number(department, year):
    counters = load_json(COUNTER_FILE, {})
    key = f"{department}_{year}"
    count = counters.get(key, 0) + 1
    counters[key] = count
    save_json(COUNTER_FILE, counters)

    dept_code = department[:3].upper()
    year_suffix = year[-2:]
    serial = str(count).zfill(4)
    return f"AOC/{dept_code}/{year_suffix}/{serial}"

def generate_staff_id():
    counters = load_json(COUNTER_FILE, {})
    count = counters.get("staff", 0) + 1
    counters["staff"] = count
    save_json(COUNTER_FILE, counters)

    return f"ADM{str(count).zfill(4)}"

def verify_student_login(matric, password):
    students = load_json(STUDENT_FILE, [])
    for student in students:
        if student.get("matric") == matric and student.get("password") == password:
            return student
    return None

def verify_admin_login(email, password):
    admins = load_json(ADMIN_FILE, [])
    for admin in admins:
        if admin.get("email") == email and admin.get("password") == password:
            return admin
    return None
