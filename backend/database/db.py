import sqlite3
from pathlib import Path

# Project directories
DATABASE_DIR = Path(__file__).parent
DATABASE_FILE = DATABASE_DIR / "edr.db"
SCHEMA_FILE = DATABASE_DIR / "schema.sql"


def get_connection():
    """
    Create and return a SQLite connection.
    Foreign keys are enabled automatically.
    """
    conn = sqlite3.connect(DATABASE_FILE)

    # Access columns by name
    conn.row_factory = sqlite3.Row

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def initialize_database():
    """
    Creates the database tables if they don't exist.
    """
    conn = get_connection()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema:
        conn.executescript(schema.read())

    conn.commit()
    conn.close()

    print("Database initialized successfully")
