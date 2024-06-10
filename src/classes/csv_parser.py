#!/usr/bin/env python3
import csv


class CsvParser:

    def __init__(self, csv_file: str) -> None:
        self.csv_file = csv_file

    def _get_delimiter(self, value: str) -> str:
        values = value.split(',')
        if len(values) > 1:
            return ','

        values = value.split(';')
        print(values)
        if len(values) > 1:
            return ';'

        values = value.split('|')
        print(values)
        if len(values) > 1:
            return '|'

        return ''

    def _get_row_data(self, header: list, values: list) -> dict:
        row = {}
        total = len(header)
        i = 0
        while i < total:
            try:
                key = header[i]
                value = values[i]
                row[key] = value
            except KeyError:
                print('Missing key')
                return {}
            except IndexError:
                print('Missing index')
                return {}
            i += 1
        return row

    def read_csv(self) -> list:
        rows = []
        try:
            with open(self.csv_file, 'r') as file:
                first_line = file.readlines()[0].strip()
                delimiter = self._get_delimiter(first_line)
                if delimiter == '':
                    return []

            with open(self.csv_file, 'r') as file:
                data = csv.reader(
                    file, delimiter=delimiter, quotechar='|')
                csv_data = []
                for x in data:
                    csv_data.append(x)

            total = len(csv_data)
            if total > 0:
                header = csv_data[0]

                i = 1
                while i < total:
                    row = csv_data[i]
                    row_data = self._get_row_data(header, row)
                    rows.append(row_data)
                    i += 1

            return rows
        except FileNotFoundError:
            return []

    def write_csv(self, values: dict) -> None:
        pass
