from dataclasses import dataclass, field
from toga.icons import Icon

def default_account_icon():
    return Icon('resources/icons/account-default')
@dataclass
class Account:
    name: str = field(default_factory=str)
    balance: float = field(default_factory=float)
    last_updated: str = field(default_factory=str)
    icon: Icon

    @staticmethod
    def for_detailed_list(items:list) -> list:
        """
        Returns a list of Account object data, suitable for a DetailedList widget.
        """
        return list( {'title' : acct.name, 'icon' : acct.icon, 'subtitle' : acct.balance} for acct in items )
