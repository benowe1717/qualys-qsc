#!/usr/bin/env python3
import constants
from auth import qualysApiAuth
from asset_tag import qualysApiAssetTag
from user import qualysApiUser
from asset import qualysApiAsset
import argparse, csv, os, sys

def writeCsv(data):
    keys = data[0].keys()
    with open(constants.OUTPUT_FILE, "w") as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def create(users):
    # This may seem like an unnecessary thing to repeat, however, since we try to use session-based
    # authentication whenever possible, we want to ensure we are refreshing that active session before
    # any critical work needs to be done to help minimize authentication issues in the middle of work
    user = qualysApiUser()

    errors = 0
    successes = 0
    for i in users:
        email = i.lower().strip()
        result = user.addUser(email)
        if not result:
            errors += 1
        else:
            successes += 1

    if errors > 0:
        print(f"{errors} users were not able to be created! Please check their details for accuracy!")
        print(", ".join(user.failed_users))
    
    if successes > 0:
        print(f"{successes} users were created successfully!")
        print(", ".join(user.successful_users))

    writeCsv(user.user_details)

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
    tag_errors = 0
    tag_successes = 0
    for username in user.users_to_tag:
        userid = user.searchUser(username)

        if userid != -1:
            role_errors = 0
            role_successes = 0
            failed_roles = []
            successful_roles = []
            
            for role in constants.ROLES:
                result = user.applyRoleToUser(userid, role)
                if result:
                    role_successes += 1
                    successful_roles.append(role)
                else:
                    role_errors += 1
                    failed_roles.append(role)

            result = tagging.tagUser(userid, username)
            if result:
                tag_successes += 1
                successful_tags.append(username)
            else:
                tag_errors += 1
                failed_tags.append(username)
        else:
            role_errors += 1
            tag_errors += 1
            failed_roles.append(role for role in constants.ROLES)
            failed_tags.append(username)

        if role_errors > 0:
            print(f"{role_errors} roles were not able to be assigned to {username}!")
            print(", ".join(failed_roles))

        if role_successes > 0:
            print(f"{role_successes} roles were assigned successfully to {username}!")
            print(", ".join(successful_roles))

    if tag_errors > 0:
        print(f"{tag_errors} users were not able to be tagged!")
        print(", ".join(failed_tags))
    
    if tag_successes > 0:
        print(f"{tag_successes} users were tagged successfully!")
        print(", ".join(successful_tags))

    asset = qualysApiAsset()
    asset.searchAssets(constants.NEEDLE)

    i = 0
    errors = 0
    successes = 0
    failed_assets = []
    successful_assets = []

    tag_count = len(tags)
    asset_count = len(asset.assets_to_tag)

    if tag_count > asset_count:
        asset_list = asset.assets_to_tag
        tag_list = tags[:asset_count]
        working_count = asset_count
    elif asset_count > tag_count:
        asset_list = asset.assets_to_tag[:tag_count]
        tag_list = tags
        working_count = tag_count
    else:
        asset_list = asset.assets_to_tag
        tag_list = tags
        working_count = asset_count

    if working_count > 0:
        while i < working_count:
            for key, value in asset_list[i].items():
                assetid = key
                assetname = value["name"]

            for key, value in tag_list[i].items():
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
        print(f"{successes} assets were were tagged successfully!")
        print(", ".join(successful_assets))

def printVersion():
    """
        This function is used in the argparse library to print the
        current version of this application
    """
    print("qsc_automation.py 0.1.8")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.\n")
    print("Written by Benjamin Owen; see below for original code")
    print("<https://github.com/benowe1717/qualys-qsc>")

def readFile(f):
    with open(f, "r") as file:
        lines = file.readlines()
        return lines
    return False

def main():
    parser = argparse.ArgumentParser(prog="main.py", description="Qualys QSC Hands-on Training is a `tool` that allows `administrators/trainers` to `provision accounts in a Qualys subscription`.")
    parser.add_argument("--version", action="store_true", required=False, help="show this program's current version")
    parser.add_argument("-f", "--file", nargs="+", required=False)
    parser.add_argument("-t", "--test", action="store_true", required=False, help="Test the API using the credentials on file before taking any actions")
    parser.add_argument("-c", "--create", action="store_true", required=False, help="Create users in the provided text file")
    parser.add_argument("-a", "--create-and-tag", action="store_true", required=False, help="Create users in the provided text, create a Global Asset Tag with child tags and tag all users and hosts")
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
        lines = []
        for f in args.file:
            if not os.path.exists(f):
                print(f"ERROR: Unable to locate file: {f}! Removing file from the list...")
                args.file.remove(f)
            else:
                result = readFile(f)
                if result is False:
                    print(f"ERROR: Unable to read file: {f}! Removing file from the list...")
                    args.file.remove(f)
                else:
                    lines.append(result)

    if len(lines) > 0:
        users = [user for line in lines for user in line]
        if args.create:
            create(users)

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

        print(f"All users that were successfully created have been written to the {constants.OUTPUT_FILE} file.")
        print("Please ensure that you have installed the `mailmerge` utility from the requirements.txt file")
        print("Please also ensure that you have configured your SMTP sersver in the mailmerge_server.conf file")
        print("And finally confirm the email template is present in the file mailmerge_template.txt")
        print("If all looks good, you can run `mailmerge --no-limit --no-dry-run` to send out credentials to all users!")
        
    else:
        print("No files remain to be parsed! Exiting...")
        exit(0)

if __name__ == "__main__":
    main()