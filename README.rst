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
    print addr['house'] #1600
    print addr['street_full'] #Pennsylvania Ave
    print addr['street_name'] #Pennsylvania
    print addr['street_type'] #Ave

    addr = addr_parser.parse("One Union Square, Apt 22-C")
    print addr['house'] #1
    print addr['street_full'] #Union Square
    print addr['street_name'] #Union
    print addr['street_type'] #Square
    print addr['suite_num'] #22-C
    print addr['suite_type'] #Apt

    addr_formatter = StreetAddressFormatter()
    street = 'West 23 Street'
    street = addr_formatter.append_TH_to_street(street) #West 23rd Street
    street = addr_formatter.abbrev_direction(street) #W 23rd Street
    street = addr_formatter.abbrev_street_avenue_etc(street) #W 23rd St

Acknowledgement
---------------

Based on test cases from http://pyparsing.wikispaces.com/file/view/streetAddressParser.py
