#!/usr/bin/env python3
from urllib.parse import quote
import os, requests, yaml

class qualysApiAuth():
    """
        This class is responsible for authenticating to the Qualys API
        To avoid passing credentials in every single API call, we will be
        using the session-based authentication method. You can expect this
        class to manage the username & password along with the session cookie
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
    _SESSION_FILE = _PATH + "/.session_token"
    _CREDS = _PATH + "/.creds.yaml"

    ########################
    ### PUBLIC CONSTANTS ###
    ########################
    SCHEME = "https://"
    BASE_URL = "qualysapi.qg3.apps.qualys.com/api"
    API_VERSION = "/2.0"

    #######################
    ### PRIVATE OBJECTS ###
    #######################
    _username = ""
    _password = ""
    _sessionid = ""

    ######################
    ### PUBLIC OBJECTS ###
    ######################
    headers = {"X-Requested-With": "Python3Requests", "Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self):
        try:
            with open(self._CREDS, "r") as file:
                creds = yaml.safe_load(file)
                self._username = creds["credentials"]["username"]
                self._password = creds["credentials"]["password"]
        except FileNotFoundError:
            print(f"ERROR: Unable to locate {self._CREDS}!")
            print("You either need to create this file and populate it with your credentials or you need to specify the correct path to your credentials on line 23!")
            exit(1)

        try:
            with open(self._SESSION_FILE) as file:
                self._sessionid = file.readlines()
        except FileNotFoundError:
            pass

        self.login()

    def login(self):
        """
            This method takes the username and password from the self._CREDS file and attempts to
            login to the Qualys API to retrieve a Session Cookie. If the Session Cookie is returned
            we will call the writeSessionToken method to save it and return True. If the call fails for
            any reason, we will return False.

            output: boolean
            result: True
        """
        # https://www.qualys.com/docs/qualys-api-vmpc-user-guide.pdf#G5.741563
        action = "login"
        endpoint = "/fo/session/"
        url = self.SCHEME + self.BASE_URL + self.API_VERSION + endpoint
        payload = f"action={action}&username={self._username}&password={quote(self._password, safe='')}"
        r = requests.post(url=url, headers=self.headers, data=payload)
        if r.status_code == 200:
            self.writeSessionToken(r.headers["SetCookie"])
            return True
        elif r.status_code == 401:
            print(f"ERROR: Unable to authenticate to the Qualys API with the user {self._username}!")
            exit(1)
        else:
            print(f"ERROR: Unable to contact the Qualys API!")
            exit(1)

    def refreshSession(self):
        pass

    def writeSessionToken(self, token):
        pass