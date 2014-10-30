[![Build Status](https://travis-ci.org/pnpnpn/street-address.svg?branch=master)](https://travis-ci.org/pnpnpn/street-address)

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


Contribute
------------
I would love for you to fork and send me pull request for this project. Please contribute. 

License
---------
The MIT License (MIT)

Copyright (c) 2012-2014 Patrick Ng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
