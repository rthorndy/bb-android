from toga.widgets.box import Box
from toga.widgets.box import Column, Row
from toga.widgets.button import Button
from toga.widgets.label import Label
from toga.style import Pack
from toga.widgets.dateinput import DateInput
from toga.widgets.detailedlist import DetailedList
from toga.widgets.divider import Divider
from toga.widgets.switch import Switch
from toga.widgets.scrollcontainer import ScrollContainer
from toga.widgets.textinput import TextInput
from toga.widgets.imageview import ImageView
from toga.widgets.numberinput import NumberInput
from toga.widgets.selection import Selection
from toga.icons import Icon
from toga.images import Image
from . import calendar
from . import daily
from . import db
from .bb_dataclasses import Account


def create_accounts_box(app):
    header = Box(children=[Label('Accounts')])
    accounts = db.get_accounts()
    accounts_list = Row(children = [ create_account_box(app, acct) for acct in accounts ])
    scroller = ScrollContainer(horizontal = True, vertical = False, content=accounts_list)
    return Box(children=[header, scroller], style=Pack(direction="column", flex=1))

def create_account_box(app, acct:Account):
    data_box = Column(children = [ Label(text=acct.name), Label(text=acct.balance) ])
    image = Image(app.paths.app / f'resources/icons/icon__{acct.color}_{acct.name[0]}.png')
    return Row(children=[ImageView(image), data_box], style=Pack(width=200, height=50, margin=9))