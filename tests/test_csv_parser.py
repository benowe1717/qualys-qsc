#!/usr/bin/env python3
import os

import pytest

from src.classes.csv_parser import CsvParser


class TestCsvParser:
    def setUp(self):
        self.base_path = '/home/benjamin/Documents/qualys/qualys-qsc/'
        self.csv_file = self.base_path + 'data/users.csv'
        self.csv = CsvParser(self.csv_file)

    def tearDown(self):
        del self.csv
        del self.csv_file
        del self.base_path

    def test_get_row_data_failed(self):
        self.setUp()
        header = ['key1', 'key2', 'key3', 'key4', 'key5']
        values = ['val1', 'val2', 'val4', 'val5']
        result = self.csv._get_row_data(header, values)
        assert result == {}
        self.tearDown()

    def test_get_row_data_all_values(self):
        self.setUp()
        header = ['key1', 'key2', 'key3', 'key4', 'key5']
        values = ['val1', 'val2', 'val3', 'val4', 'val5']
        result = self.csv._get_row_data(header, values)
        assert isinstance(result, dict)
        assert result == {
            'key1': 'val1',
            'key2': 'val2',
            'key3': 'val3',
            'key4': 'val4',
            'key5': 'val5'
        }
        self.tearDown()

    def test_get_row_data_blank_values(self):
        self.setUp()
        header = ['key1', 'key2', 'key3', 'key4', 'key5']
        values = ['val1', 'val2', '', 'val4', 'val5']
        result = self.csv._get_row_data(header, values)
        assert isinstance(result, dict)
        assert result == {
            'key1': 'val1',
            'key2': 'val2',
            'key3': '',
            'key4': 'val4',
            'key5': 'val5'
        }
        self.tearDown()

    def test_get_delimiter_falied(self):
        self.setUp()
        value = 'col1&col2&col3&col4&col5'
        result = self.csv._get_delimiter(value)
        assert result == ''
        self.tearDown()

    def test_get_delimiter_comma(self):
        self.setUp()
        value = 'col1,col2,col3,col4,col5'
        result = self.csv._get_delimiter(value)
        assert result == ','
        self.tearDown()

    def test_get_delimiter_semicolon(self):
        self.setUp()
        value = 'col1;col2;col3;col4;col5'
        result = self.csv._get_delimiter(value)
        assert result == ';'
        self.tearDown()

    def test_get_delimiter_pipe(self):
        self.setUp()
        value = 'col1|col2|col3|col4|col5'
        result = self.csv._get_delimiter(value)
        assert result == '|'
        self.tearDown()

    def test_read_csv(self):
        self.setUp()
        result = self.csv.read_csv()
        assert isinstance(result, list)
        assert len(result) == 4
        row = result[0]
        assert isinstance(row, dict)
        assert len(row) == 11
        assert 'email' in row.keys()
        assert 'bowen@qualys.com' == row['email']
        self.tearDown()

    def test_write_csv(self):
        self.setUp()
        file = 'tests/data/users.csv'
        parser = CsvParser(file)
        url = 'https://url.com'
        keys = ['email', 'username', 'password', 'url']
        values = [{
            'email': 'bowen@qualys.com',
            'username': 'bowen',
            'password': 'password1',
            'url': url
        }, {
            'email': 'rarmstrong@qualys.com',
            'username': 'rarmstrong',
            'password': 'password2',
            'url': url
        }]
        result = parser.write_csv(keys, values)
        assert result is True
        os.remove(file)
        self.tearDown()
