"""
A budget tool for the rest of us
"""


import toga
from toga.widgets.detailedlist import DetailedList
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
import os


class BanjoBudget(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        On startup, display a list of account names from the database.
        """
        # Path to the database
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data", "banjo-budget.db")
        db_path = os.path.normpath(db_path)

        # Fetch account names from the database
        account_names = []
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM account;")
            account_names = [row[0] for row in cursor.fetchall()]
            conn.close()
        except Exception as e:
            account_names = [f"Error loading accounts: {e}"]

        # Create a List widget to display account names
        list_widget = DetailedList(data=[{"title" : account_name} for account_name in account_names], style=Pack(flex=1))
        main_box = toga.Box(children=[list_widget], style=Pack(direction=COLUMN, margin=10))

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BanjoBudget()
