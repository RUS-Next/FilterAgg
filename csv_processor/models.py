from dataclasses import dataclass
from typing import Union

@dataclass
class FilterCondition:
    column: str
    operator: str
    value: Union[str, float]


@dataclass
class Agregation:
    column: str
    operator: str