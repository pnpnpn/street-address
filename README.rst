street-address
================

Street address parser and formatter



Installation
------------

From source code: ::

    python setup.py install

From pypi: ::

    pip install street-address

Usage
-----
::

    from streetaddress import StreetAddressFormatter, StreetAddressParser

    addr_parser = StreetAddressParser()

    addr = addr_parser.parse("1600 Pennsylvania Ave")
    print addr['house']
    print addr['street_full']
    print addr['street_name']
    print addr['street_type']

    addr = addr_parser.parse("One Union Square, Apt 22-C")
    print addr['house']
    print addr['street_full']
    print addr['street_name']
    print addr['street_type']
    print addr['suite_num']
    print addr['suite_type']

Acknowledgement
---------------

Based on test cases from http://pyparsing.wikispaces.com/file/view/streetAddressParser.py
