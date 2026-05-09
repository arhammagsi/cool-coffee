from flask import Blueprint, render_template, session
from database.db import query

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    user = None
    if "user_id" in session:
        user = query("SELECT * FROM users WHERE id = %s", (session["user_id"],), one=True)
    return render_template("index.html", user=user)
