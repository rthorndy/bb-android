"""
A budget tool for the rest of us
"""
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Optional
import json

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.widgets.scrollcontainer import ScrollContainer
from toga.widgets.box import Box, Column
from toga.window import Window
from dateutil.relativedelta import relativedelta

from . import accounts
from . import db
from . import calendar
from . import daily
from .bb_dataclasses import DateTimeEncoder

TZ_DT = ZoneInfo("America/Vancouver")


class BanjoBudget(toga.App):
    # Predeclare commonly assigned attributes
    data: Optional[dict[str, Any]] = {}
    main_window: Optional[Window] = None
    load_future_chunks: Optional[bool] = False
    daily_box: Optional[Box] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_running = self._load_future_chunks

    def startup(self):
        """Construct and show the Toga application.
        On startup, display a list of account names from the database.
        """
        json_path = self.paths.data / 'data.json'
        if not json_path.exists():
            db_path = self.paths.data / "banjo-budget.db"
            if not db_path.exists():
                source_path = self.paths.app / "resources/db/banjo-budget.db"

                # copy file at db_path to self.paths.data / 'banjo-budget.db'
                with open(source_path, "rb") as src:
                    with open(db_path, "wb") as dst:
                        dst.write(src.read())
                print(f'Copied {source_path} to {db_path}')

                db.set_path(db_path)
                self.data = {
                    "daily" : {},
                    "accounts": { 'Cash Account' : 0.00 },
                    "loaded_up_to": (datetime.now(tz=TZ_DT) + relativedelta(months=3)).strftime("%Y-%m-%d")
                }
            else:
                print(f'Using existing DATABASE {db_path}')
                db.set_path(db_path)
                self.data['accounts'] = db.get_accounts()
                self.data['loaded_up_to'] = None
                db.load_data(self.data)  # blocking data computation
                self.load_future_chunks = True
        else:
            print(f'Using existing JSON {json_path}')
            db.set_path(json_path)
            with open(json_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)


        self.daily_box = daily.create_daily_box()
        cal_daily = Column(
            children=[
                calendar.create_calendar_box(datetime.now(tz=TZ_DT)),
                self.daily_box,
            ]
        )
        self.scroller = ScrollContainer(horizontal=False, vertical=True, content=cal_daily, style=Pack(flex=1))

        self.accounts_box = accounts.create_accounts_box(self)

        main_box = Box(
            children=[self.accounts_box, self.scroller],
            style=Pack(direction=COLUMN, margin=20, gap=20),
        )

        self.main_window = Window(content=main_box)

        # self.main_window = toga.MainWindow(title=self.formal_name)
        # self.main_window.content = main_box
        self.main_window.show()

    async def _load_future_chunks(self, widget, steps: int = 11):
        """
        Sets the size of the scroll contaner once the window size is established.
        Then loads and processes 2 years of database transaction data, if needed. 
        """
        _, window_height = self.main_window.size
        self.scroller.height = window_height - self.accounts_box.style.height

        if not self.load_future_chunks:
            return

        for _ in range(steps):
            await db.async_load_data(widget.data)

        return widget



def main():
    toga.Widget.DEBUG_LAYOUT_ENABLED = "--test" in sys.argv
    return BanjoBudget()
