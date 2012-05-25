# -*- coding: utf-8 -*-

import sys
import os
import timeit
import re
from lxml import etree
from sys import argv
import fileinput

script, input_file = argv

def year_to_owl(year):
    result = []

    pattern = '([0-9]{4})\n'

    years_stripped = re.findall(pattern, year)
    #print("Debugging.............lan_stripped is...........", lan_stripped)
    for y in years_stripped:
        dec = etree.Element("Declaration")
        namedInd = etree.Element("NamedIndividual", IRI="#%s" % y)
        dec.append(namedInd)
        result.append(dec)

        classAsser = etree.Element("ClassAssertion")
        classTag = etree.Element("Class", IRI="#PublicationYear")
        namedInd2 = etree.Element("NamedIndividual", IRI="#%s" % y)
        classAsser.append(classTag)
        classAsser.append(namedInd2)
        result.append(classAsser)

    return result


root = etree.Element("Ontology")
for line in fileinput.input(input_file):
    #print("Debugging...........%s" % line)
    #declare language individual
    #assign it to class language
    for elem in year_to_owl(line):
        root.append(elem)

print(etree.tostring(root, pretty_print=True))

