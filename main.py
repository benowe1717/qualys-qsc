#!/usr/bin/env python3
import constants
from parseargs import parseArgs
from helper import helper
from auth import qualysApiAuth
from asset_tag import qualysApiAssetTag
from user import qualysApiUser
from asset import qualysApiAsset
import csv, os, sys

def create(users):
    # This may seem like an unnecessary thing to repeat, however, since we try to use session-based
    # authentication whenever possible, we want to ensure we are refreshing that active session before
    # any critical work needs to be done to help minimize authentication issues in the middle of work
    user = qualysApiUser()
    h = helper()

    errors = 0
    successes = 0
    for u in users:
        email = u.lower().strip()
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

    h.writeCsv(user.user_details)

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

def main():
    args = sys.argv
    myparser = parseArgs(args)
    debug = myparser.debug

    if debug:
        # TODO --> implement debug logging maybe?
        pass

    else:
        if myparser.action == "test":
            auth = qualysApiAuth()
            print("Success! Your credentials are valid!")
            myparser.parser.exit()

        elif myparser.action == "create":
            lines = []
            for f in myparser.files:
                if not os.path.exists(f):
                    print(f"ERROR: Unable to locate file: {f}! Removing file from the list...")
                    myparser.files.remove(f)

                else:
                    h = helper()
                    result = h.readFile(f)
                    if not result:
                        print(f"ERROR: Unable to read file: {f}! Removing file from the list...")
                        myparser.files.remove(f)

                    else:
                        lines.append(result)

            users = [user for line in lines for user in line]
            create(users)

            print(f"All users that were successfully created have been written to the {constants.OUTPUT_FILE} file.")
            print("Please ensure that you have installed the `mailmerge` utility from the requirements.txt file")
            print("Please also ensure that you have configured your SMTP sersver in the mailmerge_server.conf file")
            print("And finally confirm the email template is present in the file mailmerge_template.txt")
            print("If all looks good, you can run `mailmerge --no-limit --no-dry-run` to send out credentials to all users!")

        elif myparser.action == "create-and-tag":
            lines = []
            for f in myparser.files:
                if not os.path.exists(f):
                    print(f"ERROR: Unable to locate file: {f}! Removing file from the list...")
                    myparser.files.remove(f)

                else:
                    h = helper()
                    result = h.readFile(f)
                    if not result:
                        print(f"ERROR: Unable to read file: {f}! Removing file from the list...")
                        myparser.files.remove(f)

                    else:
                        lines.append(result)

            users = [user for line in lines for user in line]
            print(users)

if __name__ == "__main__":
    main()