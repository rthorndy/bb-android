"""
The complex widget that displays the details for a single day.
This includes all expenses and income, and bank account
balances and spendables.
"""
from toga.widgets.box import Box, Column, Row
from toga.widgets.button import Button
from toga.widgets.label import Label
from toga.style import Pack


def create_daily_box():
    return Box(style=Pack(background_color='green', flex=15))