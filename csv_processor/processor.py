import csv
from typing import Dict, List, Optional, Union
from .models import FilterCondition, Aggregation
from .exceptions import InvalidOperatorError, InvalidAggregateError, InvalidColumnError


class CSVProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self._read_csv()

    def _read_csv(self):
        with open(self.file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return [row for row in csv_reader]

    def _apply_filter(self, condition: FilterCondition) -> List[Dict[str, str]]:
        filtered_data = []
        operators = {
            '>' : lambda a, b: a > b,
            '<' : lambda a, b: a < b,
            '>=' : lambda a, b: a >= b,
            '<=' : lambda a, b: a <= b,
            '=' : lambda a, b: a == b,
        }

        if condition.operator not in operators:
            raise InvalidOperatorError(f'Invalid operator: {condition.operator}')

        for row in self.data:
            try:
                row_value = float(row[condition.column])
                condition_value = float(condition.value)
                compare = operators[condition.operator]
                if compare(row_value, condition_value):
                    filtered_data.append(row)
            except ValueError:
                compare = operators[condition.operator]
                condition_value = str(condition.value)
                if compare(row[condition.column], str(condition_value)):
                    filtered_data.append(row)

        return filtered_data

    def _apply_aggregation(
            self,
            data: List[Dict[str, str]],
            aggregation: Aggregation
    ) -> Dict[str, float]:
        if aggregation.column not in data[0].keys():
            raise InvalidColumnError(f'Invalid column: {aggregation.column}')

        try:
            values = [float(row[aggregation.column]) for row in data]
        except ValueError:
            raise InvalidColumnError(f'Invalid aggregation: column {aggregation.column} has no numeric value')

        operations = {
            'avg' : lambda a: sum(a) / len(a),
            'min' : min,
            'max' : max,
        }

        if aggregation.operator not in operations:
            raise InvalidAggregateError(f'Invalid operator: {aggregation.operator}')

        result = operations[aggregation.operator](values)
        return {aggregation.operator: result}

    def process(
            self,
            filter_condition: Optional[FilterCondition] = None,
            aggregation: Optional[Aggregation] = None,
    ) -> Union[List[Dict[str, str]], Dict[str, float]]:
        data = self.data if filter_condition is None else self._apply_filter(filter_condition)

        if aggregation:
            return self._apply_aggregation(data, aggregation)

        return data


