#!/usr/bin/env python3
import os
import sys

from src.classes.csv_parser import CsvParser
from src.classes.mailmerge import MailMerge
from src.classes.parseargs import ParseArgs
from src.classes.qualys_api import QualysApi


def send_email() -> int:
    send = input('Send welcome email to users? [Y/n] ').strip().lower()
    if send == 'y':
        return 1
    elif send == 'n':
        return 0
    print('Invalid input, not sending welcome email...')
    return 0


def main():
    args = sys.argv[1:]
    parser = ParseArgs(args)
    mailmerge_config = './src/configs/mailmerge_server.conf'
    mailmerge_template = './src/configs/mailmerge_template.txt'
    mailmerge_database = './data/mailmerge_database.csv'

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

        if send == 0:
            try:
                MailMerge(
                    mailmerge_config,
                    mailmerge_template,
                    mailmerge_database)
            except ValueError:
                print('Unable to locate the proper MailMerge files, or',
                      'the MailMerge files may be unconfigured!')
                print('If you have not created these files, please run',
                      'the following command:', 'mailmerge --sample')
                print(
                    'You will then need to update the constants file',
                    'located at:',
                    f'{os.path.realpath("./src/constants/constants.py")}')
                exit(1)

        i = 0
        users = []
        for row in rows:
            email = row['email']
            print(f'Creating user {email}...')
            if send == 1:
                row['send_email'] = 1

            result = qa.add_user(**row)
            if result:
                if send == 1:
                    user = {
                        'email': email,
                        'username': qa.user[i],
                        'url': f'https://{qa.headers["Host"]}'}
                else:
                    user = {
                        'email': email,
                        'username': qa.user[i][0],
                        'password': qa.user[i][1],
                        'url': f'https://{qa.headers["Host"]}'}
                users.append(user)
                i += 1

        if len(qa.user) > 0:
            print(f'{len(qa.user)} users created successfully!')
            print(qa.user)

        if len(qa.failed_user) > 0:
            print(f'{len(qa.failed_user)} users were not created!')
            print(qa.failed_user)

        if send == 0:
            merge = MailMerge(
                mailmerge_config,
                mailmerge_template,
                mailmerge_database)
            merge.build_database(users)

        else:
            print(
                'Welcome emails will now be sent to all successfully',
                'created users!')

        exit(0)

    elif parser.action == 'tag':
        print(
            'This functionality is not currently implemented and is',
            'coming soon!')
        exit(0)

    elif parser.action == 'reset':
        print('Starting reset password process...')
        send = send_email()

        if send == 0:
            try:
                MailMerge(
                    mailmerge_config,
                    mailmerge_template,
                    mailmerge_database)
            except ValueError:
                print('Unable to locate the proper MailMerge files, or',
                      'the MailMerge files may be unconfigured!')
                print('If you have not created these files, please run',
                      'the following command:', 'mailmerge --sample')
                print(
                    'You will then need to update the constants file',
                    'located at:',
                    f'{os.path.realpath("./src/constants/constants.py")}')
                exit(1)

        qa = QualysApi(parser.credentials)  # type: ignore
        print('Getting a list of all Users in your Qualys subscription...')
        qa.list_users()
        usernames = parser.users
        i = 0
        users = []
        email = 'bademail@nodomain.com'
        for username in usernames:  # type: ignore
            print(f'Resetting password for {username}...')
            for user_details in qa.users:
                if username == user_details[0]:
                    email = user_details[2]

            result = qa.reset_password(username, send)
            if result:
                if send == 1:
                    user = {
                        'email': email,
                        'username': qa.user[i],
                        'url': f'https://{qa.headers["Host"]}'}
                else:
                    user = {
                        'email': email,
                        'username': qa.user[i][0],
                        'password': qa.user[i][1],
                        'url': f'https://{qa.headers["Host"]}'}
                users.append(user)
                i += 1

        if len(qa.user) > 0:
            print(f'{len(qa.user)} user\'s password reset successfully!')
            print(qa.user)

        if len(qa.failed_user) > 0:
            print(f'{len(qa.failed_user)} user\'s password were not reset!')
            print(qa.failed_user)

        if send == 0:
            merge = MailMerge(
                mailmerge_config,
                mailmerge_template,
                mailmerge_database)
            merge.build_database(users)

        else:
            print(
                'Password reset emails will now be sent to all',
                'successful users!')

        exit(0)


if __name__ == '__main__':
    main()
