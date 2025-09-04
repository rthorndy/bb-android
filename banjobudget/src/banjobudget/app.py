"""
A budget tool for the rest of us
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.widgets.scrollcontainer import ScrollContainer
from toga.widgets.box import Box, Column, Row
from toga.window import Window
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
        scroller = ScrollContainer(horizontal=False, vertical=True, content=cal_daily)
        
        accounts_box = accounts.create_accounts_box(self)

        main_box = toga.Box(
            children=[accounts_box, scroller],
            style=Pack(direction=COLUMN, margin=20, gap = 20)
        )

        self.main_window = Window(content=main_box)
        (width, height) = self.main_window.size
        print(f'Window size: {width}x{height}')
        scroller.style.height = height - int(accounts_box.style.height)

        # self.main_window = toga.MainWindow(title=self.formal_name)
        # self.main_window.content = main_box
        self.main_window.show()


def main():
    toga.Widget.DEBUG_LAYOUT_ENABLED = True
    return BanjoBudget()
