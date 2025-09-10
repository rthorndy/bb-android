"""
The complex widget that displays the details for a single day.
This includes all expenses and income, and bank account
balances and spendables.
"""
from datetime import datetime
from zoneinfo import ZoneInfo
from toga.widgets.box import Column, Row
from toga.widgets.label import Label
from toga.style import Pack

TZ_PT = ZoneInfo('America/Vancouver')

data = {
    "date" : datetime(2025, 9, 17, tzinfo=TZ_PT),
    "transactions":
    [
        {"description" : "Expense 1", "amount" : -100, "account" : "RBC"},
        {"description" : "Expense 2", "amount" : -150, "account" : "RBC"},
        {"description" : "Expense 3", "amount" : -200, "account" : "RBC"},
        {"description" : "Expense 4", "amount" : -35, "account" : "RBC"},
        {"description" : "Expense 5", "amount" : -42, "account" : "Koho"},
        {"description" : "Expense 6", "amount" : -120, "account" : "Koho"},
        {"description" : "Income 1", "amount" : 1500, "account" : "RBC"}
    ],
    "balances":
    {
        "RBC": 1000,
        "Koho" : 500,
        "Cash" : 50
    },
    "spendable":
    {
        "RBC": 50,
        "Koho" : 0,
        "Cash" : 0
    },
}

def create_daily_box():
    header = Column(children=[Label(text = data["date"].isoformat(), style=Pack(text_align="center"))], style=Pack(justify_content="end", background_color="lightblue", color="black", font_size=20))
    content = Column(style=Pack(gap = 20))
    transactions = Row(style=Pack(gap=20))
    accounts = Row(style=Pack(gap=20))
    content.add(transactions)
    content.add(accounts)

    expenses = Column(children=[Label(text = "Expenses", style=Pack(text_align="right"))])
    income = Column(children=[Label(text = "Income", style=Pack(text_align="right"))])

    new_balances = dict(data["balances"])

    for t in data["transactions"]:
        if t["amount"] < 0:
            expenses.add(Label(text = f'{t["description"]} ${-t["amount"]}'))
        else:
            income.add(Label(text = f'{t["description"]} ${t["amount"]}'))
        new_balances[t["account"]] += t["amount"]

    transactions.add(expenses)
    transactions.add(income)

    names = Column(children = [Label(text = "", style=Pack(text_align="left"))] + [Label(text = name, style=Pack(text_align="left")) for name in data["balances"].keys()])
    accounts.add(names)

    balances = Column(children = [Label(text = "Balance", style=Pack(text_align="right"))])
    spendables = Column(children = [Label(text = "Spendable", style=Pack(text_align="right"))])
    for acct, balance in new_balances.items():
        balances.add(Label(text = f'${balance}'))
        spendables.add(Label(text = f'${data["spendable"][acct]}'))
    accounts.add(balances)
    accounts.add(spendables)

    return Column(children=[header, content], style=Pack(flex=1, background_color = "white", gap=20))