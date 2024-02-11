import sqlite3
import contextlib


def connection(db_f: str) -> None:
    try:
        conn = sqlite3.connect(db_f)
    finally:
        conn.close()


def accounts(db_f: str) -> None:
    sql_query = '''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password TEXT NOT NULL,
            email TEXT UNIQUE
        );
    '''

    with contextlib.closing(sqlite3.connect(db_f)) as conn:
        with conn:
            conn.execute(sql_query)


def notes(db_f: str) -> None:
    sql_query = '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            note TEXT,
            FOREIGN KEY (user_id) REFERENCES accounts(id)
        );
    '''

    with contextlib.closing(sqlite3.connect(db_f)) as conn:
        with conn:
            conn.execute(sql_query)


def login_attempts(db_f: str) -> None:
    sql_query = '''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address VARCHAR,
            attempts_left INTEGER
        );
    '''

    with contextlib.closing(sqlite3.connect(db_f)) as conn:
        with conn:
            conn.execute(sql_query)


def setup_database(db_f: str) -> None:
    connection(db_f)
    accounts(db_f)
    notes(db_f)
    login_attempts(db_f)
