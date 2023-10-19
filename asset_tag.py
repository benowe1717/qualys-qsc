#!/usr/bin/env python3
import constants
from requestshelper import requestsHelper
from xml_parser import qualysApiXmlParser
import logging

class qualysApiAssetTag():
    """
        This class is responsible for Creating, Updating or Searching
        for Asset Tags and then tagging specific Assets or Users with
        the given Asset Tags.
    """

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

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    global_tag_id = -1
    child_tags = []
    helper = ""
    logger = ""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Starting up the qualysApiAssetTag() class..."
        )
        self.helper = requestsHelper()

    def searchTags(self):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 32
            This method is used to search through all of the Asset Tags in
            an instance and check to see if the GLOBAL_TAG exists. Based on
            the existence of the GLOBAL_TAG, this class will either create
            the GLOBAL_TAG or update the GLOBAL_TAG with all
            of the other tags.
        """
        self.logger.info(
            "Starting a search for the Global Asset Tag..."
        )

        endpoint = "/qps/rest/2.0/search/am/tag"
        self.helper.headers["Content-Type"] = "text/xml"
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
        result = self.helper.callApi(endpoint, payload, "xml")
        if result:
            self.logger.info(
                "Search for Global Asset Tag complete!"
            )
            xml = qualysApiXmlParser(result)
            search_result = xml.parseTagSearchReturn()
            if search_result[0] != -1:
                self.logger.info(
                    "The Global Asset Tag is already present!"
                )
                self.global_tag_id = search_result[0]
                self.child_tags = search_result[1]
            return True
            self.logger.info(
                "The Global Asset Tag is not present and needs to be created!"
            )
        self.logger.error(
            "Unable to search the Qualys API for the Global Asset Tag!"
        )
        return False

    def createGlobalTag(self, tags):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 20
            This method is used to create the GLOBAL_TAG Asset Tag with
            all of the required child tags.
        """
        self.logger.info(
            "Creating the Global Asset Tag..."
        )

        endpoint = f"/qps/rest/2.0/create/am/tag"
        self.helper.headers["Content-Type"] = "text/xml"
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
            t = {'name': f"{constants.TAG_NAME}{tag}"}
            payload['ServiceRequest']['data']['Tag']['children']['set']['TagSimple'].append(t)

        result = self.helper.callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            create_result = xml.parseTagCreateReturn()

            if create_result:
                self.logger.info(
                    "Successfully created the Global Asset Tag!"
                )
                return True

        self.logger.error(
            "Failed to create the Global Asset Tag!"
        )
        return False

    def updateGlobalTag(self, tags):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 25
            This method is used to update the already existing GLOBAL_TAG
            Asset Tag with all of the required child tags.
        """
        self.logger.info(
            "Updating the Global Asset Tag..."
        )

        endpoint = f"/qps/rest/2.0/update/am/tag/{self.global_tag_id}"
        self.helper.headers["Content-Type"] = "text/xml"
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
            t = {'name': f"{constants.TAG_NAME}{tag}"}
            payload['ServiceRequest']['data']['Tag']['children']['set']['TagSimple'].append(t)

        result = self.helper.callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            update_result = xml.parseTagUpdateReturn()

            if update_result:
                self.logger.info(
                    "Successfully updated the Global Asset Tag!"
                )
                return update_result

        self.logger.error(
            "Failed to update the Global Asset Tag!"
        )
        return False

    def tagUser(self, userid, tagname):
        """
            https://docs.qualys.com/en/admin/api/#t=rbac_apis%2Fupdate_user_tags_and_roles.htm
            This method takes a userid and a tagname and calls the Qualys
            Update User Tags API call and assigns the given tagname to the
            userid
        """
        self.logger.info(
            f"Attempting to tag the user {userid} with tag: {tagname}..."
        )

        endpoint = f"/qps/rest/2.0/update/am/user/{userid}"
        self.helper.headers["Content-Type"] = "text/xml"
        payload = {
            'ServiceRequest': {
                'data': {
                    'User': {
                        'scopeTags': {
                            'add': {
                                'TagData': {
                                    'name': f"{constants.TAG_NAME}{tagname}"
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.helper.callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            tag_result = xml.parseTagUserReturn()

            if tag_result:
                self.logger.info(
                    "Successfully tagged user!"
                )
                return True

        self.logger.error(
            "Failed to tag user!"
        )
        return False

    def tagAsset(self, assetid, tagid):
        """
            https://www.qualys.com/docs/qualys-asset-management-tagging-api-v2-user-guide.pdf :: Page 135
            This method takes a given assetid and tagid and updates the
            asset with the given tagid
        """
        self.logger.info(
            f"Attempting to tag the user {assetid} with tag: {tagid}..."
        )

        endpoint = "/qps/rest/2.0/update/am/asset"
        payload = {
            'ServiceRequest': {
                'filters': {
                    'Criteria': {
                        '@field': "id",
                        '@operator': "EQUALS",
                        '#text': str(assetid)
                    }
                },
                'data': {
                    'Asset': {
                        'tags': {
                            'add': {
                                'TagSimple': {
                                    'id': tagid
                                }
                            }
                        }
                    }
                }
            }
        }
        result = self.helper.callApi(endpoint, payload, "xml")
        if result:
            xml = qualysApiXmlParser(result)
            tag_result = xml.parseTagAssetReturn()

            if tag_result:
                self.logger.info(
                    "Successfully tagged asset!"
                )
                return True

        self.logger.error(
            "Failed to tag asset!"
        )
        return False