import json
import os
import re
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.handlers.snmp_connection import SNMP
from helpers.constants.definitions import snmp_oid


class TestSNMPClass(unittest.TestCase):
    def test_snmp_custom_class(self):
        snmp = SNMP("181.232.180.7")
        print(snmp.execute("next", snmp_oid["descr"], ""))
        pass


if __name__ == "__main__":
    unittest.main()
