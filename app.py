"""
╔══════════════════════════════════════════╗
║   COOL COFFEE BAR — app.py               ║
║   Flask entry point · MySQL Edition      ║
╚══════════════════════════════════════════╝

HOW TO RUN:
  pip install flask mysql-connector-python
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

# Init DB on startup — wrapped so a missing DB doesn't crash the whole app
with app.app_context():
    try:
        init_db()
        print("✅ Database initialised successfully")
    except Exception as e:
        print(f"⚠️  DB init skipped (will retry on first request): {e}")


if __name__ == "__main__":
    print("\n☕  Cool Coffee Bar — Running")
    print("   Open: http://localhost:5000\n")
    app.run(debug=True, port=5000)
