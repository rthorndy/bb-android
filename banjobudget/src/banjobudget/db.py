import os
import sqlite3
from bb_dataclasses import Account

_connection_singleton = None

def _conn():
    global _connection_singleton
    # Path to the database
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "..", "data", "banjo-budget.db")
    db_path = os.path.normpath(db_path)
    if _connection_singleton is None:
        _connection_singleton = sqlite3.connect(db_path)
    return _connection_singleton

def get_accounts():

    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance, last_updated FROM `account`")
    data = cursor.fetchall()
    accounts = [Account(*row) for row in data]
    # print(accounts)
    return accounts

