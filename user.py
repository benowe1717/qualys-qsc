#!/usr/bin/env python3
from auth import qualysApiAuth
from urllib.parse import quote
import os, requests, yaml

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
    _CONFIG = _PATH + "/config.yaml"

    ########################
    ### PUBLIC CONSTANTS ###
    ########################
    SCHEME = "https://"
    BASE_URL = "qualysapi.qg3.apps.qualys.com"

    #######################
    ### PRIVATE OBJECTS ###
    #######################
    _auth = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    subscription = ""

    def __init__(self):
        # Instantiate the qualysApiAuth() class, which will run all the required authentication checks
        # right out of the gate. If there are any problems authenticating, it will die right here.
        # Otherwise, we continue as normal
        self._auth = qualysApiAuth()

    def addUser(self, user_details):
        """
            This method takes in a dictionary of user_details and creates the user in the given Qualys subscription.
            Not all users will have the same details, but there are some required details that will stay the same.

            param: user_details
            type: list
            sample: {
                user_role: "role", business_unit: "unit", first_name: "fname", last_name: "lname", title: "title",
                phone: 1112223333, email: "name@domain.tld", address1: "1 Main Street", city: "Park Place",
                country: "US", state: "MN"
            }

            output: boolean
            result: True/False
        """
        action = "add"
        send_email = 1
        endpoint = "/msp/user.php"
        url = self.SCHEME + self.BASE_URL + endpoint
        payload = f"action={action}&send_email={send_email}"
        for key, value in user_details.items():
            payload = payload + f"&{key}={value}"
            if key == "email":
                email = value
        basic = requests.auth.HTTPBasicAuth(self._auth._username, self._auth._password)
        r = requests.post(url=url, headers=self.headers, data=payload, auth=basic)
        if r.status_code == 200:
            return True
        else:
            print(f"ERROR: Unable to create User {value}! Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
            return False