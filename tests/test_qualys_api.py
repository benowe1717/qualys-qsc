#!/usr/bin/env python3
import os

import pytest
from requests.auth import HTTPBasicAuth

from src.classes.qualys_api import QualysApi
from src.constants import constants


class TestQualysApi:
    def setUp(self):
        self.credentials_file = 'tests/data/credentials.yaml'
        self.qa = QualysApi(self.credentials_file)

    def tearDown(self):
        del self.qa
        del self.credentials_file

    def test_missing_credentials_file(self):
        file = '/some/fake/file'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_invalid_credentials_file_not_a_file(self):
        file = '~/Documents/'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_invalid_credentials_file_not_readable(self, monkeypatch):
        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)
        file = 'tests/data/credentials.yaml'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_invalid_credentials_file_not_yaml(self):
        file = 'tests/data/not_yaml.yaml'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_invalid_credentials_file_invalid_file(self):
        file = 'tests/data/invalid_credentials.yaml'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_invalid_credentials_file_missing_key(self):
        file = 'tests/data/missing_credentials.yaml'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_invalid_credentials_file_additional_data(self):
        file = 'tests/data/additional_credentials.yaml'
        with pytest.raises(ValueError):
            QualysApi(file)

    def test_credentials_file(self):
        self.setUp()
        assert self.qa.credentials_file == os.path.realpath(
            self.credentials_file)
        assert len(self.qa.credentials) == 3
        assert 'username' in self.qa.credentials.keys()
        assert 'password' in self.qa.credentials.keys()
        assert 'host' in self.qa.credentials.keys()
        self.tearDown()

    def test_headers(self):
        self.setUp()
        assert len(self.qa.headers) == 3
        assert 'X-Requested-With' in self.qa.headers.keys()
        assert 'Content-Type' in self.qa.headers.keys()
        assert 'Host' in self.qa.headers.keys()
        assert self.qa.headers['X-Requested-With'] == 'Python3Requests'
        assert self.qa.headers['Content-Type'] == constants.QUALYS_API_CONTENT_TYPE
        assert self.qa.headers['Host'] == self.qa.credentials['host']
        self.tearDown()

    def test_user_on_startup(self):
        self.setUp()
        assert isinstance(self.qa.user, list)
        assert self.qa.user == []
        self.tearDown()

    def test_users_on_startup(self):
        self.setUp()
        assert isinstance(self.qa.users, list)
        assert len(self.qa.users) == 0
        self.tearDown()

    def test_basic_auth(self):
        self.setUp()
        result = HTTPBasicAuth(
            self.qa.credentials['username'],
            self.qa.credentials['password'])
        assert isinstance(result, HTTPBasicAuth)
        assert self.qa._basic_auth() == result
        self.tearDown()

    def test_test_failed(self, requests_mock):
        self.setUp()
        endpoint = '/api/2.0/fo/report/'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 400
        response = '<?xml version="1.0" encoding="UTF-8" ?>'
        requests_mock.register_uri(
            'GET', url, text=response, status_code=status_code)
        result = self.qa.test()
        assert result is False
        self.tearDown()

    def test_test(self, requests_mock):
        self.setUp()
        endpoint = '/api/2.0/fo/report/'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        response = '<?xml version="1.0" encoding="UTF-8" ?>'
        requests_mock.register_uri(
            'GET', url, text=response, status_code=status_code)
        result = self.qa.test()
        assert result is True
        self.tearDown()

    def test_is_valid_user_role_failed(self):
        self.setUp()
        user_role = 'Director'
        result = self.qa._is_valid_user_role(user_role)
        assert result is False
        self.tearDown()

    def test_is_valid_user_role(self):
        self.setUp()
        user_role = 'scanner'
        result = self.qa._is_valid_user_role(user_role)
        assert result is True
        self.tearDown()

    def test_is_valid_name_failed(self):
        self.setUp()
        name = 'This is not a v@l!d n@m&'
        result = self.qa._is_valid_name(name)
        assert result is False
        self.tearDown()

    def test_is_valid_name(self):
        self.setUp()
        name = 'David'
        result = self.qa._is_valid_name(name)
        assert result is True
        self.tearDown()

    def test_is_valid_title_failed(self):
        self.setUp()
        title = 'Supreme Director of T0t@l @w&$0m&n&$$'
        result = self.qa._is_valid_title(title)
        assert result is False
        self.tearDown()

    def test_is_valid_title(self):
        self.setUp()
        title = 'Program Manager'
        result = self.qa._is_valid_title(title)
        assert result is True
        self.tearDown()

    def test_is_valid_phone_number_failed(self):
        self.setUp()
        pn = '+1.555.867.5309'
        result = self.qa._is_valid_phone_number(pn)
        assert result is False
        self.tearDown()

    def test_is_valid_phone_number(self):
        self.setUp()
        pn = '+15558675309'
        result = self.qa._is_valid_phone_number(pn)
        assert result is True
        self.tearDown()

    def test_is_valid_email_failed(self):
        self.setUp()
        email = 'qualys.com'
        result = self.qa._is_valid_email(email)
        assert result is False
        self.tearDown()

    def test_is_valid_email(self):
        self.setUp()
        email = 'bowen@qualys.com'
        result = self.qa._is_valid_email(email)
        assert result is True
        self.tearDown()

    def test_is_valid_address_failed(self):
        self.setUp()
        address1 = '12 Park Place Ave, 15%'
        result = self.qa._is_valid_address(address1)
        assert result is False
        self.tearDown()

    def test_is_valid_address(self):
        self.setUp()
        address1 = '4020 Westchase Blvd'
        result = self.qa._is_valid_address(address1)
        assert result is True
        self.tearDown()

    def test_is_valid_city_failed(self):
        self.setUp()
        city = 'Another Awesome City of Awesomeness With An Awesomely Long Name'
        result = self.qa._is_valid_city(city)
        assert result is False
        self.tearDown()

    def test_is_valid_city(self):
        self.setUp()
        city = 'Raleigh'
        result = self.qa._is_valid_city(city)
        assert result is True
        self.tearDown()

    def test_is_valid_asset_group_failed(self):
        self.setUp()
        grps = 'grp1, grp2, grp3 grp4 grp5'
        result = self.qa._is_valid_asset_group(grps)
        assert result is False
        self.tearDown()

    def test_is_valid_asset_group_single_group(self):
        self.setUp()
        grps = 'grp1'
        result = self.qa._is_valid_asset_group(grps)
        assert result is True
        self.tearDown()

    def test_is_valid_asset_group_multiple_groups(self):
        self.setUp()
        grps = 'grp1,grp2'
        result = self.qa._is_valid_asset_group(grps)
        assert result is True
        self.tearDown()

    def test_is_valid_fax_failed(self):
        self.setUp()
        fax = '+1.555.867.5309'
        result = self.qa._is_valid_fax(fax)
        assert result is False
        self.tearDown()

    def test_is_valid_fax(self):
        self.setUp()
        fax = '15558675309'
        result = self.qa._is_valid_fax(fax)
        assert result is True
        self.tearDown()

    def test_is_valid_zip_code_failed(self):
        self.setUp()
        zip = 'obv not a zip'
        result = self.qa._is_valid_zip_code(zip)
        assert result is False
        self.tearDown()

    def test_is_valid_zip_code(self):
        self.setUp()
        zip = '25345'
        result = self.qa._is_valid_zip_code(zip)
        assert result is True
        self.tearDown()

    def test_is_valid_external_id_failed(self):
        self.setUp()
        id = '5T>_$N-h{vp11'
        result = self.qa._is_valid_external_id(id)
        assert result is False
        self.tearDown()

    def test_is_valid_external_id(self):
        self.setUp()
        id = 'pkYUrVObwYrSx'
        result = self.qa._is_valid_external_id(id)
        assert result is True
        self.tearDown()

    def test_validate_payload_values_failed(self):
        self.setUp()
        values = {
            'action': 'add',
            'user_role': 'manager',
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'title': 'Program Manager',
            'phone': '1.555.867.5309',
            'email': 'bowen@qualys.com',
            'address1': '4020 Westchase Blvd',
            'city': 'Raleigh',
            'state': 'North Carolina',
            'country': 'United States of America',
            'send_email': 0
        }
        result = self.qa._validate_payload_values(values)
        assert result is False
        assert len(self.qa.failed_user) == 1
        self.tearDown()

    def test_validate_payload_values(self):
        self.setUp()
        values = {
            'action': 'add',
            'user_role': 'manager',
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'title': 'Program Manager',
            'phone': '+15558675309',
            'email': 'bowen@qualys.com',
            'address1': '4020 Westchase Blvd',
            'city': 'Raleigh',
            'state': 'North Carolina',
            'country': 'United States of America',
            'send_email': 0
        }
        result = self.qa._validate_payload_values(values)
        assert result is True
        self.tearDown()

    def test_validate_optional_payload_values_failed_wrong_role(self):
        self.setUp()
        values = {
            'action': 'add',
            'user_role': 'manager',
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'title': 'Program Manager',
            'phone': '+15558675309',
            'email': 'bowen@qualys.com',
            'address1': '4020 Westchase Blvd',
            'city': 'Raleigh',
            'state': 'North Carolina',
            'country': 'United States of America',
            'send_email': 0,
            'asset_groups': 'grp1,grp2,grp3'
        }
        result = self.qa._validate_optional_payload_values(values)
        assert result is False
        assert len(self.qa.failed_user) == 1
        self.tearDown()

    def test_validate_optional_payload_values_failed(self):
        self.setUp()
        values = {
            'action': 'add',
            'user_role': 'manager',
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'title': 'Program Manager',
            'phone': '+15558675309',
            'email': 'bowen@qualys.com',
            'address1': '4020 Westchase Blvd',
            'city': 'Raleigh',
            'state': 'North Carolina',
            'country': 'United States of America',
            'send_email': 0,
            'zip_code': 'my zip code is'
        }
        result = self.qa._validate_optional_payload_values(values)
        assert result is False
        assert len(self.qa.failed_user) == 1
        self.tearDown()

    def test_validate_optional_payload_values(self):
        self.setUp()
        values = {
            'action': 'add',
            'user_role': 'manager',
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'title': 'Program Manager',
            'phone': '+15558675309',
            'email': 'bowen@qualys.com',
            'address1': '4020 Westchase Blvd',
            'city': 'Raleigh',
            'state': 'North Carolina',
            'country': 'United States of America',
            'send_email': 0,
            'fax': '15558675309',
            'zip_code': '24534'
        }
        result = self.qa._validate_optional_payload_values(values)
        assert result is True
        assert len(self.qa.failed_user) == 0
        self.tearDown()

    def test_is_valid_country_failed(self):
        self.setUp()
        country = 'usa'
        result = self.qa._is_valid_country(country)
        assert result is False
        self.tearDown()

    def test_is_valid_country(self):
        self.setUp()
        country = 'Antartica'
        result = self.qa._is_valid_country(country)
        assert result is True
        self.tearDown()

    def test_is_valid_us_state_failed(self):
        self.setUp()
        state = 'utaah'
        result = self.qa._is_valid_us_state(state)
        assert result is False
        self.tearDown()

    def test_is_valid_us_state(self):
        self.setUp()
        state = 'Colorado'
        result = self.qa._is_valid_us_state(state)
        assert result is True
        self.tearDown()

    def test_is_valid_aus_state_failed(self):
        self.setUp()
        state = 'New York'
        result = self.qa._is_valid_aus_state(state)
        assert result is False
        self.tearDown()

    def test_is_valid_aus_state(self):
        self.setUp()
        state = 'New South Wales'
        result = self.qa._is_valid_aus_state(state)
        assert result is True
        self.tearDown()

    def test_is_valid_can_state_failed(self):
        self.setUp()
        state = 'None'
        result = self.qa._is_valid_can_state(state)
        assert result is False
        self.tearDown()

    def test_is_valid_can_state(self):
        self.setUp()
        state = 'Price Edward Island'
        result = self.qa._is_valid_can_state(state)
        assert result is True
        self.tearDown()

    def test_is_valid_in_state_failed(self):
        self.setUp()
        state = 'Ontario'
        result = self.qa._is_valid_in_state(state)
        assert result is False
        self.tearDown()

    def test_is_valid_in_state(self):
        self.setUp()
        state = 'Gujarat'
        result = self.qa._is_valid_in_state(state)
        assert result is True
        self.tearDown()

    def test_detect_bad_keys_one_bad_key(self):
        self.setUp()
        values = {
            'action': 'add',
            'send_email': 1,
            'login': True,
            'user_role': 'reader',
            'business_unit': 'Unassigned'
        }
        result = self.qa._detect_bad_keys(values)
        assert result is True
        self.tearDown()

    def test_detect_bad_keys_multiple_bad_keys(self):
        self.setUp()
        values = {
            'action': 'add',
            'send_email': 1,
            'login': True,
            'user_role': 'reader',
            'business_unit': 'Unassigned',
            'firstname': 'QSC',
            'lastname': 'Training'
        }
        result = self.qa._detect_bad_keys(values)
        assert result is True
        self.tearDown()

    def test_detect_bad_keys_no_bad_keys(self):
        self.setUp()
        values = {
            'action': 'add',
            'send_email': 1,
            'user_role': 'reader',
            'business_unit': 'Unassigned',
            'first_name': 'Benjamin',
            'last_name': 'Owen'
        }
        result = self.qa._detect_bad_keys(values)
        assert result is False
        self.tearDown()

    def test_parse_required_user_fields_single_key(self):
        self.setUp()
        values = {
            'send_email': 1
        }
        result = self.qa._parse_required_user_fields(values)
        assert isinstance(result, dict)
        assert len(result) == 13
        assert result['send_email'] == values['send_email']
        assert result['action'] == 'add'
        self.tearDown()

    def test_parse_required_user_fields_multi_key(self):
        self.setUp()
        values = {
            'send_email': 1,
            'user_role': 'manager',
            'business_unit': 'Unassigned'
        }
        result = self.qa._parse_required_user_fields(values)
        assert isinstance(result, dict)
        assert len(result) == 13
        assert result['send_email'] == values['send_email']
        assert result['user_role'] == values['user_role']
        assert result['business_unit'] == values['business_unit']
        assert result['action'] == 'add'
        self.tearDown()

    def test_parse_optional_user_fields_single_key(self):
        self.setUp()
        values = {
            'zip_code': '12345'
        }
        result = self.qa._parse_optional_user_fields(values)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert result['zip_code'] == values['zip_code']
        self.tearDown()

    def test_parse_optional_user_fields_multi_key(self):
        self.setUp()
        values = {
            'zip_code': '12345',
            'asset_groups': 'grp1,grp2,grp3'
        }
        result = self.qa._parse_optional_user_fields(values)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['zip_code'] == values['zip_code']
        assert result['asset_groups'] == values['asset_groups']
        self.tearDown()

    def test_is_valid_country_and_state_failed_invalid_country(self):
        self.setUp()
        country = 'usa'
        state = 'Virginia'
        result = self.qa._is_valid_country_and_state(country, state)
        assert result is False
        self.tearDown()

    def test_is_valid_country_and_state_invalid_state(self):
        self.setUp()
        country = 'Canada'
        state = 'Virginia'
        result = self.qa._is_valid_country_and_state(country, state)
        assert result is False
        self.tearDown()

    def test_is_valid_country_and_state(self):
        self.setUp()
        country = 'United States of America'
        state = 'Virginia'
        result = self.qa._is_valid_country_and_state(country, state)
        assert result is True
        self.tearDown()

    def test_is_valid_send_email_failed(self):
        self.setUp()
        send_email = '1'
        result = self.qa._is_valid_send_email(send_email)  # type: ignore
        assert result is False
        self.tearDown()

    def test_is_valid_send_email(self):
        self.setUp()
        send_email = 1
        result = self.qa._is_valid_send_email(send_email)
        assert result is True
        self.tearDown()

    def test_add_user_failed_bad_key(self):
        self.setUp()
        values = {
            'firstname': 'Benjamin',
            'lastname': 'Owen'
        }
        result = self.qa.add_user(**values)
        assert result is False
        self.tearDown()

    def test_add_user_failed_bad_country(self):
        self.setUp()
        values = {
            'send_email': 1,
            'country': 'USA',
            'state': 'North Carolina',
            'city': 'Raleigh'
        }
        result = self.qa.add_user(**values)
        assert result is False
        self.tearDown()

    def test_add_user_failed_bad_state(self):
        self.setUp()
        values = {
            'send_email': 1,
            'country': 'Canada',
            'state': 'North Carolina',
            'city': 'Raleigh'
        }
        result = self.qa.add_user(**values)
        assert result is False
        self.tearDown()

    def test_add_user_failed_invalid_send_email(self):
        self.setUp()
        values = {
            'send_email': '1',
            'country': 'United States of America',
            'state': 'North Carolina',
            'city': 'Raleigh'
        }
        result = self.qa.add_user(**values)
        assert result is False
        self.tearDown()

    def test_add_user_failed_wrong_send_email(self):
        self.setUp()
        values = {
            'send_email': 2,
            'country': 'United States of America',
            'state': 'North Carolina',
            'city': 'Raleigh'
        }
        result = self.qa.add_user(**values)
        assert result is False
        self.tearDown()

    def test_add_user_failed(self, requests_mock):
        self.setUp()
        values = {}
        endpoint = '/msp/user.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 400
        with open('tests/data/invalid_xml_response.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.add_user(**values)
        assert result is False
        assert len(self.qa.user) == 0
        assert len(self.qa.failed_user) == 1
        for x in self.qa.failed_user:
            assert isinstance(x[0], dict)
            assert x[0]['email'] == 'qsc-training@qualys.com'
            assert isinstance(x[1], int)
            assert x[1] == 400
        self.tearDown()

    def test_add_user_add_one_user_defaults(self, requests_mock):
        self.setUp()
        values = {}
        endpoint = '/msp/user.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/xml_response.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.add_user(**values)
        assert result is True
        assert len(self.qa.user) == 1
        assert isinstance(self.qa.user[0], tuple)
        assert self.qa.user[0][0] == 'quays6qt84'
        assert self.qa.user[0][1] == 'lWby3dX#'
        self.tearDown()

    def test_add_user_add_one_user_override_defaults(self, requests_mock):
        self.setUp()
        values = {
            'action': 'add',
            'user_role': 'manager',
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'title': 'Program Manager',
            'phone': '15558675309',
            'email': 'bowen@qualys.com',
            'address1': '4020 Westchase Blvd',
            'city': 'Raleigh',
            'state': 'North Carolina',
            'send_email': 1
        }
        endpoint = '/msp/user.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/xml_response.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.add_user(**values)
        assert result is True
        assert len(self.qa.user) == 1
        assert isinstance(self.qa.user[0], str)
        assert self.qa.user[0] == 'quays6qt84'
        self.tearDown()

    def test_add_user_add_one_user_some_overrides(self, requests_mock):
        self.setUp()
        values = {
            'business_unit': 'QSC',
            'first_name': 'Benjamin',
            'last_name': 'Owen',
            'email': 'bowen@qualys.com',
        }
        endpoint = '/msp/user.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/xml_response.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.add_user(**values)
        assert result is True
        assert len(self.qa.user) == 1
        assert isinstance(self.qa.user[0], tuple)
        assert self.qa.user[0][0] == 'quays6qt84'
        assert self.qa.user[0][1] == 'lWby3dX#'
        self.tearDown()

    def test_add_user_add_multiple_users_defaults(self, requests_mock):
        self.setUp()
        values = {}
        with open('tests/data/xml_response.xml', 'r') as file:
            data = file.read()
        total = 3
        i = 0
        while i < total:
            endpoint = '/msp/user.php'
            host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
            url = host + endpoint
            status_code = 200
            with open('tests/data/xml_response.xml', 'r') as file:
                data = file.read()
            requests_mock.register_uri(
                'POST', url, text=data, status_code=status_code)
            result = self.qa.add_user(**values)
            assert result is True
            i += 1
        assert len(self.qa.user) == 3
        assert isinstance(self.qa.user[0], tuple)
        assert self.qa.user[0][0] == 'quays6qt84'
        assert self.qa.user[0][1] == 'lWby3dX#'
        self.tearDown()

    def test_add_user_add_multiple_users_override_defaults(
            self, requests_mock):
        self.setUp()
        with open('tests/data/xml_response.xml', 'r') as file:
            data = file.read()
        total = 3
        i = 0
        names = [
            ('Benjamin',
             'Owen',
             'bowen@qualys.com', 'scanner', 'Program Manager'),
            ('Ryan',
             'Armstrong',
             'rarmstrong@qualys.com', 'scanner', 'Senior Manager'),
            ('Kevin',
             'Jones',
             'kjones@qualys.com', 'manager', 'Director')]
        while i < total:
            values = {
                'action': 'add',
                'user_role': names[i][3],
                'business_unit': 'QSC',
                'first_name': names[i][0],
                'last_name': names[i][1],
                'title': names[i][4],
                'phone': '15558675309',
                'email': names[i][2],
                'address1': '4020 Westchase Blvd',
                'city': 'Raleigh',
                'state': 'North Carolina',
                'send_email': 1
            }
            endpoint = '/msp/user.php'
            host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
            url = host + endpoint
            status_code = 200
            with open('tests/data/xml_response.xml', 'r') as file:
                data = file.read()
            requests_mock.register_uri(
                'POST', url, text=data, status_code=status_code)
            result = self.qa.add_user(**values)
            assert result is True
            i += 1
        assert len(self.qa.user) == 3
        assert isinstance(self.qa.user[0], str)
        assert self.qa.user[0] == 'quays6qt84'
        self.tearDown()

    def test_add_user_add_multiple_users_some_overrides(self, requests_mock):
        self.setUp()
        with open('tests/data/xml_response.xml', 'r') as file:
            data = file.read()
        total = 3
        i = 0
        names = [
            ('Benjamin',
             'Owen',
             'bowen@qualys.com', 'scanner', 'Program Manager'),
            ('Ryan',
             'Armstrong',
             'rarmstrong@qualys.com', 'scanner', 'Senior Manager'),
            ('Kevin',
             'Jones',
             'kjones@qualys.com', 'manager', 'Director')]
        while i < total:
            values = {
                'business_unit': 'QSC',
                'first_name': names[i][0],
                'last_name': names[i][1],
                'title': names[i][4],
                'email': names[i][2],
            }
            endpoint = '/msp/user.php'
            host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
            url = host + endpoint
            status_code = 200
            with open('tests/data/xml_response.xml', 'r') as file:
                data = file.read()
            requests_mock.register_uri(
                'POST', url, text=data, status_code=status_code)
            result = self.qa.add_user(**values)
            assert result is True
            i += 1
        assert len(self.qa.user) == 3
        assert isinstance(self.qa.user[0], tuple)
        assert self.qa.user[0][0] == 'quays6qt84'
        assert self.qa.user[0][1] == 'lWby3dX#'
        self.tearDown()

    def test_is_valid_username_format_failed(self):
        self.setUp()
        username = 'my_username'
        result = self.qa._is_valid_username_format(username)
        assert result is False
        self.tearDown()

    def test_is_valid_username_format(self):
        self.setUp()
        username = 'quays7cx25'
        result = self.qa._is_valid_username_format(username)
        assert result is True
        self.tearDown()

    def test_reset_password_failed_unauthenticated(self, requests_mock):
        self.setUp()
        username = 'quays8dy36'
        email = 0
        endpoint = '/msp/password_change.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 401
        requests_mock.register_uri(
            'POST', url, text='ACCESS DENIED', status_code=status_code)
        result = self.qa.reset_password(username, email)
        assert result is False
        assert len(self.qa.failed_user) == 1
        self.tearDown()

    def test_reset_password_failed(self, requests_mock):
        self.setUp()
        username = 'quays8dy36'
        email = 0
        endpoint = '/msp/password_change.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/password_change_failed.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.reset_password(username, email)
        assert result is False
        assert len(self.qa.failed_user) == 1
        self.tearDown()

    def test_reset_password_single_user_send_email(self, requests_mock):
        self.setUp()
        username = 'quays7cx25'
        email = 1
        endpoint = '/msp/password_change.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/password_change_email.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.reset_password(username, email)
        assert result is True
        assert len(self.qa.user) == 1
        assert isinstance(self.qa.user[0], str)
        assert self.qa.user[0] == username
        self.tearDown()

    def test_reset_password_single_user_no_send_email(self, requests_mock):
        self.setUp()
        username = 'quays7cx25'
        email = 0
        endpoint = '/msp/password_change.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/password_change_no_email.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        result = self.qa.reset_password(username, email)
        assert result is True
        assert len(self.qa.user) == 1
        assert isinstance(self.qa.user[0], tuple)
        assert self.qa.user[0][0] == username
        assert self.qa.user[0][1] == 'password1!'
        self.tearDown()

    def test_reset_password_multiple_users(self, requests_mock):
        self.setUp()
        usernames = ['quays7cx25', 'quays8dy36', 'quays9ez47']
        email = 0
        endpoint = '/msp/password_change.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/password_change_no_email.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'POST', url, text=data, status_code=status_code)
        for username in usernames:
            result = self.qa.reset_password(username, email)
            assert result is True
        assert len(self.qa.user) == 3
        assert isinstance(self.qa.user[0], tuple)
        assert self.qa.user[0][0] == usernames[0]
        assert self.qa.user[0][1] == 'password1!'
        self.tearDown()

    def test_list_users_failed_unauthenticated(self, requests_mock):
        self.setUp()
        endpoint = '/msp/user_list.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 401
        requests_mock.register_uri(
            'GET',
            url,
            text='ACCESS DENIED',
            status_code=status_code)
        result = self.qa.list_users()
        assert result is False
        assert len(self.qa.users) == 0
        self.tearDown()

    def test_list_users_failed(self, requests_mock):
        self.setUp()
        endpoint = '/msp/user_list.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/list_users_failed.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.qa.list_users()
        assert result is False
        assert len(self.qa.users) == 0
        self.tearDown()

    def test_list_users(self, requests_mock):
        self.setUp()
        endpoint = '/msp/user_list.php'
        host = constants.QUALYS_API_SCHEME + self.qa.headers['Host']
        url = host + endpoint
        status_code = 200
        with open('tests/data/list_users.xml', 'r') as file:
            data = file.read()
        requests_mock.register_uri(
            'GET', url, text=data, status_code=status_code)
        result = self.qa.list_users()
        assert result is True
        assert len(self.qa.users) == 2
        self.tearDown()
