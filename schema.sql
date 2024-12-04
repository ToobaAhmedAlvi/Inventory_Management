-- schema.sql: Database schema for the Flask app

-- User details table
CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    price REAL NOT NULL,
    vendor_name TEXT NOT NULL,
    date_added DATE NOT NULL,
    quantity INTEGER NOT NULL
);
