import os

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", "change_this_password_immediately"),  # ← set via environment variable
    "database": os.getenv("DB_NAME",     "cool_coffee"),
    "charset":  "utf8mb4",
}

# ⚠️ CRITICAL: Set these via environment variables in production
SECRET_KEY    = os.getenv("SECRET_KEY",    "generate-a-strong-random-key-in-production")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-this-admin-password-in-production")
