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
    BASE_URL = ""
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
                self.BASE_URL = creds["api"]["base_url"]
        except FileNotFoundError:
            print(f"ERROR: Unable to locate {self._CREDS}!")
            print("You either need to create this file and populate it with your credentials or you need to specify the correct path to your credentials on line 23!")
            exit(1)

        try:
            with open(self._SESSION_FILE) as file:
                data = file.readlines()
                self._sessionid = data[0].strip("\n")
        except FileNotFoundError:
            # This simply means the .session_token file has not been created yet, likely implying
            # that a successful login has not occurred yet, this is ok, just trigger another login
            pass
        except IndexError:
            # This likely means that the .session_token file exists but is empty, maybe ran into
            # an error writing to the file, this is also ok, just trigger another login
            pass

        # The following flow will work like this:
        # If the .session_token file is missing or empty
        # assume that this is the first ever login and call
        # the self.login() method, which writes to the .session_token
        
        # Next try to test the API for a 200 response code
        # If this first test fails, it is likely because the .session_token
        # file was read and the session id has expired. call the self.login()
        # method to refresh the session id and try again. if it fails twice
        # then likely the credentials are wrong OR the base domain is wrong

        if not self._sessionid:
            self.login()

        test = self.testAPI()
        if not test:
            print("It looks like your session has expired! Refreshing the session cookie...")
            self.login()
            test = self.testAPI()
            if not test:
                print(f"ERROR: Unable to authenicate to the Qualys API! Please double-check your credentials in {self._CREDS} for accuracy and try again!")
                exit(1)

    def testAPI(self):
        """
            This method is used to test the session id that is either read from the disk or
            genereated by the self.login() method. If this API call returns a 200, we are safe
            to continue and do not need to refresh or recreate a session id.

            output: boolean
            result: True/False
        """
        action = "list"
        endpoint = "/fo/report/"
        url = self.SCHEME + self.BASE_URL + self.API_VERSION + endpoint
        payload = f"action={action}"
        cookies = {"QualysSession": self._sessionid}
        r = requests.post(url=url, headers=self.headers, data=payload, cookies=cookies)
        if r.status_code == 200:
            return True
        else:
            print(f"ERROR: Unable to complete test of the API! Details: Status Code: {r.status_code} :: Response Text: {r.text} :: Headers: {r.headers}")
            return False

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
            self.writeSessionToken(r.headers["Set-Cookie"])
            return True
        elif r.status_code == 401:
            print(f"ERROR: Unable to authenticate to the Qualys API with the user {self._username}!")
            exit(1)
        else:
            print(f"ERROR: Unable to contact the Qualys API!")
            exit(1)

    def writeSessionToken(self, token):
        """
            This method takes the token argument as an input, which is the Session ID/Session Token given
            by the login() method so that user credentials should only have to be passed over the network
            one time, and the rest of the api calls can be done with the appropriate session.

            param: token
            type: string
            sample: QualysSession=abcdef0123456789; path=/somepath; secure; HttpOnly, DWRSESSIONID=abcdef0123456789; path=/somepath; secure

            output: boolean
            result: True
        """
        try:
            with open(self._SESSION_FILE, "w") as file:
                split_token = token.split(";")
                new_split = split_token[0].split("=")
                self._sessionid = new_split[1]
                file.write(self._sessionid)
        except:
            print(f"ERROR: Unable to write Session ID to file!")
            exit(1)