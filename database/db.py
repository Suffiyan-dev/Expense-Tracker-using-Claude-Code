import sqlite3
import os

DB_PATH = "spendly.db"

def get_db():
    """
    Returns a SQLite connection with row_factory and foreign keys enabled.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates all tables using CREATE TABLE IF NOT EXISTS.
    """
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

def seed_db():
    """
    Inserts sample data for development.
    """
    with get_db() as conn:
        # Sample Users
        users = [
            ('testuser', 'hashed_password_123', 'test@example.com'),
            ('demo_user', 'hashed_password_456', 'demo@example.com')
        ]

        cursor = conn.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO users (username, password, email) VALUES (?, ?, ?)",
            users
        )

        # Get user IDs for seeding expenses
        cursor.execute("SELECT id, username FROM users")
        user_map = {row['username']: row['id'] for row in cursor.fetchall()}

        # Sample Expenses
        expenses = [
            (user_map['testuser'], 12.50, 'Food', 'Lunch at Deli', '2023-10-01'),
            (user_map['testuser'], 45.00, 'Transport', 'Gas fill-up', '2023-10-02'),
            (user_map['demo_user'], 120.00, 'Utilities', 'Electricity Bill', '2023-10-01'),
            (user_map['demo_user'], 8.00, 'Food', 'Coffee', '2023-10-03'),
        ]

        cursor.executemany(
            "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
            expenses
        )

        conn.commit()
