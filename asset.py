#!/usr/bin/env python3
import constants
from requestshelper import requestsHelper
from xml_parser import qualysApiXmlParser
import logging

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
    assets_to_tag = []
    failed_assets = []
    helper = ""
    logger = ""
    successful_assets = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Starting up the qualysApiAsset() class..."
        )
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
        self.logger.info(
            f"Starting a search for assets using the term: {needle}..."
        )

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
            self.logger.error(
                "Unable to search for assets!"
            )
            exit(1)

        else:
            self.logger.info(
                "Successfully found assets matching the search term!"
            )
            xml = qualysApiXmlParser(result)
            responseCode = xml.xml_data["ServiceResponse"]["responseCode"]

            while responseCode == "SUCCESS":
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
                        self.logger.error(
                            "Unable to search for assets!"
                        )
                        exit(1)

                    else:
                        xml = qualysApiXmlParser(result)
                        responseCode = xml.xml_data["ServiceResponse"]["responseCode"]
                        
                else:
                    break