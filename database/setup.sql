-- ════════════════════════════════════════════════════
--   COOL COFFEE BAR — MySQL Setup
--   Run this entire file in MySQL Workbench FIRST
--   Then update environment variables before deployment
-- ════════════════════════════════════════════════════

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS cool_coffee
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cool_coffee;

-- Step 2: Users table
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(120)  NOT NULL,
    email         VARCHAR(180)  NOT NULL UNIQUE,
    password_hash VARCHAR(64)   NOT NULL,
    phone         VARCHAR(30)   DEFAULT '',
    created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Step 3: Orders table
CREATE TABLE IF NOT EXISTS orders (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT             NOT NULL,
    branch      VARCHAR(80)     NOT NULL DEFAULT 'Phase 8',
    items_json  TEXT            NOT NULL,
    total       DECIMAL(10,2)   NOT NULL DEFAULT 0,
    notes       TEXT            DEFAULT '',
    status      VARCHAR(30)     DEFAULT 'pending',
    created_at  DATETIME        DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Step 4: Contact submissions table
CREATE TABLE IF NOT EXISTS contact_submissions (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(120)  NOT NULL,
    email      VARCHAR(180)  NOT NULL,
    subject    VARCHAR(220)  DEFAULT '',
    message    TEXT          NOT NULL,
    is_read    TINYINT(1)    DEFAULT 0,
    created_at DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Step 5: Menu items table
CREATE TABLE IF NOT EXISTS menu_items (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    category    VARCHAR(30)   NOT NULL,
    name        VARCHAR(120)  NOT NULL,
    description TEXT          DEFAULT '',
    price       INT           NOT NULL,
    tags        VARCHAR(200)  DEFAULT '',
    emoji       VARCHAR(10)   DEFAULT '☕',
    available   TINYINT(1)    DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ════════════════════════════════════════
--   USEFUL QUERIES FOR WORKBENCH
-- ════════════════════════════════════════

-- View all users:
-- SELECT * FROM users;

-- View all orders with customer name:
-- SELECT o.id, u.name, o.branch, o.total, o.status, o.created_at
-- FROM orders o JOIN users u ON o.user_id = u.id
-- ORDER BY o.created_at DESC;

-- View all contact messages:
-- SELECT * FROM contact_submissions ORDER BY created_at DESC;

-- View full menu:
-- SELECT * FROM menu_items ORDER BY category, price;

-- Update order status to 'ready':
-- UPDATE orders SET status = 'ready' WHERE id = 1;

-- Total revenue:
-- SELECT SUM(total) AS total_revenue FROM orders;

-- Most ordered branch:
-- SELECT branch, COUNT(*) AS orders FROM orders GROUP BY branch;
