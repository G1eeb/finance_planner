"""Подключение к базе данных SQLite."""

import sqlite3

DB_PATH = "data/finance_planner.sqlite"


def get_connection():
    """Создать соединение с базой и включить проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
