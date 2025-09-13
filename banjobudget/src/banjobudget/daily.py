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

_boxes = {
    "header_label" : None,
    "expenses" : None,
    "income" : None,
    "names" : None,
    "balances" : None,
    "spendables" : None
}

def create_daily_box():
    _boxes["header_label"] = Label(text="Today", style=Pack(text_align="center"))
    header = Column(children=[_boxes["header_label"]], style=Pack(justify_content="end", background_color="lightblue", color="black", font_size=20))
    content = Column(style=Pack(gap = 20))
    transactions = Row(style=Pack(gap=20))
    accounts = Row(style=Pack(gap=20))
    content.add(transactions)
    content.add(accounts)

    _boxes["expenses"] = Column(style=Pack(flex=1), children=[Label(text = "Expenses", style=Pack(text_align="left"))])
    _boxes["income"] = Column(style=Pack(flex=1),children=[Label(text = "Income", style=Pack(text_align="left"))])


    transactions.add(_boxes["expenses"])
    transactions.add(_boxes["income"])

    _boxes["names"] = Column(children = [Label(text = "", style=Pack(text_align="left"))] + [Label(text = name, style=Pack(text_align="left")) for name in data["balances"].keys()])
    accounts.add(_boxes["names"])

    _boxes["balances"] = Column(children = [Label(text = "Balance", style=Pack(text_align="right"))])
    _boxes["spendables"] = Column(children = [Label(text = "Spendable", style=Pack(text_align="right"))])
    accounts.add(_boxes["balances"])
    accounts.add(_boxes["spendables"])

    return Column(children=[header, content], style=Pack(flex=1, background_color = "white", gap=20))

def update_daily_box(dt:str, data:dict):

    # Set the header with the date
    _boxes["header_label"].text = dt.strftime("%B %d, %Y")


    # Set the expense and income lists.
    _boxes["expenses"].clear()
    _boxes["income"].clear()
    _boxes["expenses"].add(Label(text = "Expenses", style=Pack(flex=1, text_align="left")))
    _boxes["income"].add(Label(text = "Income", style=Pack(flex=1, text_align="left")))
    for t in data['transactions']:
        label = Label(text = f'${t.amount:0.2f} - {t.description}', style=Pack(text_align="left"))
        if t.amount < 0.00:
            _boxes["expenses"].add(label)
        else:
            _boxes["income"].add(label)

    # Fill in the account summary section
    _boxes["names"].clear()
    _boxes["names"].add(Label(text = "", style=Pack(text_align="left")))
    _boxes["balances"].clear()
    _boxes["spendables"].clear()
    _boxes["balances"].add(Label(text = "Balance", style=Pack(text_align="right")))
    _boxes["spendables"].add(Label(text = "Spendable", style=Pack(text_align="right")))
    for name in data['balances'].keys():
        _boxes["names"].add(Label(text = name, style=Pack(text_align="left")))

    for balance in data['balances'].values():
        _boxes["balances"].add(Label(text = f'${balance:0.2f}', style=Pack(text_align="right")))

    for spendable in data['spendable'].values():
        _boxes["spendables"].add(Label(text = f'${spendable:0.2f}', style=Pack(text_align="right")))

