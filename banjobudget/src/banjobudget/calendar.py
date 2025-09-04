"""
A file to hold all functions that build the main calendar
display.
"""
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from toga.style import Pack
from toga.widgets.box import Column, Row
from toga.widgets.label import Label

TZ_PT = ZoneInfo('America/Vancouver')


def create_calendar_box():
    today = datetime.now(tz=TZ_PT)
    start_date = today.replace(day=1)
    while start_date.weekday() != 6:
        start_date -= timedelta(days=1)
    
    header = Column(children=[Label(text = today.strftime("%B %Y"), style=Pack(text_align="center"))], style=Pack(justify_content="end", background_color="lightblue", color="black", font_size=20))

    calendar = Column(style=Pack(gap=2, background_color="white"))
    while start_date.month <= today.month:
        row = Row(children=[ create_day_box(start_date + timedelta(days=t)) for t in range(7)], style=Pack(background_color="white", gap=2))
        calendar.add(row)
        start_date += timedelta(days=7)

    return Column(style=Pack(background_color="white"), children=[header, calendar])

def create_day_box(dt):
    today = datetime.now(tz = TZ_PT)
    is_today = (dt.day == today.day and dt.month == today.month)
    is_month = (dt.month == today.month)
    return Column(style=Pack(width="75", background_color='lightyellow' if is_today else 'lightgray'), children=[
        Label(text = f'{dt.day}', style=Pack(text_align="right", width="75", flex=1, font_size=8, color='black' if is_month else 'gray')),
        Label(text = 'dots', style=Pack(text_align="center", width="75", flex=1, font_size=8, color='black' if is_month else 'gray')),
        Label(text = '$cash', style=Pack(text_align="left", width="75", flex=1, font_size=8, color='black' if is_month else 'gray')),
        Label(text = '$spendable', style=Pack(text_align="left", width="75", flex=1, font_size=8, color='black' if is_month else 'gray'))
    ])