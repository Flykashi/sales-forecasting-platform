import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'records.db'

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    store INTEGER,
    date TEXT,
    promo INTEGER,
    state_holiday TEXT,
    store_type TEXT,
    assortment TEXT,
    competition_distance REAL,
    promo2 INTEGER,
    prediction REAL,
    created_at TEXT
)
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()
    finally:
        conn.close()


def insert_record(record):
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO records (
                source, store, date, promo, state_holiday,
                store_type, assortment, competition_distance,
                promo2, prediction, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.get('source'),
                record.get('store'),
                record.get('date'),
                record.get('Promo'),
                record.get('StateHoliday'),
                record.get('StoreType'),
                record.get('Assortment'),
                record.get('CompetitionDistance'),
                record.get('Promo2'),
                record.get('prediction'),
                record.get('created_at'),
            )
        )
        conn.commit()
    finally:
        conn.close()
