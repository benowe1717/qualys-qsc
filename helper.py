#!/usr/bin/env python3
import constants
import csv

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

    def __init__(self):
        pass

    def readFile(self, f):
        with open(f, "r") as file:
            lines = file.readlines()
            return lines
        return False

    def writeCsv(self, data):
        keys = data[0].keys()
        with open(constants.OUTPUT_FILE, "w") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)