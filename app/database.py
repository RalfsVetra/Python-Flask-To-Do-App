import sqlite3
import contextlib


def c_connection(db_f: str) -> None:
    try:
        conn = sqlite3.connect(db_f)
    finally:
        conn.close()


def c_table(db_f: str) -> None:
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


def c_table_n(db_f: str) -> None:
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


def c_table_a(db_f: str) -> None:
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


def s_database(db_f: str) -> None:
    c_connection(db_f)
    c_table(db_f)
    c_table_n(db_f)
    c_table_a(db_f)
