import os
import sqlite3
from .bb_dataclasses import Account
from toga.icons import Icon

_connection_singleton = None

DB_PATH = None
def set_path(path):
    global DB_PATH
    DB_PATH = path

def _conn():
    global _connection_singleton
    # Path to the database
    print(f'Database path: {DB_PATH}')
    if _connection_singleton is None:
        _connection_singleton = sqlite3.connect(DB_PATH)
    return _connection_singleton

def get_accounts() -> list[Account]:

    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance, last_updated, color FROM `account`")
    data = cursor.fetchall()
    accounts = [Account(*row) for row in data]
    return accounts

