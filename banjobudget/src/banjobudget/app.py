"""
A budget tool for the rest of us
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import ui


class BanjoBudget(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        On startup, display a list of account names from the database.
        """
        main_box = toga.Box(
            children=[ui.create_app_header(self), ui.create_accounts_box(self), ui.create_calendar_box(self), ui.create_daily_box(self)],
            style=Pack(direction=COLUMN, margin=20, flex=1)
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BanjoBudget()
