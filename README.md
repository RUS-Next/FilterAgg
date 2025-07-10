# FilterAgg

A lightweight Python tool for filtering and aggregating CSV data from the command line.

## Features

- **Filter data** with `>`, `<`, and `=` operators
- **Calculate aggregates**: `avg`, `min`, `max`
- **Clean terminal output** with formatted tables
- **Error handling** for invalid operations
- **No external dependencies** (except pytest for testing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/csv-processor.git
cd csv-processor
```
2. Ensure you have Python 3.8+ installed

## Usage
Basic commands:
```bash
# Show all data
python main.py --file data.csv

# Filter examples
python main.py --file data.csv --where "rating>4.5"
python main.py --file data.csv --where "brand=apple"

# Aggregation examples
python main.py --file data.csv --aggregate "price=avg"
python main.py --file data.csv --aggregate "rating=max"

# Combined filter and aggregate
python main.py --file data.csv --where "brand=xiaomi" --aggregate "price=min"
```

## Examples
Filtering data
```bash
$ python main.py --file products.csv --where "price>500"
+-------------------+--------+-------+--------+
| name              | brand  | price | rating |
+-------------------+--------+-------+--------+
| iphone 15 pro     | apple  | 999   | 4.9    |
| galaxy s23 ultra  | samsung| 1199  | 4.8    |
+-------------------+--------+-------+--------+
```

Aggregating data
```bash
$ python main.py --file products.csv --aggregate "rating=avg"
+-------+
| avg   |
+-------+
| 4.67  |
+-------+
```

## License
MIT