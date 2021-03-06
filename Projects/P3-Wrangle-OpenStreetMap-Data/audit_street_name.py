#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All the imports done here
import xml.etree.cElementTree as Et
from collections import defaultdict
import re


# precompiled regular expressions
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# for auditing street names
# list of expected street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Ct", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Park", "Broadway", "Circle", "Highway", "Trail",
            "Way", "West", "North", "Terrace", "Plaza", "Market"]

# mapping the incorrect street names to the correct ones
STREET_MAPPING = {"Ave"    : "Avenue",
                  "Ave."   : "Avenue",
                  "Blvd."  : "Boulevard",
                  "Blvd"   : "Boulevard",
                  "Cir"    : "Circle",
                  "Dr"     : "Drive",
                  "Ln"     : "Lane",
                  "N."     : "North",
                  "Pkwy"   : "Parkway",
                  "Rd"     : "Road",
                  "Rd."    : "Road",
                  "St"     : "Street",
                  "St."    : "Street",
                  "Trl"    : "Trail"
                  }


def audit_street_type(street_types, street_name):
    """
    helper function used in audit(osm_file), updates the dictionary mapping the street names

    :param street_types: default dictionary set
    :param street_name: street name
    :return: update steet_types mapping wrong street name keyword to street name
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """
    helper function used in audit(osm_file), to check the attribute contains street name

    :param elem: element from node or way tag
    :return: bool
    """
    return elem.attrib['k'] == "addr:street"


def audit_street_name(osm_file):
    """
    this function takes the osm_file as parameter and returns a default dictionary set...
    ...mapping the wrong or abbreviated street names if not present in the expected list

    :usage: pass the osm_file to collect the street types dictionary
    ex output:
    {'Ave': set(['N. Lincoln Ave', 'North Lincoln Ave']),
     'Rd.': set(['Baldwin Rd.']),
     'St.': set(['West Lexington St.'])}

    :param osm_file: osm_file with the map data
    :return: dictionary mapping wrong street key word to the unique incorrect street names
    """
    osm_file = open(osm_file, "r")
    street_types = defaultdict(set)
    for event, elem in Et.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # calling helper function is_street_name(elem)
                if is_street_name(tag):
                    # print(tag.attrib)     # uncomment to see the street names
                    # calling helper function audit_street_type
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_street_name(name, mapping=STREET_MAPPING):
    """
    Update the street names by checking the last word in the street name...
    ...if the word is abbreviated change the street name as given in the mapping dict

    :param name: street name
    :param mapping: dictionary mapping the incorrect to correct street names
    :return: correct street names
    """
    name_list = []
    for i in name.split(" "):
        name_list.append(i)

    if name_list[-1] in mapping:
        name_list[-1] = mapping[name_list[-1]]

    name = " ".join(name_list)
    return name


# uncomment to run test
# OSM_FILE = "osm-files/sample.osm"
#
#
# def test():
#     st_types = audit_street_name(OSM_FILE)
#
#     import pprint
#     pprint.pprint(dict(st_types))
#     print("\n\n")
#
#     for st_type, ways in st_types.items():
#         for name in ways:
#             better_name = update_street_name(name, mapping=STREET_MAPPING)
#             print(name, "=>", better_name)
#
#
# if __name__ == '__main__':
#     test()
