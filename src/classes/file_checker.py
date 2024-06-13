#!/usr/bin/env python3
import os

import yaml


class FileChecker:
    def __init__(self, file: str) -> None:
        self.file = file

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, filepath: str) -> None:
        self._file = ''
        if '~' in filepath:
            filepath = os.path.expanduser(filepath)
        try:
            self._file = os.path.realpath(filepath, strict=True)
        except FileNotFoundError:
            dir = os.getcwd()
            parts = os.path.split(filepath)
            head = parts[0].split('./')[-1]
            tail = parts[1]
            filepath = os.path.join(dir, head, tail)
            try:
                self._file = os.path.realpath(filepath, strict=True)
            except FileNotFoundError:
                self._file = ''
                raise ValueError('Unable to locate file')

    def is_file(self) -> bool:
        if not os.path.isfile(self.file):
            return False
        return True

    def is_readable(self) -> bool:
        if not os.access(self.file, os.R_OK):
            return False
        return True

    def is_writable(self) -> bool:
        if not os.access(self.file, os.W_OK):
            return False
        return True

    def is_yaml(self) -> dict | bool:
        try:
            with open(self.file, 'r') as f:
                data = yaml.safe_load(f)
            if isinstance(data, dict):
                return data
            return False
        except yaml.YAMLError:
            return False

    def is_text(self) -> list | bool:
        try:
            with open(self.file, 'r') as f:
                data = [line.strip() for line in f]

            i = 0
            while i < len(data):
                if ',' in data[i]:
                    parts = data[i].split(',')
                    for part in parts:
                        data.append(part)
                    data.pop(i)
                i += 1

            return data
        except BaseException:
            return False
