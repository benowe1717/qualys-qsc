#!/usr/bin/env python3
import sys

from src.classes.parseargs import ParseArgs
from src.classes.qualys_api import QualysApi


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

    elif parser.action == 'new':
        print('Starting new user creation process...')
        print(parser.users)
        print(parser.credentials)

    elif parser.action == 'reset':
        print('Starting reset password process...')
        print(parser.users)
        print(parser.credentials)


if __name__ == '__main__':
    main()
