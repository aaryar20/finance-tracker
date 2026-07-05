import os
import sqlite3

from config import DB_NAME


def get_connection():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_NAME)

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # ---------------- Users ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- Transactions ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        date TEXT NOT NULL,

        type TEXT NOT NULL,

        category TEXT NOT NULL,

        amount REAL NOT NULL,

        description TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    # ---------------- Budget ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE NOT NULL,

        monthly_budget REAL DEFAULT 0,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    # ---------------- Savings Goals ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savings_goals(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE NOT NULL,

        goal_name TEXT,

        target_amount REAL,

        current_amount REAL,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    # ---------------- Categories ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        name TEXT NOT NULL,

        UNIQUE(user_id,name),

        FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":

    initialize_database()

    print("Database initialized.")