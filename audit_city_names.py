# -*- coding: utf-8 -*-

'''
This script is based on lesson material from Udacity's MongoDB course but
rewritten and repurposed for the chosen data set and use case.
'''

import xml.etree.cElementTree as ET
import sys


def audit_city_name(unknown_names, city_name):
    '''
    Function used check if the provided post_code is conforming to the
    in the expected name format. If not add the post_code to the
    provided unknown_codes set.
    '''
    expected_names = [u'Alingsås', u'Herrljunga', u'Vårgårda']

    print city_name
    if city_name not in expected_names:
        unknown_names.add(city_name)

    return


def is_city_name(elem):
    '''
    Function checking if the provided osm element (elem) is a post code or not.
    '''
    return (elem.attrib['k'] == "addr:city")


def update_city_name(city_name):
    return city_name


def clean_city_names(osmfile):
    '''
    Function that checks the osm data we give as an argument to our script and
    writes out all the post codes not present in the expected code array.
    '''
    osm_file = open(osmfile, "r")
    unknown_names = set()

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    city_name = tag.attrib['v']
                    audit_city_name(unknown_names, city_name)

    osm_file.close()

    return unknown_names


def main(argv):
    unknown_names = clean_city_names(argv)

    print 'City names not conforming to expected names:'

    for name in unknown_names:
        print name


if __name__ == "__main__":
    main(sys.argv[1])
