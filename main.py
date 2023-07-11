#!/usr/bin/env python3
from auth import qualysApiAuth

def main():
    # Simply instantiating this class will do all the checks
    # needed to ensure we are logged in to the Qualys API.
    # Any failures to login will promptly exit the entire code
    # so there is no risk of continuing without authentication
    auth = qualysApiAuth()

if __name__ == "__main__":
    main()