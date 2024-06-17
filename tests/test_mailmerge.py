#!/usr/bin/env python3
import os

import pytest

from src.classes.mailmerge import MailMerge


class TestMailMerge:
    def setUp(self):
        self.conf_file = 'tests/data/mailmerge_server.conf'
        self.template_file = 'tests/data/mailmerge_template.txt'
        self.database_file = 'tests/data/mailmerge_database.csv'
        self.mailmerge = MailMerge(
            self.conf_file,
            self.template_file,
            self.database_file)

    def tearDown(self):
        del self.mailmerge
        del self.database_file
        del self.template_file
        del self.conf_file

    def test_is_valid_conf_file_failed_unconfigured(self):
        self.setUp()
        conf_file = 'tests/data/mailmerge_server_unconfigured.conf'
        result = self.mailmerge._is_valid_conf_file(conf_file)
        assert result is False
        self.tearDown()

    def test_is_valid_conf_file_failed_invalid(self):
        self.setUp()
        conf_file = 'tests/data/mailmerge_server_invalid.conf'
        result = self.mailmerge._is_valid_conf_file(conf_file)
        assert result is False
        self.tearDown()

    def test_is_valid_conf_file(self):
        self.setUp()
        conf_file = 'tests/data/mailmerge_server.conf'
        result = self.mailmerge._is_valid_conf_file(conf_file)
        assert result is True
        self.tearDown()

    def test_conf_file_failed_not_found(self):
        self.setUp()
        conf_file = '/some/fake/file.conf'
        with pytest.raises(ValueError):
            MailMerge(conf_file, self.template_file, self.database_file)
        self.tearDown()

    def test_conf_file_failed_not_a_file(self):
        self.setUp()
        conf_file = 'tests/data'
        with pytest.raises(ValueError):
            MailMerge(conf_file, self.template_file, self.database_file)
        self.tearDown()

    def test_conf_file_failed_not_readable(self):
        self.setUp()
        conf_file = '/swapfile'
        with pytest.raises(ValueError):
            MailMerge(conf_file, self.template_file, self.database_file)
        self.tearDown()

    def test_conf_file(self):
        self.setUp()
        path = '/home/benjamin/Documents/qualys/qualys-qsc/tests/data'
        file = '/mailmerge_server.conf'
        filepath = path + file
        assert self.mailmerge.conf_file == filepath
        self.tearDown()

    def test_is_valid_template_file_failed_blank(self):
        self.setUp()
        template_file = 'tests/data/empty_template.txt'
        result = self.mailmerge._is_valid_template_file(template_file)
        assert result is False
        self.tearDown()

    def test_is_valid_template_file_missing_key(self):
        self.setUp()
        template_file = 'tests/data/invalid_template.txt'
        result = self.mailmerge._is_valid_template_file(template_file)
        assert result is False
        self.tearDown()

    def test_is_valid_template_file(self):
        self.setUp()
        template_file = 'tests/data/mailmerge_template.txt'
        result = self.mailmerge._is_valid_template_file(template_file)
        assert result is True
        self.tearDown()

    def test_template_file_failed_not_found(self):
        self.setUp()
        template_file = '/some/fake/template_file.txt'
        with pytest.raises(ValueError):
            MailMerge(self.conf_file, template_file, self.database_file)
        self.tearDown()

    def test_template_file_failed_not_a_file(self):
        self.setUp()
        template_file = 'tests/data'
        with pytest.raises(ValueError):
            MailMerge(self.conf_file, template_file, self.database_file)
        self.tearDown()

    def test_template_file_failed_not_readable(self):
        self.setUp()
        template_file = '/swapfile'
        with pytest.raises(ValueError):
            MailMerge(self.conf_file, template_file, self.database_file)
        self.tearDown()

    def test_template_file(self):
        self.setUp()
        path = '/home/benjamin/Documents/qualys/qualys-qsc/tests/data'
        file = '/mailmerge_template.txt'
        filepath = path + file
        assert self.mailmerge.template_file == filepath
        self.tearDown()

    def test_is_valid_database_file_failed_empty_file(self):
        self.setUp()
        database_file = 'tests/data/empty_database.csv'
        result = self.mailmerge._is_valid_database_file(database_file)
        assert result is False
        self.tearDown()

    def test_is_valid_database_file_failed_missing_key(self):
        self.setUp()
        database_file = 'tests/data/invalid_database.csv'
        result = self.mailmerge._is_valid_database_file(database_file)
        assert result is False
        self.tearDown()

    def test_is_valid_database_file_failed_bad_delimiter(self):
        self.setUp()
        database_file = 'tests/data/bad_delimiter_database.csv'
        result = self.mailmerge._is_valid_database_file(database_file)
        assert result is False
        self.tearDown()

    def test_is_valid_database_file(self):
        self.setUp()
        database_file = 'tests/data/mailmerge_database.csv'
        result = self.mailmerge._is_valid_database_file(database_file)
        assert result is True
        self.tearDown()

    def test_database_file_failed_not_found(self):
        self.setUp()
        database_file = '/some/fake/database_file.csv'
        with pytest.raises(ValueError):
            MailMerge(self.conf_file, self.template_file, database_file)
        self.tearDown()

    def test_database_file_failed_not_readable(self):
        self.setUp()
        database_file = '/swapfile'
        with pytest.raises(ValueError):
            MailMerge(self.conf_file, self.template_file, database_file)
        self.tearDown()

    def test_database_file_failed_not_writable(self, monkeypatch):
        self.setUp()

        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)
        with pytest.raises(ValueError):
            MailMerge(self.conf_file, self.template_file, self.database_file)
        self.tearDown()

    def test_database_file(self):
        self.setUp()
        path = '/home/benjamin/Documents/qualys/qualys-qsc/tests/data'
        file = '/mailmerge_database.csv'
        filepath = path + file
        assert self.mailmerge.database_file == filepath
        self.tearDown()
