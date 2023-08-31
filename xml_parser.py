#!/usr/bin/env python3
import xml.etree.ElementTree as ET

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
            tree = ET.fromstring(xml_data)
            self.xml_data = tree
        except TypeError:
            print(f"ERROR: Unable to parse XML Output!")
            exit(1)

    def parseUserReturn(self):
        """
            This method is used to parse the XML Output of the
            Qualys API User Creation call to determine if the result
            was actually successful or not
        """
        for item in self.xml_data.iter("USER_OUTPUT"):
            for child in item:
                if child.tag == "RETURN":
                    status = child.get("status")

                    if status == "FAILED":
                        for grandchild in child:
                            if grandchild.tag == "MESSAGE":
                                message = grandchild.text
                                
                                self.err_msg = message
                                return False
        return True