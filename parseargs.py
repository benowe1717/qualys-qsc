#!/usr/bin/env python3
import constants
import argparse, itertools

class parseArgs():
    """
        This class is a wrapper for the argpase python3 library
    """

    #########################
    ### PRIVATE CONSTANTS ###
    #########################

    ########################
    ### PUBLIC CONSTANTS ###
    ########################
    PROGRAM_NAME = constants.PROGRAM_NAME
    PROGRAM_DESCRIPTION = constants.PROGRAM_DESCRIPTION
    VERSION = constants.VERSION
    AUTHOR = constants.AUTHOR
    REPO = constants.REPO

    #######################
    ### PRIVATE OBJECTS ###
    #######################

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    parser = ""
    args = ""
    action = ""
    files = []
    users = []
    debug = False

    def __init__(self, args):
        self.parser = argparse.ArgumentParser(
            prog=self.PROGRAM_NAME, description=self.PROGRAM_DESCRIPTION
        )
        self.parser.add_argument(
            "-v", "--version", action="store_true", required=False,
            help="Show this program's current version"
        )
        self.parser.add_argument(
            "-d", "--debug", action="store_true", required=False,
            help="Enable debug logging"
        )
        self.parser.add_argument(
            "-t", "--test", action="store_true", required=False,
            help="Test the API using the credentials on file before taking any actions"
        )
        self.parser.add_argument(
            "-f", "--file", nargs="+",
            help="The path to the text file(s) that hold(s) all of the users you want to create"
        )
        self.parser.add_argument(
            "-c", "--create", action="store_true", required=False,
            help="Create users in the provided text file"
        )
        self.parser.add_argument(
            "-a", "--create-and-tag", action="store_true", required=False,
            help="Create users in the provided text, create a Global Asset Tag with child tags and tag all users and hosts"
        )
        self.parser.add_argument(
            "-r", "--reset-password", nargs="+", required=False,
            help="Reset the password for the provided usernames"
        )
        self.args = self.parser.parse_args()

        if len(args) == 1:
            self.parser.print_help()
            self.parser.exit()

        if self.args.version:
            self.printVersion()
            self.parser.exit()

        if self.args.debug:
            self.debug = True

        if self.args.test:
            self.action = "test"

        if self.args.create:
            if self.args.file is None:
                self.parser.error("--create requires --file")

            else:
                self.action = "create"
                self.files = self.args.file

        if self.args.create_and_tag:
            if self.args.file is None:
                self.parser.error("--create-and-tag requires --file")

            else:
                self.action = "create-and-tag"
                self.files = self.args.file

        if self.args.reset_password:
            self.action = "reset"
            for arg in self.args.reset_password:
                if "," in arg:
                    split = arg.split(",")
                    
                    for i in split:
                        if i:
                            self.users.append(i)

                else:
                    self.users.append(arg)

    def printVersion(self):
        """
            This function is used in the argparse library to print the
            current version of this application
        """
        print(f"{self.PROGRAM_NAME} v{self.VERSION}")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.\n")
        print(f"Written by {self.AUTHOR}; see below for original code")
        print(f"<{self.REPO}>")