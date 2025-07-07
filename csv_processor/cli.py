import argparse
from typing import Optional, List, Dict, Union
from .models import FilterCondition, Aggregation
from .processor import CSVProcessor
from  .exceptions import InvalidOperatorError,  InvalidAggregateError, InvalidColumnError

def parse_where(where: str) -> FilterCondition:
    operators = ('>', '>=', '<', '<=', '=')
    for operator in operators:
        if operator in where:
            parts = where.split(operator)
            if len(parts) == 2:
                return FilterCondition(column=parts[0], operator=operator, value=parts[1])

    raise InvalidOperatorError(f'Invalid operator: {where}')

def parse_aggregate(aggregate: str) -> Aggregation:
    if '=' not in aggregate:
        raise InvalidAggregateError(f'Invalid aggregate: {aggregate}')

    column, operation = aggregate.split('=')
    return Aggregation(column=column, operator=operation)

def format_table(data: List[Dict[str, str]]) -> str:
    if not data:
        return "Нет данных"

    headers = data[0].keys()
    max_lengths = {header: len(header) for header in headers}

    # Находим максимальные длины для каждого столбца
    for row in data:
        for header in headers:
            length = len(str(row[header]))
            if length > max_lengths[header]:
                max_lengths[header] = length

    # Создаем горизонтальную линию
    line = "+" + "+".join(["-" * (max_lengths[header] + 2) for header in headers]) + "+"

    # Форматируем заголовки
    header_line = "|" + "|".join([f" {header.ljust(max_lengths[header])} " for header in headers]) + "|"

    # Форматируем строки данных
    rows = []
    for row in data:
        row_line = "|" + "|".join([f" {str(row[header]).ljust(max_lengths[header])} " for header in headers]) + "|"
        rows.append(row_line)

    return "\n".join([line, header_line, line] + rows + [line])


def display_results(results: Union[list, dict]) -> None:
    """Отображение результатов в консоли"""
    if isinstance(results, list):
        if not results:
            print("Нет данных, соответствующих условиям фильтрации")
            return
        print(format_table(results))
    else:
        # Для агрегированных результатов (словарь)
        operation, value = next(iter(results.items()))
        line = "+" + "-" * (len(operation) + 2) + "+"
        print(f"{line}\n| {operation.ljust(len(operation))} |\n{line}\n| {str(value).ljust(len(operation))} |\n{line}")


def process_csv(
        file_path: str,
        where: Optional[str] = None,
        aggregate: Optional[str] = None
) -> None:
    """Обработка CSV файла с заданными параметрами"""
    try:
        processor = CSVProcessor(file_path)

        filter_condition = parse_where(where) if where else None
        aggregation = parse_aggregate(aggregate) if aggregate else None

        results = processor.process(filter_condition, aggregation)
        display_results(results)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден")
    except InvalidOperatorError as e:
        print(f"Ошибка фильтрации: {e}")
    except InvalidAggregateError as e:
        print(f"Ошибка агрегации: {e}")
    except InvalidColumnError as e:
        print(f"Ошибка колонки: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")