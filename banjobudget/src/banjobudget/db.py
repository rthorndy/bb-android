from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
import threading

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrulestr

from .bb_dataclasses import Account, Transaction

TZ_PT = ZoneInfo('America/Vancouver')

import asyncio.threads

STATE = {
    "conns": {},
    "db_path": None,
}

def set_path(path):
    STATE["db_path"] = path

def _conn():
    # Path to the database
    thread_id = threading.get_ident()

    if thread_id not in STATE["conns"]:
        STATE["conns"][thread_id] = sqlite3.connect(STATE["db_path"])

    return STATE["conns"][thread_id]

def get_accounts() -> list[Account]:

    conn = _conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance, last_updated, color FROM `account`")
    data = cursor.fetchall()
    accounts = [Account(*row) for row in data]
    return accounts

def get_transactions(start_date:datetime, end_date:datetime) -> list[Transaction]:

    start_date = datetime(start_date.year, start_date.month, start_date.day)
    end_date = datetime(end_date.year, end_date.month, end_date.day)

    conn = _conn()
    cursor = conn.cursor()

    # Step 1: get non-recurring transactions within the date
    cursor.execute("SELECT description, amount, date, is_recurring, recurrence_rule, account.name as account_name, end_date FROM `transaction` join account on `transaction`.account_id=account.id where date >= ? and date <= ? and is_recurring = 0", (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
    data = cursor.fetchall()
    transactions = [Transaction(*row) for row in data]

    # Step 2: get all recurring transactions within the date range. 
    # Create instances with fixed date for any that have occurrences within the
    # date range.
    cursor.execute("SELECT description, amount, date, is_recurring, recurrence_rule, account.name as account_name, end_date FROM `transaction` join account on `transaction`.account_id=account.id where is_recurring = 1")
    data = cursor.fetchall()
    for row in data:
        t = Transaction(*row)
        t.date = datetime(t.date.year, t.date.month, t.date.day)
        if t.end_date is not None:
            t.end_date = datetime(t.end_date.year, t.end_date.month, t.end_date.day)
        r_str = str(t.recurrence_rule)
        r_end = end_date if t.end_date is None else min(t.end_date, end_date)
        r = rrulestr(r_str, dtstart=t.date, forceset=True, ignoretz=True)
        # if start_date.year == 2025 and start_date.month==11 and start_date.day == 26:
        #     print (f'{t.date}, {r_str}, {r_end}, {len(r.between(start_date, r_end, inc=True))}')
        for dt in r.between(start_date, r_end, inc=True):
            transactions.append(
                Transaction(
                    description = t.description,
                    amount = t.amount,
                    date = dt.replace(tzinfo=TZ_PT),
                    is_recurring = t.is_recurring,
                    recurrence_rule = t.recurrence_rule,
                    account = t.account,
                    end_date = t.end_date.replace(tzinfo=TZ_PT) if t.end_date is not None else None
                )
            )
    return sorted(transactions, key = lambda t: t.date)


def load_data(data):
    """
    Blocking data computation/loading. 
    Will take over from data['loaded_up_to']
    """
    accounts = data['accounts']
    if 'loaded_up_to' not in data or data['loaded_up_to'] is None:
        start_date = min(acct.last_updated for acct in accounts)
    else:
        start_date = datetime.fromisoformat(data['loaded_up_to'])
        start_date = start_date.replace(tzinfo=TZ_PT)
        start_date += relativedelta(days=1)

    # Step 1: process forward to set transactions and account balances
    end_date = start_date + relativedelta(months=3)
    transactions = get_transactions(start_date, end_date)

    # print('Transactions:')
    # for t in transactions:
    #     print(f'{t.description} ({t.date.strftime("%Y-%m-%d")})')

    current_date = datetime(start_date.year, start_date.month, start_date.day, tzinfo=TZ_PT)
    t_index = 0
    yesterday = None
    while current_date <= end_date:
        key = date_key(current_date)
        if key not in data:
            if yesterday is None:
                yesterday_accounts = { acct.name : 0.00 for acct in accounts }
            else:
                yesterday_accounts = data[yesterday]['balances']
            
            data[key] = {
                'transactions' : [],
                'balances' : dict(yesterday_accounts),
                'eod' : dict(yesterday_accounts),
                'spendable' : {}
            }

        # if any account has this as its last_updated date, set the day's 
        # starting account balance to the account's balance value.
        for acct in accounts:
            if date_key(acct.last_updated) == key:
                data[key]['balances'][acct.name] = acct.balance

        # Find the index of the first transaction with today's date. It may end before
        # today's date, which is fine, because we'll catch up to it with the current_date
        # loop eventually.
        while t_index < len(transactions) and transactions[t_index].date < current_date:
            t_index += 1

        # If the transaction date at t_index is EQUAL to today, we include it in today's
        # array and update the appropriate account. Repeat until t_index points to the
        # future.
        while t_index < len(transactions) and transactions[t_index].date == current_date:
            t = transactions[t_index]
            data[key]['transactions'].append(t)
            data[key]['balances'][t.account] += t.amount
            data[key]['eod'][t.account] += t.amount

            t_index += 1

        yesterday = key
        current_date += relativedelta(days=1)

    # Step 2: work backwards to establish the maximum spendable in each account.
    current_date = end_date - relativedelta(days=1)
    key = date_key(end_date)
    data[key]["spendable"] = dict(data[key]["balances"])
    for acct in accounts:
        data[key]["spendable"][acct.name] = data[key]["eod"][acct.name]
    tomorrow = key
    while current_date >= start_date:
        key = date_key(current_date)
        for acct in accounts:
            data[key]["spendable"][acct.name] = min(
                data[tomorrow]["spendable"][acct.name],
                data[key]["eod"][acct.name]
            )

        tomorrow = key
        current_date -= relativedelta(days=1)

    data["loaded_up_to"] = end_date.strftime("%Y-%m-%d")

async def async_load_data(data):
    """
    Async wrapper to load data up to the given datetime. Implemented by offloading
    the blocking load_data to a thread so callers can await it.
    """
    if data is None:
        return None
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, load_data, data)

def date_key(dt:datetime) -> str:
    return dt.strftime("%Y-%m-%d")