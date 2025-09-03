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
import calendar
import daily


def create_daily_box(app):
    """
    The complex box that displays the details for a
    single day. Because of the complexity, we will offload
    this to a separate file.
    """
    return daily.create_daily_box(app)

def create_accounts_box(app):
    pass

def create_calendar_box(app):
    """
    The complex box that is the entire calendar widget. Due
    to the complexity, we will offload this to a separate file.
    """
    return calendar.create_calendar(app)

def create_app_header(app):
    """
    The main header bar, holding the app name, logo etc.
    Just a coloured bar with text.
    """
    pass