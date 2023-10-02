#!/usr/bin/env python3
import constants
from requestshelper import requestsHelper
from xml_parser import qualysApiXmlParser

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

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    helper = ""
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    failed_assets = []
    successful_assets = []
    assets_to_tag = []

    def __init__(self):
        self.helper = requestsHelper()

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
        limit = 100
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
        result = self.helper.callApi(endpoint, payload, "xml")
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