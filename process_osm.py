# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import sys
import json

import audit_city_names
import audit_post_codes
import audit_street_names

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of
dictionaries that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function
with the element as an argument. You should return a dictionary, containing the
shaped data for that element.  We have also provided a way to save the data in
a file, so that you could use mongoimport later on to import the shaped data
into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your
final project, you are strongly encouraged to use the code from previous
exercise to update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value
pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array
      are floats and not strings.
- if the second level tag "k" value contains problematic characters, it should
be ignored
- if the second level tag "k" value starts with "addr:", it should be added to
a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains
":", you can process it in a way that you feel is best. For example, you might
split it into a two-level dictionary like with "addr:", or otherwise convert
the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}

    if element.tag == "way":
        node['node_refs'] = []

    if element.tag == "node" or element.tag == "way":
        node['type'] = element.tag
        attrs = element.attrib
        node['created'] = {}

        for attr in attrs:
            if attr == "lat" or attr == "lon":
                if "pos" not in node:
                    node['pos'] = []
                if attr == "lat":
                    node['pos'].insert(0, float(element.attrib[attr]))
                elif attr == "lon":
                    node['pos'].insert(0, float(element.attrib[attr]))
            elif attr in CREATED:
                node['created'][attr] = element.attrib[attr]
            else:
                node[attr] = element.attrib[attr]

        for subtag in element.iter('tag'):
            key, value = subtag.attrib['k'], subtag.attrib['v']
            if problemchars.match(key):
                continue
            elif lower_colon.match(key):
                subtag_keys = key.split(":")
                if subtag_keys[0] == "addr":
                    if "address" not in node:
                        node['address'] = {}
                    if subtag_keys[1] == "street":
                        node['address'][subtag_keys[1]] = \
                            audit_street_names.update_street_name(value)
                    elif subtag_keys[1] == "postcode":
                        node['address'][subtag_keys[1]] = \
                            audit_post_codes.update_post_code(value)
                    elif subtag_keys[1] == "city":
                        node['address'][subtag_keys[1]] = \
                            audit_city_names.update_city_name(value)
                    else:
                        node['address'][subtag_keys[1]] = value
                else:
                    node[subtag_keys[1]] = value
            else:
                if ":" not in key:
                    node[key] = value
            if element.tag == "way":
                for subtag in element.iter('nd'):
                    node['node_refs'].append(subtag.attrib['ref'])

        return node

    else:
        return None


def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def main(argv):
    process_map(argv)


if __name__ == "__main__":
    main(sys.argv[1])
