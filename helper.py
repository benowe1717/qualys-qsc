#!/usr/bin/env python3
import constants
import csv, logging

class helper():
    """
        This is a simple helper class for main.py to share it's methods
        with any other classes that might need them
    """

    #########################
    ### PRIVATE CONSTANTS ###
    #########################

    ########################
    ### PUBLIC CONSTANTS ###
    ########################

    #######################
    ### PRIVATE OBJECTS ###
    #######################

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    logger = ""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Starting up the helper() class..."
        )

    def readFile(self, f):
        self.logger.info(
            f"Reading {f}..."
        )
        with open(f, "r") as file:
            lines = file.readlines()
            self.logger.info(
                f"Successfully read {f}!"
            )
            return lines
        return False

    def writeCsv(self, data):
        self.logger.info(
            "Writing to mailmerge database file..."
        )
        keys = data[0].keys()
        with open(constants.OUTPUT_FILE, "w") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            self.logger.info(
                "Mailmerge database file successfully updated!"
            )