#!/usr/bin/env python3
import constants
from requestshelper import requestsHelper
from xml_parser import qualysApiXmlParser
import logging, time

class qualysApiUser():
    """
        This class is responsible for User Management in the Qualys API
        Primarily this class will be used to add new users to a subscription
        that is provided by a CSV file and a YAML configuration file
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
    logger = ""
    failed_users = []
    successful_users = []
    users_to_tag = []
    user_details = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Starting up the qualysApiUser() class..."
        )
        self.helper = requestsHelper()

    def addUser(self, user):
        """
            https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G17.783431
            https://documenter.getpostman.com/view/7159960/SVzw51A9#52dc0ffe-a2ae-4dea-9cbb-661251477df5
            This method takes in an email address and creates the user
            in the given Qualys Subscription. The only input is the email
            address, the rest comes from the constants file.

            param: users
            type: string
            sample: test@test.com
        """
        self.logger.info(
            f"Attempting to create user: {user}..."
        )

        action = "add"
        send_email = 0
        endpoint = "/msp/user.php"
        payload = f"action={action}&send_email={send_email}"

        for key, value in constants.REQUIRED_FIELDS.items():
            payload = payload + f"&{key}={value}"

        result = self.helper.callApi(endpoint, payload, "params")
        if not result:
            self.logger.error(
                f"Failed to create user: {user}!"
            )
            self.failed_users.append(user)
            return False

        else:
            self.logger.info(
                f"Successfully created user: {user}!"
            )
            self.successful_users.append(user)
            xml = qualysApiXmlParser(result)
            user_details = xml.parseUserReturn()
            self.users_to_tag.append(user_details[0])
            user_dict = {
                "email": user,
                "username": user_details[0],
                "password": user_details[1],
                "url": constants.URL
            }
            self.user_details.append(user_dict)
            return True

    def searchUser(self, username):
        """
            https://docs.qualys.com/en/admin/api/#t=rbac_apis%2Fsearch_user_list_based_on_id_name_and_rolename.htm
            This method takes a given username (text) and searches the
            user list in the Qualys instance and checks to see if the
            username exists, and if it does exist, returns an id, otherwise
            returns -1. In pretty much every case this should return an id.

            param: username
            type: string
            sample: quays6bw

            output: integer
            result: 123456 or -1
        """
        self.logger.info(
            f"Starting search for user: {username}..."
        )

        endpoint = "/qps/rest/2.0/search/am/user/"
        payload = {
            'ServiceRequest': {
                'filters': {
                    'Criteria': {
                        '@field': "username",
                        '@operator': "EQUALS",
                        '#text': username
                    }
                },
                'preferences': {
                    'limitResults': {
                        '#text': "10"
                    }
                }
            }
        }
        result = self.helper.callApi(endpoint, payload, "xml")
        if not result:
            return -1

        else:
            xml = qualysApiXmlParser(result)
            if xml.xml_data["ServiceResponse"]["responseCode"] == "SUCCESS":
                count = int(xml.xml_data["ServiceResponse"]["count"])
                if count == 0:
                    return -1

                self.logger.info(
                    "Successfully found the User's ID!"
                )
                userid = int(xml.xml_data["ServiceResponse"]["data"]["User"]["id"])
                return userid

            else:
                self.logger.error(
                    "Failed to find the User's ID!"
                )
                return -1

    def applyRoleToUser(self, userid, rolename):
        """
            https://docs.qualys.com/en/admin/api/#t=rbac_apis%2Fupdate_user_tags_and_roles.htm
            This method takes a given user id and a given role name and
            applies the role to the user. This ensures that the created user
            has the right permissions within the Qualys subscription.
        """
        self.logger.info(
            f"Attempting to apply role: {rolename} to user: {userid}..."
        )

        endpoint = f"/qps/rest/2.0/update/am/user/{userid}"
        payload = {
            'ServiceRequest': {
                'data': {
                    'User': {
                        'roleList': {
                            'add': {
                                'RoleData': {
                                    'name': {
                                        '#text': rolename
                                    }
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
            role_result = xml.parseRoleAssignResult()

            if role_result:
                self.logger.info(
                    "Successfully applied role to user!"
                )
                return True

        self.logger.error(
            "Failed to apply role to user!"
        )
        return False

    def resetPassword(self, username):
        """
            https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G17.784588
            Take in a username and change the password for that user
        """
        # you actually CANNOT do this here b/c it's the qualys api so
        # of course it doesn't work like the rest of the api calls do
        # where this WOULD work and SHOULD work but it DOESN'T work
        # endpoint = "/msp/password_change.php"
        # payload = {
        #     "user_logins": username,
        #     "email": 0
        # }

        endpoint = f"/msp/password_change.php?user_logins={username}&email=0"
        result = self.helper.callApi(endpoint)
        if not result:
            return -1

        else:
            xml = qualysApiXmlParser(result)
            password = xml.parsePasswordReset()
            if not password:
                return -1

            else:
                return password