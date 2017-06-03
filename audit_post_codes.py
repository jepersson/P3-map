# -*- coding: utf-8 -*-

'''
This script is based on lesson material from Udacity's MongoDB course but
rewritten and repurposed for the chosen data set and use case.
'''

import xml.etree.cElementTree as ET
import re
import sys

POST_CODE_REGEX = re.compile(r'^\d{3} \d{2}$')


def audit_post_code(unknown_codes, post_code):
    '''
    Function used check if the provided post_code is conforming to the
    in the expected name format. If not add the post_code to the
    provided unknown_codes set.
    '''
    if not POST_CODE_REGEX.match(post_code):
        unknown_codes.add(post_code)

    if post_code[:2] >= 42 and post_code[:2] <= 54:
        unknown_codes.add(post_code)

    return


def is_post_code(elem):
    '''
    Function checking if the provided osm element (elem) is a post code or not.
    '''
    return (elem.attrib['k'] == "addr:postcode")


def update_post_code(post_code):
    if post_code[3] != ' ':
        post_code = post_code[:3] + ' ' + post_code[3:]

    return post_code


def clean_post_code(osmfile):
    '''
    Function that checks the osm data we give as an argument to our script and
    writes out all the post codes not present in the expected code array.
    '''
    osm_file = open(osmfile, "r")
    unknown_codes = set()

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_post_code(tag):
                    post_code = update_post_code(tag.attrib['v'])
                    audit_post_code(unknown_codes, post_code)

    osm_file.close()

    return unknown_codes


def main(argv):
    unknown_codes = clean_post_code(argv)

    print 'Post codes not conforming to expected (Swedish) standards:'

    for code in unknown_codes:
        print code


if __name__ == "__main__":
    main(sys.argv[1])
