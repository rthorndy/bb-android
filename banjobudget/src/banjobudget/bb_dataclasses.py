"""
Dataclasses that are useful in the project.
"""

from dataclasses import dataclass, asdict, is_dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from toga.icons import Icon

TZ_PT = ZoneInfo('America/Vancouver')

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        # Handle dataclasses
        if is_dataclass(o):
            return asdict(o)
        # Handle datetimes
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d")
        # Fall back to the default implementation for other types
        return super().default(o)
    

@dataclass
class Account:
    name: str
    balance: float
    last_updated: datetime
    color: str

    def __post_init__(self):
        """
        This method is called after the object is created.
        We can use it to clean up or convert data.
        """
        # If the value provided for last_updated was a string, convert it
        if isinstance(self.last_updated, str):
            self.last_updated = datetime.fromisoformat(self.last_updated)
            self.last_updated = self.last_updated.replace(tzinfo=TZ_PT)


    @staticmethod
    def for_detailed_list(items:list) -> list:
        """
        Returns a list of Account object data, suitable for a DetailedList widget.
        """
        return list( {'title' : acct.name, 'icon' : Icon(f'resources/icons/icon__{acct.color}_{acct.name[0]}'), 'subtitle' : acct.balance} for acct in items )


@dataclass
class Transaction:
    description: str
    amount: float
    date: datetime
    is_recurring: bool
    recurrence_rule: str
    account: str
    end_date: datetime = None

    def __post_init__(self):
        """
        Called after initialization to convert string dates into
        datetime objects.
        """
        # Convert the 'start' field if it's a string
        if isinstance(self.date, str):
            self.date = datetime.fromisoformat(self.date)
            self.date = self.date.replace(tzinfo=TZ_PT)

        # convert the is_recurring field
        self.is_recurring = bool(self.is_recurring)

        # Convert the 'end' field if it was provided as a string
        # This check naturally handles the 'None' case, as None is not a string.
        if isinstance(self.end_date, str):
            self.end_date = datetime.fromisoformat(self.end_date)
            self.end_date = self.end_date.replace(tzinfo=TZ_PT)
