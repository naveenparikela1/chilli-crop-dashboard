import sqlite3
from datetime import datetime

DB_NAME = "chillicrop.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        state TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS varieties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        avg_yield_qpa REAL,          -- quintals per acre
        avg_price REAL,              -- Rs per quintal
        color_value TEXT
    );

    CREATE TABLE IF NOT EXISTS yields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER,
        variety_id INTEGER,
        season TEXT,                 -- Rabi / Kharif
        year INTEGER,
        yield_qpa REAL,
        area_acres REAL,
        FOREIGN KEY (region_id) REFERENCES regions(id),
        FOREIGN KEY (variety_id) REFERENCES varieties(id)
    );

    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER,
        record_date TEXT,
        temperature REAL,
        humidity REAL,
        rainfall_mm REAL,
        FOREIGN KEY (region_id) REFERENCES regions(id)
    );

    CREATE TABLE IF NOT EXISTS pests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER,
        pest_name TEXT,
        risk_level TEXT,             -- Low / Medium / High / Critical
        affected_acres REAL,
        treatment TEXT,
        detected_on TEXT,
        FOREIGN KEY (region_id) REFERENCES regions(id)
    );

    CREATE TABLE IF NOT EXISTS market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variety_id INTEGER,
        mandi TEXT,
        record_date TEXT,
        price_min REAL,
        price_max REAL,
        price_modal REAL,
        FOREIGN KEY (variety_id) REFERENCES varieties(id)
    );

    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT,             -- weather / pest / market
        severity TEXT,
        message TEXT,
        created_at TEXT
    );
    """)
    conn.commit()
    conn.close()


def query(sql, params=()):
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized: chillicrop.db")
