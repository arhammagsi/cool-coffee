import json
from flask import Blueprint, request, session, render_template
from database.db import query
from config import ADMIN_PASSWORD

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
        else:
            return render_template("admin.html", error="Wrong password.", authed=False)

    if not session.get("admin"):
        return render_template("admin.html", authed=False)

    users    = query("SELECT id, name, email, phone, created_at FROM users ORDER BY created_at DESC")
    orders   = query(
        "SELECT o.*, u.name AS user_name FROM orders o "
        "JOIN users u ON o.user_id = u.id ORDER BY o.created_at DESC"
    )
    contacts = query("SELECT * FROM contact_submissions ORDER BY created_at DESC")

    orders_parsed = []
    for row in orders:
        o = dict(row)
        o["items"]      = json.loads(o["items_json"])
        o["created_at"] = str(o["created_at"])
        orders_parsed.append(o)

    users_clean    = [dict(u) for u in users]
    contacts_clean = [dict(c) for c in contacts]
    for u in users_clean:    u["created_at"] = str(u["created_at"])
    for c in contacts_clean: c["created_at"] = str(c["created_at"])

    return render_template("admin.html",
        authed=True,
        users=users_clean,
        orders=orders_parsed,
        contacts=contacts_clean,
    )
