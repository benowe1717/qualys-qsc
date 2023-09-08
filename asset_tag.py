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

    def _callApi(self, endpoint, payload, request_type):
        """
            This method is here to make the network call to the Qualys API
            and serves as a repeatable point of entry to that API.
            param: endpoint
            type: string
            sampe: /path/to/api/endpoint

            param: payload
            type: string/dict
            sample: param1=this&param2=that
            sample: {'param1': 'this', 'param2': 'that'}

            param: request_type
            type: string
            this is either "params" or "xml"

            output: dict/boolean
            result: either a dict from xmltodict library on success or
                    False on failure
        """
        url = self._auth.SCHEME + self._auth.BASE_URL + endpoint
        basic = requests.auth.HTTPBasicAuth(self._auth._username, self._auth._password)
        if request_type == "params":
            r = requests.post(url=url, headers=self.headers, data=payload, auth=basic)
        elif request_type == "xml":
            self.headers["Content-Type"] = "text/xml"
            r = requests.post(url=url, headers=self.headers, data=xmltodict.unparse(payload, full_document=False), auth=basic)
        if r.status_code == 200:
            return r.text
        else:
            print(f"ERROR: Qualys API Call failed! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
            return False

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
        result = self._callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            tag_id = xml.parseTagSearchReturn()
            if result != -1:
                self.global_tag_id = tag_id
            return True
        return False

    def createGlobalTag(self, tags):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 20
            This method is used to create the GLOBAL_TAG Asset Tag with all of the required
            child tags.
        """
        endpoint = f"/qps/rest/2.0/create/am/tag"
        self.headers["Content-Type"] = "text/xml"
        payload = {
            'ServiceRequest': {
                'data': {
                    'Tag': {
                        'name': self.GLOBAL_TAG,
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

        result = self._callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            create_result = xml.parseTagCreateReturn()
            if create_result:
                return True
        return False

    def updateGlobalTag(self, tags):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 25
            This method is used to update the already existing GLOBAL_TAG Asset Tag with all of the
            required child tags.
        """
        endpoint = f"/qps/rest/2.0/update/am/tag/{self.global_tag_id}"
        self.headers["Content-Type"] = "text/xml"
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

        result = self._callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            update_result = xml.parseTagUpdateReturn()
            if update_result:
                return True
        return False

    def tagUser(self, userid, tagname):
        endpoint = f"/qps/rest/2.0/update/am/user/{userid}"
        self.headers["Content-Type"] = "text/xml"
        payload = {
            'ServiceRequest': {
                'data': {
                    'User': {
                        'scopeTags': {
                            'add': {
                                'TagData': {
                                    'name': tagname
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self._callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            print(result)
        return False

    def tagAsset(self, assetname):
        pass