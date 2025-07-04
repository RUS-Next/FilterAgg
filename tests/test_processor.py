import pytest
import csv
import os
from csv_processor.processor import CSVProcessor
from csv_processor.models import FilterCondition, Aggregation
from csv_processor.exceptions import InvalidOperatorError, InvalidAggregateError, InvalidColumnError

@pytest.fixture
def sample_csv(tmp_path):
    file_path = os.path.join(tmp_path, 'test.csv')
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'brand', 'price', 'rating'])
        writer.writerow(['iphone', 'apple', '999', '4.9'])
        writer.writerow(['galaxy', 'samsung', '1199', '4.8'])
        writer.writerow(['redmi', 'xiaomi', '199', '4.6'])
        writer.writerow(['poco', 'xiaomi', '299', '4.4'])
    return file_path

# Reading test
def test_read_csv(sample_csv):
    processor = CSVProcessor(sample_csv)
    assert len(processor.data) == 4
    assert processor.data[0]['brand'] == 'apple'
    assert processor.data[1]['name'] == 'galaxy'
    assert processor.data[2]['price'] == '199'
    assert processor.data[3]['rating'] == '4.4'

# Filtering tests
def test_filter_equals(sample_csv):
    processor = CSVProcessor(sample_csv)
    condition = FilterCondition(column='brand', operator='=', value='samsung')
    filtered = processor._apply_filter(condition)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'galaxy'

def test_filter_gt(sample_csv):
    processor = CSVProcessor(sample_csv)
    condition = FilterCondition(column='price', operator='>', value='1000')
    filtered = processor._apply_filter(condition)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'galaxy'

def test_filter_lt(sample_csv):
    processor = CSVProcessor(sample_csv)
    condition = FilterCondition(column='rating', operator='<', value='4.5')
    filtered = processor._apply_filter(condition)
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'poco'

def test_filter_goe(sample_csv):
    processor = CSVProcessor(sample_csv)
    condition = FilterCondition(column='price', operator='>=', value='999')
    filtered = processor._apply_filter(condition)
    assert len(filtered) == 2
    assert filtered[0]['name'] == 'iphone'
    assert filtered[1]['name'] == 'galaxy'

def test_filter_loe(sample_csv):
    processor = CSVProcessor(sample_csv)
    condition = FilterCondition(column='rating', operator='<=', value='4.6')
    filtered = processor._apply_filter(condition)
    assert len(filtered) == 2
    assert filtered[0]['name'] == 'redmi'
    assert filtered[1]['name'] == 'poco'

# Aggregation tests
def test_aggregation_avg(sample_csv):
    processor = CSVProcessor(sample_csv)
    aggregation = Aggregation(column='rating', operator='avg')
    result = processor._apply_aggregation(processor.data, aggregation)
    assert pytest.approx(result['avg'], 0.01) == 4.675

def test_aggregation_min(sample_csv):
    processor = CSVProcessor(sample_csv)
    aggregation = Aggregation(column='price', operator='min')
    result = processor._apply_aggregation(processor.data, aggregation)
    assert result['min'] == 199

def test_aggregation_max(sample_csv):
    processor = CSVProcessor(sample_csv)
    aggregation = Aggregation(column='price', operator='max')
    result = processor._apply_aggregation(processor.data, aggregation)
    assert result['max'] == 1199

# Errors tests
def test_invalid_operator(sample_csv):
    processor = CSVProcessor(sample_csv)
    condition = FilterCondition(column='brand', operator='sgdfgsdfg', value='samsung')
    with pytest.raises(InvalidOperatorError):
        processor._apply_filter(condition)

def test_invalid_aggregate(sample_csv):
    processor = CSVProcessor(sample_csv)
    aggregation = Aggregation(column='rating', operator='invalid')
    with pytest.raises(InvalidAggregateError):
        processor._apply_aggregation(processor.data, aggregation)

def test_invalid_column(sample_csv):
    processor = CSVProcessor(sample_csv)
    aggregation = Aggregation(column='invalid', operator='avg')
    with pytest.raises(InvalidColumnError):
        processor._apply_aggregation(processor.data, aggregation)
