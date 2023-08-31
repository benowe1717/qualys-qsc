#!/usr/bin/env python3
from auth import qualysApiAuth
from xml_parser import qualysApiXmlParser
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
    COUNTRIES_WITH_STATES = ["United States of America", "Australia", "Canada", "India"]
    VALID_COUNTRIES = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antartica", "Antigua and Barbuda",
        "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
        "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia-Herzegovina",
        "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria",
        "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands",
        "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia",
        "Comoros", "Congo", "Cook Islands", "Costa Rica", "Cote D'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic",
        "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
        "Equatorial Guinea", "Estonia", "Ethiopia", "Faeroe Islands", "Falkland Islands (Malvinas)", "Fiji", "Finland",
        "France", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia",
        "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guatemala", "Guernsey, C.I.",
        "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and McDonald Islands", "Honduras", "Hong Kong",
        "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland", "Isle of Man", "Israel",
        "Italy", "Jamaica", "Japan", "Jersey, C.I.", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait",
        "Kyrgyzstan", "Lao Peoples Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia",
        "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar",
        "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius",
        "Mexico", "Micronesia, Fed. States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco",
        "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherland Antilles", "Netherlands",
        "Neutral Zone (Saudi/Iraq)", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue",
        "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama Canal Zone",
        "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico",
        "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Samoa", "San Marino",
        "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovak Republic",
        "Slovenia", "Solomon Islands", "Somalia", "South Africa", "Spain", "Sri Lanka", "St. Helena",
        "St. Pierre and Miquelon", "St. Vincent and the Grenadines", "Sudan", "Suriname",
        "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic", "Taiwan",
        "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago",
        "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "U.S.Minor Outlying Islands",
        "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay",
        "Uzbekistan", "Vanuatu", "Vatican City State", "Venezuela", "Vietnam", "Virgin Islands (British)",
        "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zaire", "Zambia", "Zimbabwe",
    ]
    VALID_US_STATES = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "Armed Forces Asia", "Armed Forces Europe", "Armed Forces Pacific",
        "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Hawaii",
        "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
        "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
        "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island","South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]
    VALID_AUS_STATES = [
        "New South Wales", "Northern Territory", "Queensland", "Tasmania", "Victoria", "Western Australia",
    ]
    VALID_CAN_STATES = [
        "Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland",
        "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island", "Quebec",
        "Saskatchewan", "Yukon"
    ]
    VALID_IN_STATES = [
        "Andhra Pradesh", "Andaman and Nicobar Islands", "Arunachal Pradesh", "Assam", "Bihar",
        "Chandigarh", "Chattisgarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana",
        "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadadweep",
        "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Pondicherry",
        "Punjab", "Rajasthan","Sikkim", "Tamil Nadu", "Tripura", "Uttar Pradesh", "Uttaranchal", "West Bengal", "No State"
    ]

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
        # Instantiate the qualysApiAuth() class, which will run all the required authentication checks
        # right out of the gate. If there are any problems authenticating, it will die right here.
        # Otherwise, we continue as normal
        self._auth = qualysApiAuth()

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
        url = self._auth.SCHEME + self._auth.BASE_URL + endpoint
        payload = f"action={action}&send_email={send_email}"

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
        basic = requests.auth.HTTPBasicAuth(self._auth._username, self._auth._password)
        r = requests.post(url=url, headers=self.headers, data=payload, auth=basic)
        if r.status_code == 200:
            xml = qualysApiXmlParser(r.text)
            result = xml.parseUserReturn()
            if not result:
                print(f"ERROR: Unable to create User {email}! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {xml.err_msg}")
                self.failed_users.append(email)
                return False
            else:
                self.successful_users.append(email)
                return True
        else:
            print(f"ERROR: Unable to create User {email}! URL: {url} :: Response Code: {r.status_code} :: Headers: {r.headers} :: Details: {r.text}")
            self.failed_users.append(email)
            return False