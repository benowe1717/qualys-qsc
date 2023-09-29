#!/usr/bin/env python3
import constants
import xmltodict

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
        """
        status = self.xml_data["USER_OUTPUT"]["RETURN"]["@status"]

        if status == "FAILED":
            message = self.xml_data["USER_OUTPUT"]["RETURN"]["MESSAGE"]
            self.err_msg = message
            return False
        elif status == "SUCCESS":
            username = self.xml_data["USER_OUTPUT"]["USER"]["USER_LOGIN"]
            password = self.xml_data["USER_OUTPUT"]["USER"]["PASSWORD"]
            return [username, password]

    def parseTagSearchReturn(self):
        """
            This method is used to parse the XML Output of the
            Qualys API Asset Tag Search call to determine if the Asset Tag
            exists and return it's ID or return -1
        """
        tag_id = -1
        count = int(self.xml_data["ServiceResponse"]["count"])

        if count >= 1:
            tag_id = int(self.xml_data["ServiceResponse"]["data"]["Tag"]["id"])
            child_tags = []
            for item in self.xml_data["ServiceResponse"]["data"]["Tag"]["children"]["list"]["TagSimple"]:
                child_tagid = item["id"]
                child_tagname = item["name"]
                if constants.TAG_NAME in child_tagname:
                    child_tagdict = {child_tagid: {'name': child_tagname}}
                    child_tags.append(child_tagdict)

        return [tag_id, child_tags]

    def parseTagCreateReturn(self):
        """
            This method is used to parse the XML Output of the
            Qualys API Asset Tag Create call to determine if the Global Asset Tag
            and all of it's child tags were created successfully
        """
        status = self.xml_data["ServiceResponse"]["responseCode"]

        if status == "SUCCESS":
            return True
        else:
            return False

    def parseTagUpdateReturn(self):
        """
            This method is used to parse the XML Output of the 
            Qualys API Asset Tag Update call to determine if the Global Asset Tag
            was updated successfully with all given child tags
        """
        status = self.xml_data["ServiceResponse"]["responseCode"]

        if status == "SUCCESS":
            return True
        else:
            return False

    def parseTagUserReturn(self):
        """
            This method is used to parse the XML Output of the
            Qualys API Update User Tags call to determine if a given
            asset tag was properly assigned to a user
        """
        status = self.xml_data["ServiceResponse"]["responseCode"]

        if status == "SUCCESS":
            return True
        else:
            return False

    def parseTagAssetReturn(self):
        """
            This method is used to parse the XML Output of the
            Qualys API Update Asset call to determine if a given
            asset tag was applied to an asset
        """
        status = self.xml_data["ServiceResponse"]["responseCode"]

        if status == "SUCCESS":
            return True
        else:
            return False

    def parseRoleAssignResult(self):
        """
            This method is used to parse the XML Output of the
            Qualys API Update User call to determine if a given
            role/set of roles was applied to a user
        """
        status = self.xml_data["ServiceResponse"]["responseCode"]

        if status == "SUCCESS":
            return True
        else:
            return False