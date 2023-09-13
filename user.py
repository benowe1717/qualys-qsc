#!/usr/bin/env python3
import constants
from auth import qualysApiAuth
from xml_parser import qualysApiXmlParser
from urllib.parse import quote
import os, requests, time, xmltodict, yaml

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
    _PATH = os.path.dirname(os.path.realpath(__file__))
    _CONFIG = _PATH + "/.creds.yaml"

    ########################
    ### PUBLIC CONSTANTS ###
    ########################
    COUNTRIES_WITH_STATES = constants.COUNTRIES_WITH_STATES
    VALID_COUNTRIES = constants.VALID_COUNTRIES
    VALID_US_STATES = constants.VALID_US_STATES
    VALID_AUS_STATES = constants.VALID_AUS_STATES
    VALID_CAN_STATES = constants.VALID_CAN_STATES
    VALID_IN_STATES = constants.VALID_IN_STATES
    REQUIRED_FIELDS = constants.REQUIRED_FIELDS

    #######################
    ### PRIVATE OBJECTS ###
    #######################
    _auth = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    current_users = []
    failed_users = []
    successful_users = []
    users_to_tag = []

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

    def validateCountryCode(self, country_code):
        """
            This method is used to validate if the Country Code assigned
            to the User in the CSV file is a valid Country Code for the Qualys API
            https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G17.784098
        """
        if country_code in self.VALID_COUNTRIES:
            return True
        return False

    def validateStateCode(self, country_code, state_code):
        """
            This method is used to validate if the State assigned to
            the User in the CSV file is a valid State for the corresponding
            Country Code for the Qualys API
            https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G17.784098
        """
        if country_code == "United States of America":
            if state_code in self.VALID_US_STATES:
                return True
        elif country_code == "Australia":
            if state_code in self.VALID_AUS_STATES:
                return True
        elif country_code == "Canada":
            if state_code in self.VALID_CAN_STATES:
                return True
        elif country_code == "India":
            if state_code in self.VALID_IN_STATES:
                return True
        return False

    def listUsers(self):
        """
            https://docs.qualys.com/en/vm/api/users/index.htm#t=users%2Flist_users.htm
            This method lists all users in the current subscription and
            adds each email address to the self.current_users list which
            will be used to verify if duplicate users are going to be created
        """
        endpoint = "/msp/user_list.php"
        result = self._callApi(endpoint)
        if result:
            xml = qualysApiXmlParser(result)
            for user in xml.xml_data["USER_LIST_OUTPUT"]["USER_LIST"]["USER"]:
                email = user["CONTACT_INFO"]["EMAIL"]
                if email not in self.current_users:
                    self.current_users.append(email)
        else:
            print(f"ERROR: Unable to get user list!")
            exit(1)

    def addUser(self, user_details):
        """
            https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G17.783431
            https://documenter.getpostman.com/view/7159960/SVzw51A9#52dc0ffe-a2ae-4dea-9cbb-661251477df5
            This method takes in a dictionary of user_details and creates the user in the given Qualys subscription.
            Not all users will have the same details, but there are some required details that will stay the same.

            param: user_details
            type: dictionary
            sample: {
                user_role: "role", business_unit: "unit", first_name: "fname", last_name: "lname", title: "title",
                phone: 1112223333, email: "name@domain.tld", address1: "1 Main Street", city: "Park Place",
                country: "United States of America", state: "New York"
            }

            output: boolean
            result: True/False
        """
        action = "add"
        send_email = 1
        endpoint = "/msp/user.php"
        payload = f"action={action}&send_email={send_email}"

        users = set(self.current_users)
        if user_details["email"] in users:
            print(f"ERROR: User's email address: {user_details['email']} is a duplicate!")
            dup_user = f"{user_details['email']} {user_details['first_name']} {user_details['last_name']}"
            self.failed_users.append(dup_user)
            return False

        # First, validate the Country Code
        if not self.validateCountryCode(user_details["country"]):
            print(f"ERROR: User has an invalid Country Code: {value}! Please fix their country value!")
            self.failed_users.append(user_details["email"])
            return False
        else:
            # Second, check if the Country Code requires a State
            if user_details["country"] in self.COUNTRIES_WITH_STATES:
                # Third, validate the State and that the State matches the Country
                if not self.validateStateCode(user_details["country"], user_details["state"]):
                    print(f"ERROR: User has an invalid State Code: {user_details['state']} for Country: {user_details['country']}! Please fix their state and/or country value(s)!")
                    self.failed_users.append(user_details["email"])
                    return False
            else:
                # Remove the State altogether if it's not needed
                user_details.pop("state")
        for key, value in user_details.items():
            payload = payload + f"&{key}={value}"
            if key == "email":
                email = value
        result = self._callApi(endpoint, payload, "params")
        if not result:
            self.failed_users.append(email)
            return False
        else:
            self.successful_users.append(email)
            self.current_users.append(email)
            xml = qualysApiXmlParser(result)
            username = xml.parseUserReturn()
            if not username:
                print(f"ERROR: Unable to create User {email}! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {xml.err_msg}")
                self.failed_users.append(email)
                return False
            else:
                self.users_to_tag.append(username)
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
        result = self._callApi(endpoint, payload, "xml")
        if not result:
            return -1
        else:
            xml = qualysApiXmlParser(result)
            if xml.xml_data["ServiceResponse"]["responseCode"] == "SUCCESS":
                count = int(xml.xml_data["ServiceResponse"]["count"])
                while count < 1:
                    print(f"ERROR: Unable to locate the User's ID! This is probably because the user was just created, sleeping for 10s and trying again...")
                    print(xml.xml_data)
                    time.sleep(10)
                    result = self._callApi(endpoint, payload, "xml")
                    if not result:
                        return -1
                    else:
                        xml = qualysApiXmlParser(result)
                        count = int(xml.xml_data["ServiceResponse"]["count"])
                userid = int(xml.xml_data["ServiceResponse"]["data"]["User"]["id"])
                return userid
            else:
                return -1