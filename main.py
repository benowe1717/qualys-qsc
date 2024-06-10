#!/usr/bin/env python3
import sys

from src.classes.csv_parser import CsvParser
from src.classes.parseargs import ParseArgs
from src.classes.qualys_api import QualysApi


def send_email() -> int:
    send = input('Send welcome email to users? [Y/n]').strip().lower()
    if send == 'y':
        return 1
    elif send == 'n':
        return 0
    print('Invalid input, not sending welcome email...')
    return 0


def main():
    args = sys.argv[1:]
    parser = ParseArgs(args)

    if parser.action == 'test':
        print('Starting test process...')
        if not parser.credentials:
            print('Invalid credentials file!')
            exit(1)

        qa = QualysApi(parser.credentials)  # type: ignore
        result = qa.test()
        if not result:
            print('Invalid username/password or other error!')
            exit(1)

        print('Your credentials are valid!')
        exit(0)

    elif parser.action == 'create':
        print('Starting new user creation process...')
        csvparser = CsvParser(parser.users)  # type: ignore
        rows = csvparser.read_csv()
        send = send_email()
        qa = QualysApi(parser.credentials)  # type: ignore

        if len(rows) == 0:
            print('No Users to add!')
            exit(0)

        for row in rows:
            user = row['email']
            print(f'Creating user {user}...')
            if send == 1:
                row['send_email'] = 1

            qa.add_user(**row)

        if len(qa.user) > 0:
            print(f'{len(qa.user)} users created successfully!')
            print(qa.user)

        if len(qa.failed_user) > 0:
            print(f'{len(qa.failed_user)} users were not created!')
            print(qa.failed_user)

    elif parser.action == 'reset':
        print('Starting reset password process...')
        print(parser.users)
        print(parser.credentials)


if __name__ == '__main__':
    main()
