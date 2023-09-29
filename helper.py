#!/usr/bin/env python3
import constants
from auth import qualysApiAuth
import requests, xmltodict

class qualysApiHelper():
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
    _auth = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    failed_users = []
    successful_users = []
    users_to_tag = []
    user_details = []

    def __init__(self):
        # Instantiate the qualysApiAuth() class, which will run all
        # the required authentication checks right out of the gate. 
        # If there are any problems authenticating, it will die right here.
        # Otherwise, we continue as normal
        self._auth = qualysApiAuth()

    def callApi(self, endpoint, payload=None, request_type=None):
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