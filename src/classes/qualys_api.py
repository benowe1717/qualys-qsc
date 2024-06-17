#!/usr/bin/env python3
import re

import requests
import xmltodict
from requests.auth import HTTPBasicAuth

from src.classes.file_checker import FileChecker
from src.constants import constants


class QualysApi:
    CREDENTIAL_KEYS = constants.QUALYS_API_CREDENTIALS_KEYS
    REQUESTED = constants.QUALYS_API_USER_AGENT
    CONTENT_TYPE = constants.QUALYS_API_CONTENT_TYPE
    SCHEME = constants.QUALYS_API_SCHEME
    REQUIRED_USER_FIELDS = constants.QUALYS_API_REQUIRED_USER_FIELDS
    OPTIONAL_USER_FIELDS = constants.QUALYS_API_OPTIONAL_USER_FIELDS
    USER_ROLES = constants.QUALYS_API_VALID_USER_ROLES
    COUNTRIES = constants.QUALYS_API_VALID_COUNTRY_CODES
    US_STATES = constants.QUALYS_API_VALID_US_STATES
    AUS_STATES = constants.QUALYS_API_VALID_AUS_STATES
    CAN_STATES = constants.QUALYS_API_VALID_CAN_STATES
    IN_STATES = constants.QUALYS_API_VALID_IN_STATES
    USERNAME_FORMAT = constants.QUALYS_API_USERNAME_FORMAT

    def __init__(self, credentials_file: str) -> None:
        self.credentials_file = credentials_file
        self.headers = {
            'X-Requested-With': self.REQUESTED,
            'Content-Type': self.CONTENT_TYPE,
            'Host': self.credentials['host']
        }
        self.users = []
        self.user = []
        self.failed_user = []

    @property
    def credentials_file(self) -> str:
        return self._credentials_file

    @credentials_file.setter
    def credentials_file(self, filepath: str) -> None:
        self._credentials_file = ''
        fc = FileChecker(filepath)
        if not fc.is_file():
            raise ValueError('Not a file')

        if not fc.is_readable():
            raise ValueError('Not readable')

        data = fc.is_yaml()
        if not data:
            raise ValueError('Not YAML')

        try:
            credentials = data['credentials']  # type: ignore
            self._credentials_file = fc.file
            self.credentials = credentials
        except KeyError:
            raise ValueError('Invalid credentials file')

    @property
    def credentials(self) -> dict:
        return self._credentials

    @credentials.setter
    def credentials(self, data: dict) -> None:
        self._credentials = {}
        if len(data) != 3:
            raise ValueError('Invalid credentials file')

        for key in self.CREDENTIAL_KEYS:
            if key not in data.keys():
                raise ValueError(f'Missing {key}!')
        self._credentials = data

    def _basic_auth(self) -> HTTPBasicAuth:
        username = self.credentials['username']
        password = self.credentials['password']
        return HTTPBasicAuth(username, password)

    def _is_valid_user_role(self, role: str) -> bool:
        if role not in self.USER_ROLES:
            return False
        return True

    def _is_valid_asset_group(self, value: str) -> bool:
        pattern = r"^\w+([\,\w]+)?$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_name(self, value: str) -> bool:
        pattern = r"^[A-z0-9\,\.\-\s]{,50}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_title(self, value: str) -> bool:
        pattern = r"^[A-z0-9\,\.\-\s]{,100}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_phone_number(self, number: str) -> bool:
        pattern = r"^[0-9\+\-\(\)\s]{,40}$"
        if not re.match(pattern, number):
            return False
        return True

    def _is_valid_fax(self, value: str) -> bool:
        pattern = r"^\d{,40}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_email(self, email: str) -> bool:
        pattern = r"^[A-z0-9\.\-\_]+\@[A-z0-9\.\-]+\.\w{2,}"
        if not re.match(pattern, email):
            return False
        return True

    def _is_valid_address(self, value: str) -> bool:
        pattern = r"^[A-z0-9\,\.\-\s]{,80}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_city(self, value: str) -> bool:
        pattern = r"^[A-z0-9\,\.\-\s]{,50}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_zip_code(self, value: str) -> bool:
        pattern = r"^\d{,20}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_external_id(self, value: str) -> bool:
        pattern = r"^[A-z]{,256}$"
        if not re.match(pattern, value):
            return False
        return True

    def _is_valid_country(self, country: str) -> bool:
        if country in self.COUNTRIES:
            return True
        return False

    def _is_valid_us_state(self, state: str) -> bool:
        if state in self.US_STATES:
            return True
        return False

    def _is_valid_aus_state(self, state: str) -> bool:
        if state in self.AUS_STATES:
            return True
        return False

    def _is_valid_can_state(self, state: str) -> bool:
        if state in self.CAN_STATES:
            return True
        return False

    def _is_valid_in_state(self, state: str) -> bool:
        if state in self.IN_STATES:
            return True
        return False

    def _validate_payload_values(self, values: dict) -> bool:
        result = self._is_valid_user_role(values['user_role'])
        if not result:
            error = (values, 400, 'Invalid User Role')
            self.failed_user.append(error)
            return False

        if values['user_role'] == 'unit_manager':
            if values['business_unit'] == 'Unassigned':
                error = (values, 400, 'Invalid Business Unit for Unit Manager')
                self.failed_user.append(error)
                return False

        result = self._is_valid_name(values['first_name'])
        if not result:
            error = (values, 400, 'Invalid First Name')
            self.failed_user.append(error)
            return False

        result = self._is_valid_name(values['last_name'])
        if not result:
            error = (values, 400, 'Invalid Last Name')
            self.failed_user.append(error)
            return False

        result = self._is_valid_title(values['title'])
        if not result:
            error = (values, 400, 'Invalid Title')
            self.failed_user.append(error)
            return False

        result = self._is_valid_phone_number(values['phone'])
        if not result:
            error = (values, 400, 'Invalid Phone Number')
            self.failed_user.append(error)
            return False

        result = self._is_valid_email(values['email'])
        if not result:
            error = (values, 400, 'Invalid Email Address')
            self.failed_user.append(error)
            return False

        result = self._is_valid_address(values['address1'])
        if not result:
            error = (values, 400, 'Invalid Street Address')
            self.failed_user.append(error)
            return False

        result = self._is_valid_city(values['city'])
        if not result:
            error = (values, 400, 'Invalid City')
            self.failed_user.append(error)
            return False

        result = self._is_valid_country_and_state(
            values['country'], values['state'])
        if not result:
            error = (values, 400, 'Invalid Country or State')
            self.failed_user.append(error)
            return False

        result = self._is_valid_send_email(values['send_email'])
        if not result:
            error = (values, 400, 'Invalid send_email option')
            self.failed_user.append(error)
            return False

        return True

    def _validate_optional_payload_values(self, values: dict) -> bool:
        if 'asset_groups' in values.keys():
            roles = ['manager', 'unit_manager']
            if values['user_role'] in roles:
                error = (values, 400, 'Invalid User Role with Asset Groups')
                self.failed_user.append(error)
                return False

            result = self._is_valid_asset_group(values['asset_groups'])
            if not result:
                error = (values, 400, 'Invalid Asset Group(s)')
                self.failed_user.append(error)
                return False

        if 'fax' in values.keys():
            result = self._is_valid_fax(values['fax'])
            if not result:
                error = (values, 400, 'Invalid Fax')
                self.failed_user.append(error)
                return False

        if 'address2' in values.keys():
            result = self._is_valid_address(values['address2'])
            if not result:
                error = (values, 400, 'Invalid Street Address')
                self.failed_user.append(error)
                return False

        if 'zip_code' in values.keys():
            result = self._is_valid_zip_code(values['zip_code'])
            if not result:
                error = (values, 400, 'Invalid Zip Code')
                self.failed_user.append(error)
                return False

        if 'external_id' in values.keys():
            result = self._is_valid_external_id(values['external_id'])
            if not result:
                error = (values, 400, 'Invalid External ID')
                self.failed_user.append(error)
                return False

        return True

    def _parse_required_user_fields(self, values: dict) -> dict:
        payload = self.REQUIRED_USER_FIELDS.copy()
        for key in self.REQUIRED_USER_FIELDS.keys():
            if key in values:
                payload[key] = values[key]
        return payload

    def _parse_optional_user_fields(self, values: dict) -> dict:
        payload = {}
        for key in self.OPTIONAL_USER_FIELDS:
            if key in values.keys():
                payload[key] = values[key]
        return payload

    def _detect_bad_keys(self, values: dict) -> bool:
        for key in values.keys():
            if key not in self.REQUIRED_USER_FIELDS.keys(
            ) and key not in self.OPTIONAL_USER_FIELDS:
                print(f'Invalid User Field: {key}')
                return True
        return False

    def _is_valid_country_and_state(self, country: str, state: str) -> bool:
        result = self._is_valid_country(country)
        if not result:
            print(f'Invalid Country: {country}')
            return False

        if country == 'United States of America':
            result = self._is_valid_us_state(state)
            if not result:
                print(f'Invalid State: {state} for Country: {country}')
                return False

        elif country == 'Australia':
            result = self._is_valid_aus_state(state)
            if not result:
                print(f'Invalid State: {state} for Country: {country}')
                return False

        elif country == 'Canada':
            result = self._is_valid_can_state(state)
            if not result:
                print(f'Invalid State: {state} for Country: {country}')
                return False

        elif country == 'India':
            result = self._is_valid_in_state(state)
            if not result:
                print(f'Invalid State: {state} for Country: {country}')
                return False

        return True

    def _is_valid_send_email(self, value: int) -> bool:
        if value == 1 or value == 0:
            return True
        print(f'send_email must be 1 or 0, is: {value}')
        return False

    def _is_valid_username_format(self, username: str) -> bool:
        pattern = r"^" + self.USERNAME_FORMAT + r"[a-z0-9]{3,}"
        if not re.match(pattern, username):
            print(f'Invalid username format: {username}')
            return False
        return True

    def test(self) -> bool:
        endpoint = '/api/2.0/fo/report/?action=list'
        url = self.SCHEME + self.headers['Host'] + endpoint
        r = requests.get(
            url=url,
            headers=self.headers,
            auth=self._basic_auth())
        if r.status_code != 200:
            print(r.status_code, r.text)
            return False
        return True

    def list_users(self) -> bool:
        endpoint = '/msp/user_list.php'
        url = self.SCHEME + self.headers['Host'] + endpoint
        r = requests.get(
            url=url,
            headers=self.headers,
            auth=self._basic_auth())
        if r.status_code != 200:
            error = ('', r.status_code, r.text)
            self.failed_user.append(error)
            print(r.status_code, r.text)
            return False
        else:
            response = xmltodict.parse(r.text)
            try:
                xml_return = response['USER_LIST_OUTPUT']['RETURN']
                if xml_return['@status'] == 'FAILED':
                    code = int(xml_return['@number'])
                    msg = xml_return['MESSAGE']
                    error = ('', code, msg)
                    self.failed_user.append(error)
                    return False
            except KeyError:
                # Qualys does not use the 'RETURN' tag consistently
                # it is there for both success and failure in the Add User
                # and the Reset Password calls, but not the basic User List
                pass

        response = xmltodict.parse(r.text)
        user_list = response['USER_LIST_OUTPUT']['USER_LIST']
        for user in user_list['USER']:
            username = user['USER_LOGIN']
            userid = user['USER_ID']
            email = user['CONTACT_INFO']['EMAIL']
            user_details = (username, userid, email)
            self.users.append(user_details)
        return True

    def add_user(self, **kwargs) -> bool:
        result = self._detect_bad_keys(kwargs)
        if result:
            error = (kwargs, 400, 'Invalid user keys')
            self.failed_user.append(error)
            return False

        payload = self._parse_required_user_fields(kwargs)
        optional_payload = self._parse_optional_user_fields(kwargs)
        if len(optional_payload) > 0:
            payload = {**payload, **optional_payload}

        result = self._validate_payload_values(payload)
        if not result:
            error = (payload, 400, 'Invalid required field(s)')
            self.failed_user.append(error)
            return False

        result = self._validate_optional_payload_values(payload)
        if not result:
            error = (payload, 400, 'Invalid optional field(s)')
            self.failed_user.append(error)
            return False

        endpoint = '/msp/user.php'
        url = self.SCHEME + self.headers['Host'] + endpoint
        r = requests.post(
            url=url,
            headers=self.headers,
            data=payload,
            auth=self._basic_auth())
        if r.status_code != 200:
            error = (payload, r.status_code, r.text)
            self.failed_user.append(error)
            print(r.status_code, r.text)
            return False
        else:
            response = xmltodict.parse(r.text)['USER_OUTPUT']['RETURN']
            if response['@status'] == 'FAILED':
                code = int(response['@number'])
                msg = response['MESSAGE']
                error = (payload, code, msg)
                self.failed_user.append(error)
                return False

        response = xmltodict.parse(r.text)['USER_OUTPUT']['USER']
        if payload['send_email'] == 1:
            user = response['USER_LOGIN']
        else:
            user = (response['USER_LOGIN'], response['PASSWORD'])
        self.user.append(user)
        return True

    def reset_password(self, username: str, email: int) -> bool:
        result = self._is_valid_username_format(username)
        if not result:
            error = (username, 400, 'Invalid username format')
            self.failed_user.append(error)
            return False

        result = self._is_valid_send_email(email)
        if not result:
            error = (email, 400, 'Invalid email option')
            self.failed_user.append(error)
            return False

        payload = {
            'user_logins': username,
            'email': email
        }
        endpoint = '/msp/password_change.php'
        url = self.SCHEME + self.headers['Host'] + endpoint
        r = requests.post(
            url=url,
            headers=self.headers,
            data=payload,
            auth=self._basic_auth())
        if r.status_code != 200:
            error = (payload, r.status_code, r.text)
            self.failed_user.append(error)
            print(r.status_code, r.text)
            return False
        else:
            response = xmltodict.parse(r.text)
            xml_return = response['PASSWORD_CHANGE_OUTPUT']['RETURN']
            if xml_return['@status'] == 'FAILED':
                code = int(xml_return['@number'])
                msg = xml_return['MESSAGE']
                error = (payload, code, msg)
                self.failed_user.append(error)
                return False

        response = xmltodict.parse(r.text)
        xml_return = response['PASSWORD_CHANGE_OUTPUT']['RETURN']['CHANGES']
        user_list = xml_return['USER_LIST']['USER']
        if email == 1:
            user = user_list['USER_LOGIN']
        else:
            user = (user_list['USER_LOGIN'], user_list['PASSWORD'])
        self.user.append(user)
        return True
