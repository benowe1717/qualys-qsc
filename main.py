#!/usr/bin/env python3
import sys

from src.classes.parseargs import ParseArgs


def main():
    args = sys.argv[1:]
    parser = ParseArgs(args)

    if parser.action == 'test':
        print('Starting test process...')
        print(parser.credentials)

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
