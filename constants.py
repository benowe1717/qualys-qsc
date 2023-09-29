#!/usr/bin/env python3

REQUIRED_FIELDS = {
    "user_role": "reader",
    "business_unit": "Unassigned",
    "first_name": "QSC",
    "last_name": "Training",
    "title": "QSC Training 2023",
    "phone": "18007454355",
    "email": "qsc-training@qualys.com",
    "address1": "919 E Hillsdale Blvd, 4th Floor",
    "city": "Foster City",
    "country": "United States of America",
    "state": "California"
}
URL = "https://qualysguard.qg4.apps.qualys.com"
GLOBAL_TAG = "QSC"
NEEDLE = "EC2"
ROLES = [
    "CSAM User", "PATCH USER"
]
TAG_NAME = "qsc-"
OUTPUT_FILE = "mailmerge_database.csv"