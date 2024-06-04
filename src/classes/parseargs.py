#!/usr/bin/env python3
import argparse
import re

from src.classes.file_checker import FileChecker
from src.constants import constants


class ParseArgs:
    NAME = constants.ARGPARSE_PROGRAM_NAME
    DESC = constants.ARGPARSE_PROGRAM_DESCRIPTOIN
    VER = constants.ARGPARSE_PROGRAM_VERSION
    AUTH = constants.ARGPARSE_PROGRAM_AUTHOR
    REPO = constants.ARGPARSE_PROGRAM_REPO

    def __init__(self, args: list) -> None:
        self.args = args
        self.action = ''
        self.credentials = ''
        self.users = ''
        self.parser = argparse.ArgumentParser(
            prog=self.NAME, description=self.DESC)

        self.parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            required=False,
            help='Show this program\'s current version')

        self.parser.add_argument(
            '-c',
            '--credentials',
            nargs=1,
            help='The filepath to the file containing your API credentials'
        )

        self.parser.add_argument(
            '-t',
            '--test',
            action='store_true',
            required=False,
            help='Test the provided credentials against the Qualys API'
        )

        self.parser.add_argument(
            '-n',
            '--new',
            nargs=1,
            required=False,
            help='Create users in the Qualys Subscription from the given file'
        )

        self.parser.add_argument(
            '-r',
            '--reset-password',
            nargs='+',
            required=False,
            help='Reset the password for each of the provided users'
        )

        self.parse_args = self.parser.parse_args()
        if len(self.args) == 0:
            self.parser.print_help()
            self.parser.exit()

        # '-v'/'--version' provided
        if self.parse_args.version:
            self._print_version()
            self.parser.exit()

        # '-t'/'--test' provided
        # requires credentials
        if self.parse_args.test:
            self.action = 'test'
            if self.parse_args.credentials is None:
                self.parser.error('--test requires --credentials')

            self.credentials = self._is_valid_credentials_path(
                self.parse_args.credentials[0])
            if not self.credentials:
                self.parser.error('Invalid credentials file')

        # '-n'/'--new' provided
        # requires credentials
        if self.parse_args.new:
            self.action = 'new'
            if self.parse_args.credentials is None:
                self.parser.error('--new requires --credentials')

            self.credentials = self._is_valid_credentials_path(
                self.parse_args.credentials[0])
            if not self.credentials:
                self.parser.error('Invalid credentials file')

            self.users = self._is_valid_txt_file(self.parse_args.new[0])
            if not self.users:
                self.parser.error('Invalid text file')

        # '-r'/'--reset-password' provided
        # requires credentials
        if self.parse_args.reset_password:
            self.action = 'reset'
            if self.parse_args.credentials is None:
                self.parser.error('--reset-password requires --credentials')

            self.credentials = self._is_valid_credentials_path(
                self.parse_args.credentials[0])
            if not self.credentials:
                self.parser.error('Invalid credentials file')

            self.users = [user.strip(', ')
                          for user in self.parse_args.reset_password]

    def _print_version(self) -> None:
        print(f'{self.NAME} v{self.VER}')
        print(
            'This is free software:',
            'you are free to change and redistribute it.')
        print('There is NO WARARNTY, to the extent permitted by law.')
        print(f'Written by {self.AUTH}; see below for original code')
        print(f'<{self.REPO}')

    def _is_valid_credentials_path(self, path) -> str | bool:
        try:
            fc = FileChecker(path)
            if not fc.is_file():
                return False

            if not fc.is_readable():
                return False

            if not fc.is_yaml():
                return False

            return fc.file
        except ValueError:
            return False

    def _is_valid_txt_file(self, path) -> str | bool:
        try:
            fc = FileChecker(path)
            if not fc.is_file():
                return False

            if not fc.is_readable():
                return False

            if not fc.is_text():
                return False

            return fc.file
        except ValueError:
            return False
