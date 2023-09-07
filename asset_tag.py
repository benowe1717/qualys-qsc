#!/usr/bin/env python3
import constants
from auth import qualysApiAuth
from xml_parser import qualysApiXmlParser
from urllib.parse import quote
import os, requests, xmltodict, yaml

class qualysApiAssetTag():
    """
        This class is responsible for Creating, Updating or Searching
        for Asset Tags and then tagging specific Assets or Users with
        the given Asset Tags.
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
    GLOBAL_TAG = constants.GLOBAL_TAG

    #######################
    ### PRIVATE OBJECTS ###
    #######################
    _auth = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    global_tag_id = -1

    def __init__(self):
        # Instantiate the qualysApiAuth() class, which will run all the required authentication checks
        # right out of the gate. If there are any problems authenticating, it will die right here.
        # Otherwise, we continue as normal
        self._auth = qualysApiAuth()

    def searchTags(self):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 32
            This method is used to search through all of the Asset Tags in an instance and
            check to see if the GLOBAL_TAG exists. Based on the existence of the GLOBAL_TAG, 
            this class will either create the GLOBAL_TAG or update the GLOBAL_TAG with
            all of the other tags.
        """
        endpoint = "/qps/rest/2.0/search/am/tag"
        self.headers["Content-Type"] = "text/xml"
        payload = {
            "ServiceRequest": {
                "filters": {
                    "Criteria": {
                        "@field": "name",
                        "@operator": "EQUALS",
                        "#text": self.GLOBAL_TAG
                    }
                }
            }
        }
        url = self._auth.SCHEME + self._auth.BASE_URL + endpoint
        basic = requests.auth.HTTPBasicAuth(self._auth._username, self._auth._password)
        r = requests.post(url=url, headers=self.headers, data=xmltodict.unparse(payload, full_document=False), auth=basic)
        if r.status_code == 200:
            xml = qualysApiXmlParser(r.text)
            result = xml.parseTagSearchReturn()
            if result != -1:
                self.global_tag_id = result
            return True
        else:
            print(f"ERROR: Unable to search for Asset Tags! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
            return False

    def createGlobalTag(self, tags):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 20
            This method is used to create the GLOBAL_TAG Asset Tag with all of the required
            child tags.
        """
        pass

    def updateGlobalTag(self, tags):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 25
            This method is used to update the already existing GLOBAL_TAG Asset Tag with all of the
            required child tags.
        """
        endpoint = f"/qps/rest/2.0/update/am/tag/{self.global_tag_id}"
        url = self._auth.SCHEME + self._auth.BASE_URL + endpoint
        payload = {
            'ServiceRequest': {
                'data': {
                    'Tag': {
                        'children': {
                            'set': {
                                'TagSimple': []
                            }
                        }
                    }
                }
            }
        }

        for tag in tags:
            t = {'name': tag}
            payload['ServiceRequest']['data']['Tag']['children']['set']['TagSimple'].append(t)

        basic = requests.auth.HTTPBasicAuth(self._auth._username, self._auth._password)
        r = requests.post(url=url, headers=self.headers, data=xmltodict.unparse(payload, full_document=False), auth=basic)
        if r.status_code == 200:
            xml = qualysApiXmlParser(r.text)
            result = xml.parseTagUpdateReturn()
            if not result:
                print(f"ERROR: Unable to update the Global Asset Tag! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
                return False
            else:
                return True