#!/usr/bin/env python3
from user import qualysApiUser
from pandas.errors import ParserError
import argparse, os, sys
import pandas as pd

def printVersion():
    """
        This function is used in the argparse library to print the current version of this application
    """
    print("qsc_automation.py 0.0.4")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.\n")
    print("Written by Benjamin Owen; see below for original code")
    print("<https://github.com/benowe1717/qualys-qsc>")

def readCsv(filename):
    """
        This function is used in two ways. 1) Test if the file is in fact a CSV file and 2) Read the data from a CSV file into a pandas dataframe
    """
    decoders = ["ISO-8859-1", "utf-8", "unicode_escape"]
    try:
        df = pd.read_csv(filename)
        return df
    except UnicodeDecodeError:
        print("Unable to read CSV file with the default encoding option!")
        for decoder in decoders:
            print(f"Attempting to reading CSV with the following encoding option: {decoder}...")
            try:
                df = pd.read_csv(filename, encoding=decoder)
                return df
            except UnicodeDecodeError:
                print(f"Unable to read CSV file with encoding option: {decoder}")
        return False
    except ParserError:
        # https://stackoverflow.com/a/67838605
        print(f"ERROR: The given file is not a CSV file!")
        return False

def main():
    parser = argparse.ArgumentParser(prog="qsc_automation.py", description="Qualys QSC Hands-on Training is a `tool` that allows `administrators/trainers` to `provision accounts in a Qualys subscription`.")
    parser.add_argument("--version", action="store_true", required=False, help="show this program's current version")
    parser.add_argument("-f", "--file", nargs="+", required=False)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    if args.version:
        printVersion()
        parser.exit()

    if args.file:
        dataframes = []
        for f in args.file:
            if not os.path.exists(f):
                print(f"ERROR: Unable to locate file: {f}! Removing file from the list...")
                args.file.remove(f)
            else:
                result = readCsv(f)
                if result is False:
                    print(f"ERROR: Unable to read file as CSV: {f}! Removing file from the list...")
                    args.file.remove(f)
                else:
                    dataframes.append([result, f])
        print(f"Remaining files to use: {args.file}")

        # convert to while loop so we can say we're done whenever
        if len(args.file) > 0:
            # instantiate user class
            # user = qualysApiUser()
            # check header row for required fields
            # if all required fields exist, loop through rows and create users
                # convert each row into the dict using the header as the key
                # and using the row value as the value
                # pass the entire dict to the user class
                # errors = 0
                # user.addUser(user_details=user_details)
                # if the user creation fails
                    # set errors=1
            # if any required field is missing
                # remove entire csv from list and move to the next one
            # if errors=1
                # print list of users that were failed to create users.failed_users
            pass
        else:
            print("No files remain to be parsed! Exiting...")
            exit(0)
    else:
        parser.print_help()
        parser.exit()

if __name__ == "__main__":
    main()