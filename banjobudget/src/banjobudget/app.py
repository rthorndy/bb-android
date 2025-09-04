"""
A budget tool for the rest of us
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.widgets.scrollcontainer import ScrollContainer
from toga.widgets.box import Box, Column, Row
from . import accounts
from . import db
from . import calendar
from . import daily


class BanjoBudget(toga.App):
    def startup(self):
        """Construct and show the Toga application.
        On startup, display a list of account names from the database.
        """
        db.set_path(self.paths.app / 'resources/db/banjo-budget.db')

        cal_daily = Column(children=[calendar.create_calendar_box(), daily.create_daily_box()])
        scroller = ScrollContainer(horizontal=False, vertical=True, content=cal_daily, style=Pack(flex=10))
        
        main_box = toga.Box(
            children=[accounts.create_accounts_box(self), scroller],
            style=Pack(direction=COLUMN, margin=20, flex=1)
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BanjoBudget()
