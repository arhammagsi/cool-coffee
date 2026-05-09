from flask import Blueprint, request, jsonify
from database.db import query

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["POST"])
def contact():
    name    = request.form.get("name",    "").strip()
    email   = request.form.get("email",   "").strip().lower()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    errors = []
    if not name:    errors.append("Name is required.")
    if not email:   errors.append("Email is required.")
    if not message: errors.append("Message is required.")
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    query(
        "INSERT INTO contact_submissions (name, email, subject, message) VALUES (%s, %s, %s, %s)",
        (name, email, subject, message),
        commit=True,
    )
    return jsonify({"success": True, "message": "Message received! We'll be in touch. ☕"})
