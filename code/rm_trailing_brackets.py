# -*- coding: utf-8 -*-

from sys import argv
import os
import fileinput

script, from_file = argv

for line in fileinput.input(from_file):
    #print ("before: ", line)
    line=line.rstrip(']\n')
    line=line.lstrip('[')
    print (line)
