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


        # Simulate dividers by alternating row background colors
        detailed_data = []
        for idx, account_name in enumerate(account_names):
            # Alternate background color for divider effect
            bg_color = "#f8f8f8" if idx % 2 == 0 else "#e0e0e0"
            detailed_data.append({"title": account_name, "style": Pack(background_color=bg_color)})

        # Create a DetailedList with border and drop shadow on the container
        list_container = toga.Box(
            children=[
                DetailedList(
                    data=[{"title": account_name} for account_name in account_names],
                    style=Pack(flex=1)
                )
            ],
            style=Pack(
                flex=1,
                padding=8,
                background_color="#ffffff"
            )
        )
        main_box = toga.Box(children=[list_container], style=Pack(direction=COLUMN, margin=20, flex=1))

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BanjoBudget()
