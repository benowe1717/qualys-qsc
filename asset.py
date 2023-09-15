#!/usr/bin/env python3
import constants
from auth import qualysApiAuth
from xml_parser import qualysApiXmlParser
from urllib.parse import quote
import os, requests, xmltodict, yaml

class qualysApiAsset():
    """
        This class is responsible for Asset Management in the Qualys API
        Primarily this class will be used to search assets in a subscription
        and build a list that is ready to be tagged
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
    _auth = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    failed_assets = []
    successful_assets = []
    assets_to_tag = []

    def __init__(self):
        # Instantiate the qualysApiAuth() class, which will run all the required authentication checks
        # right out of the gate. If there are any problems authenticating, it will die right here.
        # Otherwise, we continue as normal
        self._auth = qualysApiAuth()

    def _callApi(self, endpoint, payload=None, request_type=None):
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
        if payload:
            if request_type == "params":
                r = requests.post(url=url, headers=self.headers, data=payload, auth=basic)
            elif request_type == "xml":
                self.headers["Content-Type"] = "text/xml"
                r = requests.post(url=url, headers=self.headers, data=xmltodict.unparse(payload), auth=basic)
        else:
            r = requests.get(url=url, headers=self.headers, auth=basic)
        if r.status_code == 200:
            return r.text
        else:
            print(f"ERROR: Qualys API Call failed! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
            return False

    def searchAssets(self, needle):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 137
            This method searches the entire asset list (haystack) using the
            given search term (needle) and builds a list of available assets
            to tag

            param: needle
            type: string
            sample: EC2
        """
        limit = 5
        offset = 0
        endpoint = "/qps/rest/2.0/search/am/asset"
        payload = {
            'ServiceRequest': {
                'filters': {
                    'Criteria': {
                        '@field': "name",
                        '@operator': "CONTAINS",
                        "#text": needle
                    }
                },
                'preferences': {
                    'limitResults': str(limit)
                }
            }
        }
        result = self._callApi(endpoint, payload, "xml")
        if not result:
            print(f"ERROR: Unable to search assets!")
            exit(1)
        else:
            xml = qualysApiXmlParser(result)
            while xml.xml_data["ServiceResponse"]["responseCode"] == "SUCCESS":
                for asset in xml.xml_data["ServiceResponse"]["data"]["Asset"]:
                    do_not_tag = 0
                    for tag in asset["tags"]["list"]["TagSimple"]:
                        if constants.TAG_NAME in tag["name"]:
                            do_not_tag = 1
                    
                    if do_not_tag == 0:
                        assetid = asset["id"]
                        assetname = asset["name"]
                        asset_dict = {assetid: {'name': assetname}}
                        self.assets_to_tag.append(asset_dict)

                if xml.xml_data["ServiceResponse"]["hasMoreRecords"] == "true":
                    offset = offset + limit
                    payload["ServiceRequest"]["preferences"]["startFromOffset"] = str(offset)
                    result = self._callApi(endpoint, payload, "xml")
                    if not result:
                        print(f"ERROR: Unable to search assets!")
                        exit(1)
                    else:
                        xml = qualysApiXmlParser(result)
                else:
                    break