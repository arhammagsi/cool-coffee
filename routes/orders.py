import json
from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
from database.db import query

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/order", methods=["POST"])
def place_order():
    if "user_id" not in session:
        return jsonify({"success": False, "errors": ["Please log in to place an order."]}), 401

    data   = request.get_json()
    items  = data.get("items", [])
    branch = data.get("branch", "Phase 8")
    notes  = data.get("notes", "")
    total  = sum(i.get("price", 0) * i.get("qty", 1) for i in items)

    if not items:
        return jsonify({"success": False, "errors": ["Cart is empty."]}), 400

    order_id = query(
        "INSERT INTO orders (user_id, branch, items_json, total, notes) VALUES (%s, %s, %s, %s, %s)",
        (session["user_id"], branch, json.dumps(items), total, notes),
        commit=True,
    )
    return jsonify({
        "success":  True,
        "order_id": order_id,
        "total":    total,
        "message":  f"Order #{order_id} placed! Delivering from {branch} to your door. 🛵✅",
    })


@orders_bp.route("/orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("main.index"))

    rows   = query(
        "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC",
        (session["user_id"],),
    )
    orders = []
    for row in rows:
        o = dict(row)
        o["items"]      = json.loads(o["items_json"])
        o["created_at"] = str(o["created_at"])
        orders.append(o)

    return render_template("orders.html", orders=orders)
