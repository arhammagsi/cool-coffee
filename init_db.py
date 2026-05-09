import mysql.connector
from config import DB_CONFIG


def init_db():
    """Create database + tables and seed menu if empty. Called once on app startup."""

    db_name = DB_CONFIG["database"]   # e.g. "cool_coffee"
    base = {
        "host":     DB_CONFIG["host"],
        "port":     DB_CONFIG["port"],
        "user":     DB_CONFIG["user"],
        "password": DB_CONFIG["password"],
        "charset":  "utf8mb4",
        "connection_timeout": 10,
    }

    # Step 1 — try to connect directly to the target database
    try:
        conn = mysql.connector.connect(**base, database=db_name)
    except mysql.connector.errors.ProgrammingError:
        # Database doesn't exist yet — create it first (root access needed)
        conn = mysql.connector.connect(**base)
        cur  = conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        cur.close()
        conn.close()
        conn = mysql.connector.connect(**base, database=db_name)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id            INT AUTO_INCREMENT PRIMARY KEY,
        name          VARCHAR(120) NOT NULL,
        email         VARCHAR(180) NOT NULL UNIQUE,
        password_hash VARCHAR(64)  NOT NULL,
        phone         VARCHAR(30)  DEFAULT '',
        created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id         INT AUTO_INCREMENT PRIMARY KEY,
        user_id    INT           NOT NULL,
        branch     VARCHAR(80)   NOT NULL DEFAULT 'Phase 8',
        items_json MEDIUMTEXT    NOT NULL,
        total      DECIMAL(10,2) NOT NULL DEFAULT 0,
        notes      VARCHAR(500)  DEFAULT '',
        status     VARCHAR(30)   DEFAULT 'pending',
        created_at DATETIME      DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_submissions (
        id         INT AUTO_INCREMENT PRIMARY KEY,
        name       VARCHAR(120)  NOT NULL,
        email      VARCHAR(180)  NOT NULL,
        subject    VARCHAR(220)  DEFAULT '',
        message    VARCHAR(2000) NOT NULL,
        is_read    TINYINT(1)    DEFAULT 0,
        created_at DATETIME      DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        category    VARCHAR(30)  NOT NULL,
        name        VARCHAR(120) NOT NULL,
        description VARCHAR(500) DEFAULT '',
        price       INT          NOT NULL,
        tags        VARCHAR(200) DEFAULT '',
        emoji       VARCHAR(10)  DEFAULT '',
        available   TINYINT(1)   DEFAULT 1
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    conn.commit()

    # Seed menu only if empty
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        _seed_menu(cursor)
        conn.commit()
        print("Menu seeded into MySQL.")

    print("MySQL database ready.")
    cursor.close()
    conn.close()


def _seed_menu(cursor):
    menu = [
        ("hot",  "Espresso",             "Single origin shot — intense, syrupy, crema",          280, "STRONG",                "☕"),
        ("hot",  "Double Espresso",      "Two shots for those who mean business",                 380, "STRONG",                "☕"),
        ("hot",  "Flat White",           "Velvety microfoam over a double ristretto",             420, "CLASSIC",               "☕"),
        ("hot",  "Cappuccino",           "Equal parts espresso, steamed milk & foam",             390, "",                      "☕"),
        ("hot",  "Latte",                "Smooth espresso with steamed milk",                     420, "",                      "☕"),
        ("hot",  "Americano",            "Espresso & hot water — bold and clean",                 320, "",                      "☕"),
        ("hot",  "Cool Signature Hot",   "Cardamom espresso, caramel & milk foam",                520, "SIGNATURE,BESTSELLER",  "🌙"),
        ("hot",  "Dark Mocha",           "70% dark chocolate, espresso & steamed milk",           490, "RICH",                  "🍫"),
        ("cold", "Cold Brew",            "18-hour slow steep — smooth, low acid",                 480, "SMOOTH",                "🧊"),
        ("cold", "Nitro Cold Brew",      "Nitrogen-infused, creamy, zero sugar needed",           560, "SIGNATURE",             "🧊"),
        ("cold", "Iced Latte",           "Espresso over ice with cold milk",                      440, "",                      "🧋"),
        ("cold", "Iced Caramel Latte",   "Salted caramel, espresso, iced milk",                   490, "POPULAR",               "🧋"),
        ("cold", "Espresso Tonic",       "Chilled espresso, sparkling tonic, citrus",             510, "REFRESHING",            "🍊"),
        ("cold", "Cool Drift",           "Cold brew, tonic water, orange peel",                   540, "SIGNATURE,UNIQUE",      "🧋"),
        ("cold", "Very Vanilla Iced",    "House vanilla, cold milk, double espresso",             470, "BESTSELLER",            "🧋"),
        ("spec", "Cool Infinity",        "Double espresso, black sesame, vanilla cream swirl",    620, "FLAGSHIP,MUST TRY",     "∞"),
        ("spec", "Red Eye",              "Drip coffee + double espresso",                         550, "EXTRA STRONG",          "🔥"),
        ("spec", "Midnight Black",       "Activated charcoal latte, coconut milk, vanilla",       580, "UNIQUE",                "🌙"),
        ("spec", "Honey Lavender Latte", "Lavender syrup, raw honey, espresso, oat milk",         560, "FLORAL",                "🍯"),
        ("spec", "Blue Velvet",          "Butterfly pea cold brew, lemon, tonic",                 580, "INSTA-WORTHY",          "🫐"),
        ("spec", "Cortado Oscuro",       "Equal ristretto & warm dark chocolate milk",            490, "",                      "🍫"),
        ("mat",  "Matcha Latte",         "Ceremonial grade matcha, steamed oat milk",             490, "POPULAR",               "🍵"),
        ("mat",  "Iced Matcha",          "Cold oat milk, ceremonial matcha",                      510, "",                      "🍵"),
        ("mat",  "Dirty Matcha",         "Matcha latte with espresso shot on top",                550, "BESTSELLER",            "🍵"),
        ("mat",  "Peach Oolong",         "Cold-brewed oolong, peach syrup, sparkling water",      460, "",                      "🍑"),
        ("mat",  "Rose Chai",            "Karachi-style masala chai with dried rose petals",      380, "DESI LOVE",             "🌹"),
        ("food", "Butter Croissant",     "Flaky, layered, warm — baked fresh every morning",      280, "FRESHLY BAKED",         "🥐"),
        ("food", "Classic Waffles",      "Crispy outside, fluffy inside, maple syrup & butter",   590, "",                      "🧇"),
        ("food", "Nutella Waffles",      "Belgian waffle, warm Nutella, hazelnuts, berries",      680, "POPULAR",               "🧇"),
        ("food", "Club Sandwich",        "Grilled chicken, cheese, lettuce, tomato",              640, "",                      "🥪"),
        ("food", "Avocado Toast",        "Sourdough, smashed avo, chili flakes, poached egg",     720, "HEALTHY",               "🥑"),
        ("food", "Pancake Stack",        "3 fluffy pancakes, fresh fruit, honey drizzle",         620, "",                      "🥞"),
        ("dess", "Cool Black Forest",    "Dark chocolate layers, kirsch cream, fresh cherries",   490, "SIGNATURE",             "🎂"),
        ("dess", "NY Cheesecake",        "Dense, creamy, biscuit base, berry coulis",             450, "BESTSELLER",            "🍰"),
        ("dess", "Creme Brulee",         "Vanilla custard, torched sugar crust",                  520, "MUST TRY",              "🍮"),
        ("dess", "Lava Cake",            "Molten dark chocolate, vanilla ice cream",              560, "POPULAR",               "🍫"),
        ("dess", "Tiramisu",             "Espresso-soaked, mascarpone, cocoa dusting",            490, "",                      "🍰"),
        ("dess", "Warm Cookie",          "Double choc chip, freshly baked with cream",            320, "",                      "🍪"),
    ]
    cursor.executemany(
        "INSERT INTO menu_items (category, name, description, price, tags, emoji) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        menu
    )
