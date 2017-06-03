# -*- coding: utf-8 -*-

'''
This script is based on lesson material from Udacity's MongoDB course but
rewritten and repurposed for the chosen data set and use case.
'''

import xml.etree.cElementTree as ET
import sys


def audit_street_name(unknown_street_names, street_name):
    '''
    Function used check if the provided street_names is conforming to the
    in the expected street name format. If not add the street_name to the
    provided unknown_street_names set.
    '''
    street_preffixes = [u'Norra', u'Södra', u'Västra', u'Östra', u'Stora',
                        u'Lilla', u'Nya', u'Gamla']
    street_types = [u'Gata', u'Väg', u'Allé', u'Gården', u'Gård', u'Torget',
                    u'Skola', u'Industriområde', u'Bro', u'Berget']
    street_endings = [u'gatan', u'vägen', u'väg', u'allén', u'gården', u'gård',
                      u'platsen', u'plan', u'torg', u'kullen', u'leden',
                      u'torp', u'backen', u'åsen']

    components = street_name.split(' ')

    if len(components) <= 3:
        if components[0] not in street_preffixes and \
           components[-1] not in street_types:
            if not components[-1].endswith(tuple(street_endings)):
                unknown_street_names.add(street_name)
                return
    if len(components) == 2:
        if components[0] not in street_preffixes and \
           components[1] not in street_types:
            if not components[1].endswith(tuple(street_endings)):
                unknown_street_names.add(street_name)
                return
    if len(components) == 1:
        if not components[0].endswith(tuple(street_endings)):
            unknown_street_names.add(street_name)
            return


def update_street_name(street_name):
    communities = [u'Hol', u'Horla', u'Asklanda', u'Rommefall', u'Tämta']
    street_name = street_name.replace(',', '')
    street_name = street_name.title()

    # Check if community name is set last and then push it in from of the
    # street address.
    components = street_name.split(' ')
    if components[-1] in communities:
        street_name = components[-1] + ' ' + ' '.join(components[:-1])

    return street_name


def is_street_name(elem):
    '''
    Function checking if the provided osm element (elem) is a street or not.
    '''
    return (elem.attrib['k'] == "addr:street")


def clean(osmfile):
    '''
    Function that checks the osm data we give as an argument to our script and
    writes out all the different street types not present in the expected
    street name array.
    '''
    osm_file = open(osmfile, "r")
    unknown_streets = set()

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    street_name = update_street_name(tag.attrib['v'])
                    audit_street_name(unknown_streets, street_name)

    osm_file.close()

    return unknown_streets


def main(argv):
    unknown_streets = clean(argv)

    print 'Street names not conforming to expected (Swedish) naming standards:'

    for street in unknown_streets:
        print street


if __name__ == "__main__":
    main(sys.argv[1])
