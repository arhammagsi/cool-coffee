import hashlib
import re
from flask import Blueprint, request, session, redirect, url_for, jsonify
from database.db import query

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    phone    = request.form.get("phone", "").strip()

    errors = []
    if not name:
        errors.append("Name is required.")
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Valid email is required.")
    if len(password) < 6:
        errors.append("Password must be at least 6 characters.")
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    if query("SELECT id FROM users WHERE email = %s", (email,), one=True):
        return jsonify({"success": False, "errors": ["Email already registered."]}), 409

    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    query(
        "INSERT INTO users (name, email, password_hash, phone) VALUES (%s, %s, %s, %s)",
        (name, email, pw_hash, phone),
        commit=True,
    )

    user = query("SELECT * FROM users WHERE email = %s", (email,), one=True)
    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return jsonify({"success": True, "message": f"Welcome to Cool Coffee, {name}! ☕", "name": name})


@auth_bp.route("/login", methods=["POST"])
def login():
    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    pw_hash  = hashlib.sha256(password.encode()).hexdigest()

    user = query(
        "SELECT * FROM users WHERE email = %s AND password_hash = %s",
        (email, pw_hash),
        one=True,
    )
    if user:
        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        return jsonify({"success": True, "message": f"Welcome back, {user['name']}! ☕", "name": user["name"]})

    return jsonify({"success": False, "errors": ["Invalid email or password."]}), 401


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@auth_bp.route("/api/me")
def api_me():
    if "user_id" in session:
        return jsonify({"logged_in": True, "name": session.get("user_name")})
    return jsonify({"logged_in": False})
