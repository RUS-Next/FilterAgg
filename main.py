import argparse
from csv_processor.cli import process_csv


def main():
    parser = argparse.ArgumentParser(description='Обработка CSV файлов')
    parser.add_argument('--file', required=True, help='Путь к CSV файлу')
    parser.add_argument('--where', help='Условие фильтрации (например, "rating>4.7")')
    parser.add_argument('--aggregate', help='Условие агрегации (например, "rating=avg")')

    args = parser.parse_args()
    process_csv(args.file, args.where, args.aggregate)


if __name__ == '__main__':
    main()