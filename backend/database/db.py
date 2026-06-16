from contextlib import contextmanager
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "soc_edr.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def get_cursor():
    connection = get_connection()
    try:
        yield connection.cursor()
        connection.commit()
    finally:
        connection.close()