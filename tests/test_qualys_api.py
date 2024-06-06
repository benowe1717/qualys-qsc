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
