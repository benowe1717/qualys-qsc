#!/usr/bin/env python3
from user import qualysApiUser
from pandas.errors import ParserError
import argparse, os, sys
import pandas as pd

def printVersion():
    """
        This function is used in the argparse library to print the current version of this application
    """
    print("qsc_automation.py 0.0.5")
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

def validateHeaders(required_fields, given_fields):
    """
        This function takes the list of required fields (required_fields) and compares it to the
        list of input fields (given_fields) to determine if we are given all the required fields

        param: list1
        type: list
        sample: [field1, field2, field3]

        param: list2
        type: list
        sample: [field1, field2]

        output: boolean/list
        result if lists match: True
        result if lists fail: list of missing fields
        sample: [field3]
    """
    s = set(given_fields)
    missing_fields = [x for x in required_fields if x not in s]
    if len(missing_fields) > 0:
        return missing_fields
    else:
        return True

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

        if len(args.file) > 0:
            for df in dataframes:
                # This may seem like an unnecessary thing to repeat, however, since we try to use session-based
                # authentication whenever possible, we want to ensure we are refreshing that active session before
                # any critical work needs to be done to help minimize authentication issues in the middle of work
                user = qualysApiUser()

                # This returns just the first row of the dataframe, which will be the header row
                header = list(df[0])

                # Now compare the required fields to the given fields
                missing = validateHeaders(user.required_fields, header)
                if not missing:
                    print(f"ERROR: {df[1]} is missing one more required fields! Please add the following headers to your CSV:")
                    print(", ".join(missing))
                    continue

                user_dicts = df[0].to_dict(orient="records")
                i = 0
                errors = 0
                while i < len(user_dicts):
                    user_details = user_dicts[i]
                    result = user.addUser(user_details=user_details)
                    if not result:
                        errors += 1
                    i += 1

                if errors > 0:
                    print(f"{errors} users were not able to be created! Please check their details for accuracy!")
                    print(", ".join(users.failed_users))

        else:
            print("No files remain to be parsed! Exiting...")
            exit(0)
    else:
        parser.print_help()
        parser.exit()

if __name__ == "__main__":
    main()