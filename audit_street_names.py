# -*- coding: utf-8 -*-

'''
This script is based on lesson material from Udacity's MongoDB course but
rewritten and repurposed the the choosen data set and use case.
'''

import xml.etree.cElementTree as ET
import re
import sys

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Array containing expected street names for our data
expected = [u'gatan', u'vägen', u' gata', u' väg', u'väg', u'backen',
            u'gården', u'gård', u'plan', u'bro', u'torp', u'allén', u'allé',
            u'Industriområde']

# Mapping between abbriviations and full lenght words
mapping = {}


def audit_street_type(unknown_street_types, street_name):
    '''
    Function used check if the provided street_name's street type is contained
    in the expected street names array. If not add the street_name to the
    provided unknown_street_types set.
    '''
    unknown = True

    for expected_end in expected:
        if street_name.endswith(expected_end):
            unknown = False

    if unknown:
        unknown_street_types.add(street_name)


def is_street_name(elem):
    '''
    Function checking if the provided osm element (elem) is a street or not.
    '''
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    '''
    Function that checks the osm data we give as an argument to our script and
    writes out all the different street types not present in the expected
    street name array.
    '''
    osm_file = open(osmfile, "r")
    unknown_street_types = set()

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(unknown_street_types, tag.attrib['v'])

    osm_file.close()

    return unknown_street_types


def update_name(name, mapping):
    '''
    Updates street names based on the mapping dictionary defined at the top of
    the script.
    '''
    for key in mapping.keys():
        if key in name:
            name = name.replace(key, mapping[key])
            break

    return name


def main(argv):
    unknown_streets = audit(argv)

    for street in unknown_streets:
        print street


if __name__ == "__main__":
    main(sys.argv[1])
