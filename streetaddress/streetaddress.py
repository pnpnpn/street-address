#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    streetaddress.streetaddress
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by PN.
    :license: MIT, see LICENSE for more details.
"""

import time
import logging
import sys
import re
import json
from optparse import OptionParser


########################################################################
# StreetAddressParser
########################################################################

class StreetAddressParser():
    def __init__(self):
        abbrev_suffix_map = get_abbrev_suffix_dict()
        self.street_type_set = set(abbrev_suffix_map.keys() + abbrev_suffix_map.values())

        self.text2num_dict = get_text2num_dict()
        self.suite_type_set = set([
            'suite', 'ste', 'apt','apartment', 
            'room', 'rm', '#',
            ])
        self.rec_st_nd_rd_th = re.compile(r'^\d+(st|nd|rd|th)$', flags=re.I|re.U)
        self.rec_house_number = re.compile(r'^\d\S*$', flags=re.I|re.U)

    def parse(self, addr_str, skip_house=False):
        addr_str = addr_str.strip()
        res = {
                'house' : None,
                'street_name' : None,
                'street_type' : None,
                'street_full' : None,
                'suite_num' : None,
                'suite_type' : None,
                'other' : None,
                }

        tokens = addr_str.split()
        start_idx = 0

        if len(tokens) == 0:
            return res

        if skip_house:
            start_idx = 0
        else:
            if tokens[0].lower() in self.text2num_dict:
                res['house'] = unicode(self.text2num_dict[tokens[0].lower()])
                start_idx = 1
            elif self.rec_st_nd_rd_th.search(tokens[0]):
                #first token is actually a street number (not house)
                start_idx = 0 
            elif self.rec_house_number.search(tokens[0]):
                res['house'] = tokens[0] 
                start_idx = 1
            else:
                #no house number
                start_idx = 0

            if res['house'] and len(tokens) >= 2 and tokens[1] == '1/2':
                res['house'] += ' ' + tokens[1] 
                start_idx = 2

        street_accum = []
        other_accum = []
        is_in_state = 'street' #can be 'street', 'suite', 'other'

        for i in range(start_idx, len(tokens)):
            word = tokens[i]
            #word = re.sub(r'[\.\,]+$', '', word, flags=re.I|re.U) 
            while len(word) > 0 and (word[-1] == '.' or word[-1] == ','):
                #truncate the trailing dot (for abbrev)
                word = word[:-1]
            word_lw = word.lower()

            if word_lw in self.street_type_set and len(street_accum) > 0:
                res['street_type'] = word
                is_in_state = 'other'
            elif word_lw in self.suite_type_set:
                res['suite_type'] = word
                is_in_state = 'suite'
            elif len(word_lw) > 0 and word_lw[0] == '#' and res['suite_num'] is not None:
                res['suite_type'] = '#'
                res['suite_num'] = word[1:]
                is_in_state = 'other'
            elif is_in_state == 'street':
                street_accum.append(word)
            elif is_in_state == 'suite':
                res['suite_num'] = word
                is_in_state = 'other'
            elif is_in_state == 'other': 
                other_accum.append(word)
            else:
                raise Exception('this state should never be reached')

        # TODO PO Box handling
        #acronym = lambda s : Regex(r"\.?\s*".join(s)+r"\.?")
        #poBoxRef = ((acronym("po") | acronym("apo") | acronym("afp")) + 
        #            Optional(CaselessLiteral("BOX"))) + Word(alphanums)("boxnumber")

        if street_accum:
            res['street_name'] = ' ' . join(street_accum)
        if other_accum:
            res['other'] = ' ' . join(other_accum)

        if res['street_name'] and res['street_type']:
            res['street_full'] = res['street_name'] + ' ' + res['street_type']
        elif res['street_name']:
            res['street_full'] = res['street_name'] 
        elif res['street_type']:
            res['street_full'] = res['street_type'] 

        return res

def get_abbrev_suffix_dict():
    return {
            'avenue' : 'ave',
            'street' : 'st',
            'boulevard': 'blvd',
            'parkway': 'pkwy',
            'highway': 'hwy',
            'drive': 'dr',
            'place': 'pl',
            'expressway': 'expy',
            'heights': 'hts',
            'junction' : 'jct',
            'center': 'ctr',
            'circle' : 'cir',
            'cove' : 'cv',
            'lane' : 'ln',
            'road' : 'rd',
            'court' : 'ct',
            'square' : 'sq',
            'loop' : 'lp',
            }



def get_text2num_dict():
    return  {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'thirty': 30,
        'forty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90,
        } 


########################################################################
# StreetAddressFormatter
########################################################################
class StreetAddressFormatter():
    def __init__(self):
        #abbreviate west, east, north, south?
        self.abbrev_suffix_map = get_abbrev_suffix_dict()
        self.street_type_set = set(self.abbrev_suffix_map.keys() + self.abbrev_suffix_map.values())
        self.abbrev_direction_map = {
            'east' : 'E',
            'west' : 'W', 
            'north' : 'N',
            'south' : 'S',
            }

        for k,v in self.abbrev_suffix_map.items():
            self.abbrev_suffix_map[k] = v.title()

        TH_or_str = '|' . join(self.street_type_set)
        self.re_TH= re.compile(r'\b(\d+)\s+(%s)\.?$' % TH_or_str, flags=re.I|re.U)

    def st_nd_th_convert(self, num_str):
        if num_str[-1] == '1':
            return num_str + 'st'
        elif num_str[-1] == '2':
            return num_str + 'nd'
        elif num_str[-1] == '3':
            return num_str + 'rd'
        else:
            return num_str + 'th'

    def append_TH_to_street(self, addr):
        #street,avenue needs to be the last word
        addr = addr.strip()
        match = self.re_TH.search(addr)
        if match:
            repl = '%s %s' % (self.st_nd_th_convert(match.group(1)), match.group(2))
            addr = addr.replace(match.group(0), repl)
        return addr

    def abbrev_direction(self, addr):
        word_lst = addr.split()
        if len(word_lst) == 0:
            return addr

        for i in range(len(word_lst) - 1):
            word = word_lst[i].lower() 
            #should have a digit after direction, e.g. "West 23rd" 
            if word in self.abbrev_direction_map and word_lst[i+1][0].isdigit():
                word_lst[i] = self.abbrev_direction_map[word]
        addr = ' ' . join(word_lst)
        return addr

    def abbrev_street_avenue_etc(self, addr, abbrev_only_last_token=True):
        word_lst = addr.split()
        if len(word_lst) == 0:
            return addr

        if abbrev_only_last_token:
            pos_lst = [-1]
        else:
            pos_lst = range(len(word_lst))

        for p in pos_lst:
            word = re.sub(r'\.$', '', word_lst[p]).lower() #get rid of trailing period
            if word in self.abbrev_suffix_map:
                word_lst[p] = self.abbrev_suffix_map[word]
        addr = ' ' . join(word_lst)
        return addr


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
            #addr = streetAddress.parseString(t, parseAll=True)
            #print "Number:", addr.street.number
            #print "Street:", addr.street.name
            #print "Type:", addr.street.type
            #if addr.street.boxnumber:
            #    print "Box:", addr.street.boxnumber
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

