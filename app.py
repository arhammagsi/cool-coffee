"""
╔══════════════════════════════════════════╗
║   COOL COFFEE BAR — app.py               ║
║   Flask entry point · MySQL Edition      ║
╚══════════════════════════════════════════╝

HOW TO RUN:
  pip install flask mysql-connector-python gunicorn
  python app.py
  Open: http://localhost:5000
"""

from flask import Flask
from config import SECRET_KEY
from database.db import close_db
from database.init_db import init_db

from routes.main    import main_bp
from routes.auth    import auth_bp
from routes.orders  import orders_bp
from routes.contact import contact_bp
from routes.admin   import admin_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Close DB connection after each request
app.teardown_appcontext(close_db)

# Register all blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(admin_bp)

# ── DB init on FIRST REQUEST (not at startup) ──────────────────────────────
# Running init_db() at startup causes gunicorn worker timeouts because
# the DB connection hangs for 30 s before Railway's MySQL is reachable.
# Using before_request ensures the app boots instantly; DB is set up on
# the first real HTTP request when MySQL is already up.
_db_ready = False

@app.before_request
def setup_db_once():
    global _db_ready
    if not _db_ready:
        try:
            init_db()
            _db_ready = True
            print("✅ Database initialised")
        except Exception as e:
            print(f"⚠️  DB init failed (will retry next request): {e}")
# ───────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    print("\n☕  Cool Coffee Bar — Running")
    print("   Open: http://localhost:5000\n")
    app.run(debug=True, port=5000)
