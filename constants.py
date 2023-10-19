#!/usr/bin/env python3
import sys

LOG_FILE = "qualys-qsc.log"
FORMAT = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
STREAM = sys.stdout

### parseArgs ###
PROGRAM_NAME = "main.py"
PROGRAM_DESCRIPTION = "Qualys QSC Hands-on Training is a `tool` that allows `administrators/trainers` to `provision accounts in a Qualys subscription`."
VERSION = "0.1.9"
AUTHOR = "Benjamin Owen"
REPO = "https://github.com/benowe1717/qualys-qsc"
###

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