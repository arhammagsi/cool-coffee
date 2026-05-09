import mysql.connector
from flask import g
from config import DB_CONFIG


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=(), one=False, commit=False):
    """
    Run a SQL query.
      - one=True    → return a single row (or None)
      - commit=True → commit and return lastrowid
      - default     → return list of rows
    """
    db     = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params)

    if commit:
        db.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    rows = cursor.fetchall()
    cursor.close()
    return (rows[0] if rows else None) if one else rows
