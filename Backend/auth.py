# 1. auth.py
# (Handles admin & user authentication routes)

from flask import Blueprint, request, jsonify
import json
import os

auth_bp = Blueprint('auth', __name__)

ADMIN_FILE = os.path.join("Data", "admins.json")
STUDENT_FILE = os.path.join("Data", "students.json")

@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    role = data.get("role")
    user_id = data.get("staffId") or data.get("matric")
    password = data.get("password")

    if not role or not user_id or not password:
        return jsonify({"error": "Missing credentials"}), 400

    if role == "admin":
        if not os.path.exists(ADMIN_FILE):
            return jsonify({"error": "Admin data not found"}), 404
        with open(ADMIN_FILE, 'r') as f:
            admins = json.load(f)
        user = next((a for a in admins if a["staffId"] == user_id and a["password"] == password), None)
    elif role == "student":
        if not os.path.exists(STUDENT_FILE):
            return jsonify({"error": "Student data not found"}), 404
        with open(STUDENT_FILE, 'r') as f:
            students = json.load(f)
        user = next((s for s in students if s["matric"] == user_id and s["password"] == password), None)
    else:
        return jsonify({"error": "Invalid role specified"}), 400

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
