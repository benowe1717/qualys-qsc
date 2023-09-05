#!/usr/bin/env python3
import xmltodict, re

class qualysApiXmlParser():
    """
        This class is responsible for parsing the XML output from the
        Qualys API as not all 200 HTTP response codes indicate an actual
        successful result. Use this class to parse the real return message.
    """

    # Note that there are no "private" objects or methods in the
    # Python class structure, but it is generally accepted that
    # methods and objects with a single "_" (underscore) preceding
    # the name indicates something "not to be messed with". So I'm
    # adopting that convention to denote "private" objects and methods

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
    xml_data = ""
    err_msg = ""

    def __init__(self, xml_data):
        try:
            self.xml_data = xmltodict.parse(xml_data)
        except:
            print(f"ERROR: Unable to parse XML Output!")
            exit(1)

    def parseUserReturn(self):
        """
            This method is used to parse the XML Output of the
            Qualys API User Creation call to determine if the result
            was actually successful or not

            {"USER_OUTPUT": {"API": {"@name": "user.php", "@username": "yourapiusername", "@at": "1970-01-01T00:00:00Z"},
            "RETURN": {"@status": "SUCCESS", "MESSAGE": "some_username user has been successfully created."}}}

            {"USER_OUTPUT": {"API": {"@name": "user.php", "@username": "yourapiusername", "@at": "1970-01-01T00:00:00Z"},
            "RETURN": {"@status": "FAILED", "@number": "1234", MESSAGE": "failure reason goes here"}}}
        """
        status = self.xml_data["USER_OUTPUT"]["RETURN"]["@status"]

        if status == "FAILED":
            message = self.xml_data["USER_OUTPUT"]["RETURN"]["MESSAGE"]
            self.err_msg = message
            return False
        elif status == "SUCCESS":
            message = self.xml_data["USER_OUTPUT"]["RETURN"]["MESSAGE"]
            username = re.search(r"^(?P<username>[a-z0-9]+)\s+user\s+has", message)
            return username