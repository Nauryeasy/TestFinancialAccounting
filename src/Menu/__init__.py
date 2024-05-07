from typing import Type

from .BaseMenuItem import BaseMenuItem
from .GetBalance import GetBalance
from .AddReport import AddReport
from .CorrectReport import CorrectReport
from .FindReports import FindReports


def get_menu() -> list[Type[BaseMenuItem]]:
    return BaseMenuItem.__subclasses__()
