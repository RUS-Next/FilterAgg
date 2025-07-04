from dataclasses import dataclass
from typing import Union

@dataclass
class FilterCondition:
    column: str
    operator: str
    value: Union[str, float]


@dataclass
class Aggregation:
    column: str
    operator: str