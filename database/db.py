# database/db.py

import sqlite3


# ==========================
# Create Database Connection
# ==========================

def get_db_connection():

    conn = sqlite3.connect("ai_interview.db")

    conn.row_factory = sqlite3.Row

    return conn


# ==========================
# Create Tables (Run Once)
# ==========================

def create_tables():

    conn = sqlite3.connect("ai_interview.db")

    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
    """)

    # Results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        score INTEGER
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()


# ==========================
# Run Database Setup
# ==========================

if __name__ == "__main__":

    create_tables()

    print("Database and tables created successfully!")