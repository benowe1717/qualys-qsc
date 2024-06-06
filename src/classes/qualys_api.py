#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth

from src.classes.file_checker import FileChecker
from src.constants import constants


class QualysApi:
    CREDENTIAL_KEYS = constants.QUALYS_API_CREDENTIALS_KEYS
    REQUESTED = constants.QUALYS_API_USER_AGENT
    CONTENT_TYPE = constants.QUALYS_API_CONTENT_TYPE
    SCHEME = constants.QUALYS_API_SCHEME

    def __init__(self, credentials_file: str) -> None:
        self.credentials_file = credentials_file
        self.headers = {
            'X-Requested-With': self.REQUESTED,
            'Content-Type': self.CONTENT_TYPE,
            'Host': self.credentials['host']
        }

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
