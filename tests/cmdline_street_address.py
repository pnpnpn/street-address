#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import unittest
from optparse import OptionParser
from streetaddress import StreetAddressFormatter, StreetAddressParser



########################################################################
# Test
########################################################################
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-8s %(levelname)-8s %(message)s',
                        datefmt='%H:%M:%S'
                        )
    usage = """Usage: %prog [options]

Examples:
    ./%prog --addr="366 West 52nd Street  New York, NY 10019" 
    ./%prog --addr="135-20 40th ROAD, queens, NY 11354"
    ./%prog --addr="22-15 31st St, 11105"

    """
    optp = OptionParser(usage=usage)

    optp.add_option('--addr', help='address to parse',
            action='store', type='string', dest="addr", default=None)
    opts, args = optp.parse_args()

    #if not opts.addr:
    #    optp.error('addr must be specified')
    #orig_addr = opts.addr 

    tests = """\
        3120 De la Cruz Boulevard
        100 South Street
        123 Main
        221B Baker Street
        10 Downing St
        1600 Pennsylvania Ave
        33 1/2 W 42nd St.
        454 N 38 1/2
        21A Deer Run Drive
        256K Memory Lane
        12-1/2 Lincoln
        23N W Loop South
        23 N W Loop South
        25 Main St
        2500 14th St
        12 Bennet Pkwy
        Pearl St
        Bennet Rd and Main St
        19th St
        1500 Deer Creek Lane
        2081 N Webb Rd
        2081 N. Webb Rd
        1515 West 22nd Street
        2029 Stierlin Court
        P.O. Box 33170
        The Landmark @ One Market, Suite 200
        One Market, Suite 200
        One Market
        One Union Square
        One Union Square, Apt 22-C
        186 Avenue A
        10 Avenue of America
        25 West St
        """.split("\n")

    addr_parser = StreetAddressParser()
    addr_formatter = StreetAddressFormatter()

    if opts.addr:
        lst = [opts.addr]
    else:
        lst = map(str.strip,tests)

    for t in lst:
        if t:
            print '"%s"' % t
            logging.info('addr_str: ' + unicode(t))
            addr = addr_parser.parse(t)

            if addr['street_full'] is not None:
                street = addr_formatter.append_TH_to_street(addr['street_full'])
                logging.info('After append_TH_to_street: ' + street)

                street = addr_formatter.abbrev_direction(street)
                logging.info('After abbrev_direction: ' + street)

                street = addr_formatter.abbrev_street_avenue_etc(street)
                logging.info('After abbrev_street_avenue_etc: ' + street)

                street = addr_formatter.abbrev_street_avenue_etc(street, abbrev_only_last_token=False)
                logging.info('After abbrev_street_avenue_etc (aggressive): ' + street)

            print json.dumps(addr, sort_keys=True)

