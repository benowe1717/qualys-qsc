#!/usr/bin/env python3
import constants
from auth import qualysApiAuth
from asset_tag import qualysApiAssetTag
from user import qualysApiUser
from asset import qualysApiAsset
from pandas.errors import ParserError
import argparse, os, sys
import pandas as pd

def create(df):
    # This may seem like an unnecessary thing to repeat, however, since we try to use session-based
    # authentication whenever possible, we want to ensure we are refreshing that active session before
    # any critical work needs to be done to help minimize authentication issues in the middle of work
    user = qualysApiUser()

    # This returns just the first row of the dataframe, which will be the header row
    header = list(df)

    # Now compare the required fields to the given fields
    missing = validateHeaders(user.REQUIRED_FIELDS, header)
    if not missing:
        print(f"ERROR: {df[1]} is missing one more required fields! Please add the following headers to your CSV:")
        print(", ".join(missing))
        return False

    user_dicts = df.to_dict(orient="records")
    i = 0
    errors = 0
    successes = 0
    user.listUsers()
    while i < len(user_dicts):
        user_details = user_dicts[i]
        result = user.addUser(user_details=user_details)
        if not result:
            errors += 1
        else:
            successes += 1
        i += 1

    if errors > 0:
        print(f"{errors} users were not able to be created! Please check their details for accuracy!")
        print(", ".join(user.failed_users))
    
    if successes > 0:
        print(f"{successes} users were created successfully!")
        print(", ".join(user.successful_users))

    return user

def createAndTag(df):
    user = create(df)
    tagging = qualysApiAssetTag()

    result = tagging.searchTags()
    if result and tagging.global_tag_id != -1:
        tagging.updateGlobalTag(user.users_to_tag)
    else:
        tagging.createGlobalTag(user.users_to_tag)
    result = tagging.searchTags()
    tags = tagging.child_tags

    failed_tags = []
    successful_tags = []
    errors = 0
    successes = 0
    for username in user.users_to_tag:
        userid = user.searchUser(username)

        if userid != -1:
            result = tagging.tagUser(userid, username)
            if result:
                successful_tags.append(username)
                successes += 1
            else:
                errors += 1
                failed_tags.append(username)
        else:
            errors += 1
            failed_tags.append(username)

    if errors > 0:
        print(f"{errors} users were not able to be tagged!")
        print(", ".join(failed_tags))
    
    if successes > 0:
        print(f"{successes} users were tagged successfully!")
        print(", ".join(successful_tags))

    asset = qualysApiAsset()
    asset.searchAssets(constants.NEEDLE)

    i = 0
    errors = 0
    successes = 0
    failed_assets = []
    successful_assets = []
    count = len(asset.assets_to_tag)
    if count > 0:
        while i < count:
            for key, value in asset.assets_to_tag[i].items():
                assetid = key
                assetname = value["name"]
            for key, value in tags[i].items():
                tagid = key
                tagname = value["name"]
            result = tagging.tagAsset(assetid, tagid)
            if result:
                successes += 1
                successful_assets.append(assetname)
            else:
                errors += 1
                failed_assets.append(assetname)
            i += 1

    if errors > 0:
        print(f"{errors} assets were not able to be tagged!")
        print(", ".join(failed_assets))

    if successes > 0:
        print(f"{errors} assets were were tagged successfully!")
        print(", ".join(successful_assets))

def printVersion():
    """
        This function is used in the argparse library to print the current version of this application
    """
    print("qsc_automation.py 0.1.6")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.\n")
    print("Written by Benjamin Owen; see below for original code")
    print("<https://github.com/benowe1717/qualys-qsc>")

def readCsv(filename):
    """
        This function is used in two ways:
        1) Test if the file is in fact a CSV file and 
        2) Read the data from a CSV file into a pandas dataframe
    """
    decoders = constants.DECODERS
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
    parser = argparse.ArgumentParser(prog="main.py", description="Qualys QSC Hands-on Training is a `tool` that allows `administrators/trainers` to `provision accounts in a Qualys subscription`.")
    parser.add_argument("--version", action="store_true", required=False, help="show this program's current version")
    parser.add_argument("-f", "--file", nargs="+", required=False)
    parser.add_argument("-t", "--test", action="store_true", required=False, help="Test the API using the credentials on file before taking any actions")
    parser.add_argument("-c", "--create", action="store_true", required=False, help="Create users in the provided CSV file")
    parser.add_argument("-a", "--create-and-tag", action="store_true", required=False, help="Create users in the provided CSV, create a Global Asset Tag with child tags and tag all users and hosts")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    if args.version:
        printVersion()
        parser.exit()

    if args.test:
        auth = qualysApiAuth()
        print("Success! Your credentials are valid!")
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
    else:
        parser.print_help()
        parser.exit()

    if len(dataframes) > 0:
        if args.create:
            # loop over df
            # create each user
            # done
            for df in dataframes:
                data = df[0]
                filename = df[1]

                create(data)
        elif args.create_and_tag:
            # loop over df
            # create each user
            # create global tag if needed
            # create child tags using usernames
            # tag all usernames with child tags
            # tag all assets with child tags
            # done
            for df in dataframes:
                data = df[0]
                filename = df[1]

                createAndTag(data)
        else:
            parser.print_help()
            parser.exit()
    else:
        print("No files remain to be parsed! Exiting...")
        exit(0)

if __name__ == "__main__":
    main()