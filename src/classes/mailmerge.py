#!/usr/bin/env python3
from src.classes.csv_parser import CsvParser
from src.classes.file_checker import FileChecker
from src.constants import constants


class MailMerge:
    KEYS = constants.MAILMERGE_TEMPLATE_KEYS
    CONFIG_KEYS = constants.MAILMERGE_SERVER_KEYS

    def __init__(
            self,
            conf_file: str,
            template_file: str,
            database_file: str) -> None:
        self.conf_file = conf_file
        self.template_file = template_file
        self.database_file = database_file

    @property
    def conf_file(self) -> str:
        return self._conf_file

    @conf_file.setter
    def conf_file(self, file: str) -> None:
        fc = FileChecker(file)
        if not fc.is_file():
            raise ValueError('Not a file')

        if not fc.is_readable():
            raise ValueError('Not readable')

        if not self._is_valid_conf_file(fc.file):
            raise ValueError('Invalid config')

        self._conf_file = fc.file

    @property
    def template_file(self) -> str:
        return self._template_file

    @template_file.setter
    def template_file(self, file: str) -> None:
        fc = FileChecker(file)
        if not fc.is_file():
            raise ValueError('Not a file')

        if not fc.is_readable():
            raise ValueError('Not readable')

        if not self._is_valid_template_file(fc.file):
            raise ValueError('Invalid template')

        self._template_file = fc.file

    @property
    def database_file(self) -> str:
        return self._database_file

    @database_file.setter
    def database_file(self, file: str) -> None:
        fc = FileChecker(file)
        if not fc.is_file():
            raise ValueError('Not a file')

        if not fc.is_readable():
            raise ValueError('Not readable')

        if not fc.is_writable():
            raise ValueError('Not writable')

        if not self._is_valid_database_file(fc.file):
            raise ValueError('Invalid database')

        self._database_file = fc.file

    def _is_valid_conf_file(self, file: str) -> bool:
        with open(file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        first_line = '# Mailmerge SMTP Server Config'
        if first_line != lines[0]:
            return False

        start = '[smtp_server]'
        total_lines = len(lines)
        i = 0
        config = []
        while i < total_lines:
            if lines[i] == start:
                end = i + 6
                config = lines[(i + 1):end]
                break
            i += 1

        if len(config) == 0:
            return False

        for line in config:
            data = [x for x in line.split(' ') if x != '']
            if len(data) != 3:
                print(f'Invalid configuration line: {line}')
                return False

            if data[0] not in self.CONFIG_KEYS:
                print(f'Invalid configuration key/value: {line}')
                return False
        return True

    def _is_valid_template_file(self, file: str) -> bool:
        with open(file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) == 0:
            return False
        for key in self.KEYS:
            template_key = '{{' + key + '}}'
            exists = 0
            for line in lines:
                if template_key in line:
                    exists = 1
                    break
            if exists == 0:
                return False
        return True

    def _is_valid_database_file(self, file: str) -> bool:
        with open(file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            if len(lines) == 0:
                return False
            first_line = lines[0]

        headers = []
        delimiters = [',', ';', '|']
        for delimiter in delimiters:
            headers = first_line.split(delimiter)
            if len(headers) > 1:
                break
        if len(headers) == 0:
            return False
        for key in self.KEYS:
            if key not in headers:
                return False
        return True

    def _print_help_message(self) -> None:
        print(f'Please review the {self.database_file} file for accuracy')
        print(
            'If all looks good, please run the following command to ',
            'use mailmerge to send out the welcome email to each of ',
            'your users:')
        print(
            f'mailmerge --config {self.conf_file} ',
            f'--template {self.template_file} ',
            f'--database {self.database_file}')

    def build_database(self, values: list) -> bool:
        parser = CsvParser(self.database_file)
        result = parser.write_csv(self.KEYS, values)
        if not result:
            return False
        self._print_help_message()
        return True
