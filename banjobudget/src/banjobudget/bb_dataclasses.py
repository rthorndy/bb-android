"""
Dataclasses that are useful in the project.
"""

from dataclasses import dataclass, field
from toga.icons import Icon

@dataclass
class Account:
    name: str = field(default_factory=str)
    balance: float = field(default_factory=float)
    last_updated: str = field(default_factory=str)
    color: str = field(default_factory=str)

    @staticmethod
    def for_detailed_list(items:list) -> list:
        """
        Returns a list of Account object data, suitable for a DetailedList widget.
        """
        return list( {'title' : acct.name, 'icon' : Icon(f'resources/icons/icon__{acct.color}_{acct.name[0]}'), 'subtitle' : acct.balance} for acct in items )

