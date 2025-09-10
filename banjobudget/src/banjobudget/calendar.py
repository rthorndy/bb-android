"""
A file to hold all functions that build the main calendar
display.
"""
import random
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from toga.style import Pack
from toga.widgets.box import Column, Row
from toga.widgets.button import Button
from toga.widgets.label import Label
from banjobudget.day_canvas import DayCanvas

TZ_PT = ZoneInfo('America/Vancouver')

# Centralized mutable state (avoids global statements)
_state = {
    'current_month': None,
    'month_label': None,
    'day_boxes_cache': {},
    'calendar_box': None,
}


def create_calendar_box(dt):
    _state['current_month'] = dt.replace(day=1)
    header = create_header()
    day_boxes =  create_day_boxes(dt)
    _state['calendar_box'] = Column(style=Pack(background_color="white"), children=[header, day_boxes])
    _state['day_boxes_cache'][(dt.year, dt.month)] = day_boxes
    return _state['calendar_box']

def create_header():
    _state['month_label'] = Label(text = _state['current_month'].strftime("%B %Y"), style=Pack(text_align="center", flex=8))
    header = Row(children=[
        Button(text = "<", style=Pack(flex = 1, text_align="left"), on_press=left_button_press),
        _state['month_label'],
        Button(text = ">", style=Pack(flex = 1, text_align="right"), on_press=right_button_press)
    ], style=Pack(justify_content="start", background_color="lightblue", color="black", font_size=20))

    return header

def create_day_box(dt):
    today = datetime.now(tz = TZ_PT)
    is_today = (dt.day == today.day and dt.month == today.month)
    is_month = (dt.month == _state['current_month'].month)

    # Use the custom DayCanvas to render the four-row day cell
    canvas = DayCanvas(
        day=str(dt.day),
        has_income=random.random() < 0.5,
        has_expense=random.random() < 0.5,
        cash="$cash",
        spendable="$spend",
        is_today = is_today,
        is_month = is_month
    )
    canvas.on_press = select_day
    canvas.style = Pack(flex=1)
    canvas.on_resize = on_resize
    return canvas

def on_resize(widget, width, height, **kwargs):
    widget.draw(width)
    return widget

def select_day(widget:DayCanvas, *args, **kwargs):
    print(f'Clicked: {widget}, {args}, {kwargs}, {widget.day}')
    return widget

def create_day_row(dt):
    return [ create_day_box(dt + timedelta(days = t)) for t in range(7) ]


def create_day_boxes(month_dt):
    rows = []
    start_date = month_dt.replace(day=1)
    _state['current_month'] = start_date

    while start_date.weekday() != 6:
        start_date -= timedelta(days=1)

    while (start_date.year, start_date.month) <= (month_dt.year, month_dt.month):
        row = Row(children = create_day_row(start_date), style=Pack(background_color="white", gap=2, flex=1, height=60))
        rows.append(row)
        start_date += timedelta(days=7)

    day_boxes = Column(style=Pack(gap=2, background_color="white"), children = rows, flex=1)
    return day_boxes


def redraw_day_boxes():
    day_boxes = _state['calendar_box'].children[1].children
    for row in day_boxes:
        for canvas in row:
            canvas.redraw()

    return day_boxes

def left_button_press(widget):
    update_calendar(_state['current_month'] - relativedelta(months=1))
    return widget
    
def right_button_press(widget):
    update_calendar(_state['current_month'] + relativedelta(months=1))
    return widget

def update_calendar(new_month):
    print(f'Update from {_state["current_month"].strftime("%B %Y")} to {new_month.strftime("%B %Y")}')
    old_dt = datetime(_state['current_month'].year, _state['current_month'].month, 1)
    old_day_boxes = _state['calendar_box'].children[1]
    if (new_month.year, new_month.month) not in _state['day_boxes_cache']:
        new_day_boxes = create_day_boxes(new_month)
        _state['day_boxes_cache'][(new_month.year, new_month.month)] = new_day_boxes
    else:
        new_day_boxes = _state['day_boxes_cache'][(new_month.year, new_month.month)]

    _state['current_month'] = new_month.replace(day=1)
    print(f'Before: {old_dt.strftime("%B %Y")}')
    print(f'\tCalendar: {_state["calendar_box"].children}')
    print(f'\tOld Boxes: {old_day_boxes}')
    _state['calendar_box'].replace(old_day_boxes, new_day_boxes)
    _state['month_label'].text = new_month.strftime("%B %Y")
    print()
    print(f'After: {new_month.strftime("%B %Y")}')
    print(f'\tCalendar: {_state["calendar_box"].children}')
    print(f'\tNew Boxes: {new_day_boxes}')
    print('-' * 20)
    #redraw_day_boxes()
