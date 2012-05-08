# -*- coding: utf-8 -*-

import sys
import os
import timeit
import re

# class publication
# (class parser)
# function to_owl
# function main -> which analyses do we do
# evtl. andere functionen um sich nur autoren/... anzuzeigen -> statistical analyses

class Publication(object):
    '''Class represents a single publication from the zmath dataset'''

    id = 0
    an = ""
    abstract = ""
    titleString = ""
    title = "" #TODO how to extract it
    publicationYear = 0
    authors = []
    mscClasses = []
    source = "" #TODO how to represent it; parse book/journal/conference
    language = []
    englishKeywords = []

    def get_id(self):
        '''Returns the id of a publication'''
        return self.id

    def get_an(self):
        '''Returns the :an: (accession number) of a publication'''
        return self.an

    def get_abstract(self):
        '''Returns the abstract of a publication'''
        return self.abstract

    def get_titleString(self):
        '''Returns the titleString of a publication'''
        return self.titleString

    def get_title(self):
        '''Returns the title of a publication'''
        return self.title

    def get_publicationYear(self):
        '''Returns the publication year of a publication'''
        return self.publicationYear

    def get_authors(self):
        '''Returns all the authors appearing in the :ai: field of a publication'''
        return self.authors

    def get_mscClasses(self):
        return self.mscClasses

    def get_source(self):
        return self.source

    def get_language(self):
        '''Returns all the languages appearing in the :la: fieald of a publication'''
        return self.language

    def get_keywords(self):
        '''Returns all the english keywords of a publication'''
        return self.englishKeywords

    def info(self):
        '''Display all metadata of a publication'''
        print 'id: ', self.get_id()
        print 'an: ', self.get_an()
        print 'title: ', self.get_title()
        print 'titleString: ', self.get_titleString()
        print 'authors: ', self.get_authors()
        print 'abstract: ', self.get_abstract()
        print 'publication year: ', self.get_publicationYear()
        print 'msc classes: ', self.get_mscClasses()
        print 'source: ', self.get_source()
        print 'language: ', self.get_language()
        print 'english key words: ', self.get_keywords()



class Parser(object):
    '''Class parses line by line an input file and creates publication objects out of it'''
    # TODO: decide class or function?

    # global variables to be kept track of:
    languages = []
    # years = []
    # authors = []
    # mscClasses = []
    # keyWords = []

    def __init__(self, inputFile):
        #lalala
        pass

    def iterate_publications(self, handleMethod):
        #lala
        pass



    # if class : init(inputFile)
    # if function (inputFile, handleMethod)

    # gets input file
    # while !eof
    # read line
    # if not end of publication:
        # create publication, fill in the fields
    # if end of publication: process the publication -> handleMethod
    # overwrite object


########## HandleMethods #################################################################

def publications_to_owl(publication):
    '''Takes a publication object and converts it to its representation in xml/owl syntax'''
    # TODO modify method so that it can appends publications to existing owl file
    pass

##########################################################################################

def main(args):
    if len(args) != 1:
        print 'Usage: python parser.py <datasetfile>'
        exit()

    # lala parser starten halt

if __name__ == "__main__":
    #main(sys.argv[1:])
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)

# main
# datei als parameter uebergeben
# zeile fuer zeile einlesen
# variablen definieren
# sich ein objekt fuer die aktuelle publikation basteln
# ...
#
# globale variablen
# language_list
# wenn zeile="::::" -> zuruecksetzen
