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
    _CONFIG = _PATH + "/.creds.yaml"

    ########################
    ### PUBLIC CONSTANTS ###
    ########################
    SCHEME = "https://"
    BASE_URL = ""

    #######################
    ### PRIVATE OBJECTS ###
    #######################
    _auth = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    failed_users = []
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}
    required_fields = ["user_role", "business_unit", "first_name", "last_name", "title", "phone", "email", "address1", "city", "country", "state"]
    successful_users = []

    def __init__(self):
        # Read in the config file to grab the base URL
        try:
            with open(self._CONFIG, "r") as file:
                config = yaml.safe_load(file)
                self.BASE_URL = config["api"]["base_url"].split("/")[0] # the /api is not needed for this class
        except FileNotFoundError:
            print(f"ERROR: Unable to locate {self._CONFIG}!")
            print("You either need to create this file and populate it with your config or you need to specify the correct path to your config on line 23!")
            exit(1)

        # Instantiate the qualysApiAuth() class, which will run all the required authentication checks
        # right out of the gate. If there are any problems authenticating, it will die right here.
        # Otherwise, we continue as normal
        self._auth = qualysApiAuth()

    def addUser(self, user_details):
        """
            https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G17.783431
            https://documenter.getpostman.com/view/7159960/SVzw51A9#52dc0ffe-a2ae-4dea-9cbb-661251477df5
            This method takes in a dictionary of user_details and creates the user in the given Qualys subscription.
            Not all users will have the same details, but there are some required details that will stay the same.

            param: user_details
            type: list
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
        url = self.SCHEME + self.BASE_URL + endpoint
        payload = f"action={action}&send_email={send_email}"
        for key, value in user_details.items():
            payload = payload + f"&{key}={value}"
            if key == "email":
                email = value
        basic = requests.auth.HTTPBasicAuth(self._auth._username, self._auth._password)
        r = requests.post(url=url, headers=self.headers, data=payload, auth=basic)
        if r.status_code == 200:
            self.successful_users.append(email)
            return True
        else:
            print(f"ERROR: Unable to create User {email}! Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
            self.failed_users.append(email)
            return False