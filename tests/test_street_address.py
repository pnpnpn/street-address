import unittest

from nose.tools import *
from streetaddress import StreetAddressFormatter, StreetAddressParser

class TestStreetAddress(unittest.TestCase):
    def setUp(self):
        self.addr_parser = StreetAddressParser()
        self.addr_formatter = StreetAddressFormatter()


    def test_success_abbrev_street_avenue_etc(self):
        addr = self.addr_parser.parse('221B Baker Street')
        eq_(self.addr_formatter.abbrev_street_avenue_etc(addr['street_full']), 'Baker St')

