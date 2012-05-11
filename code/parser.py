# -*- coding: utf-8 -*-

import sys
import os
import timeit
import re
import fileinput
from lxml import etree

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
    citations = []

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

    def get_citations(self):
        '''Returns all the papers which the current publication cites'''
        return self.citations

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
        print 'citations: ', self.get_citations()


class Parser(object):
    '''Class parses line by line an input file and creates publication objects out of it'''
    # TODO: decide class or function?
    # if class : init(inputFile)
    # if function (inputFile, handleMethod)


    # global variables to be kept track of:
    languages = []
    # years = []
    # authors = []
    # mscClasses = []
    # keyWords = []

    def __init__(self, inputFile):
        self.inputFile = inputFile

    def iterate_publications(self, handleMethod):
        result = list()
        #used for capturing tuple tag-content, content can be empty
        pattern = ':([a-z/:]{2,5}):\t?(.*)'

        for line in fileinput.input(self.inputFile):
            pline = re.findall(pattern, line)
            # If tag has no content (end of record), than a single value is written to list, not a tuple
            if type(pline[0]) == tuple:
                tag = pline[0][0]
                content = pline[0][1]
            else:
                tag = pline[0]
                content = ''

            #Debug
            #print ("This is the regex i parsed: %s, %s" % (tag, content))
            #print("Debugging", tag)

            if tag == 'id':
                #objekt erzeugen, parsen anfangen
                currentPub = Publication()
                currentPub.id = int(content)
                #print ("id: ", currentPub.id)

            elif tag == 'an' and content != '':
                currentPub.an = content
                #print ("an: ", currentPub.an)

            elif tag == 'py' and content != '':
                currentPub.publicationYear = content
                #print ("py: ", currentPub.publicationYear)

            elif tag == 'au':
                # save authors temporarily and simulate ai out of it if ai field empty
                tempAuthor =  content.split("; ")

            elif tag == 'ai' and content != '':
                currentPub.authors = content.split("; ")
                #print ("authors: ", currentPub.authors)

            # Simulate :ai: out of :au: if :ai: empty or containing just ";"s
            elif tag =='ai' and (content == '' or content == "; " or ("; ;") in content):
                # Check if one author or list of authors
                if type(tempAuthor) == str:
                    (lastName, firstName) = tempAuthor.lower().split(", ")
                    firstName = firstName.replace(".","-").replace(" ","-").rstrip("-")
                    currentPub.authors.append("%s.%s" % (lastName, firstName))

                else:
                    for auth in tempAuthor:
                        (lastName, firstName) = auth.lower().split(", ")
                        firstName = firstName.replace(".","-").replace(" ","-").rstrip("-")
                        currentPub.authors.append("%s.%s" % (lastName, firstName))


            elif tag == 'ti' and content != '':
                currentPub.titleString = content
                #TODO extract title somehow
                #print ("title: ", currentPub.titleString)

            elif tag == 'so' and content != '':
                currentPub.source = content
                #TODO: parse source so that it makes sense
                #print ("source: ", currentPub.source)

            elif tag == 'cc' and content != '':
                currentPub.mscClasses = content.split()
                #print ("classes: ", currentPub.mscClasses)

            elif tag == 'ut' and content != '':
                currentPub.englishKeywords = content.split("; ")
                #print ("keywords: ", currentPub.englishKeywords)

            elif tag == 'la' and content != '':
                # look up if it's already in languages, if not, add it
                currentPub.language = content.split(' ')
                #handles cases of one/more languages
                if ' ' in content:
                    for l in currentPub.language:
                        if l not in self.languages:
                            self.languages.append(l)
                else:
                    if content not in self.languages:
                        self.languages.append(content)


            elif tag == 'ci' and content != '':
                currentPub.citations = content.split("; ")
                #print ("citations: ", currentPub.citations)

            elif tag == 'li':
                pass

            elif tag == 'ab/en' and content != '':
                currentPub.abstract = content
                #print ("abstract: ", currentPub.abstract)

            elif tag == 'rv/en':
                pass

            elif tag == '::':
                result.append(handleMethod(currentPub))
                #print "Debug output: is currentPub created successfully"
                #currentPub.info()
                del currentPub
                #mach was mit dem erzeugten objekt
                #zerstoere das objekt am ende

            else:
                #print "An unexpected line occured in the input file or content of tag was empty."
                pass

        #print result
        print ("self.languages contains", self.languages)
        return result



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
    # Achtung! In Feldern, die Listen enthalten, koenen auch leere Elemente drin sein (autoren, etc), check before apending
    dec1 = etree.Element("Declaration")
    pub = "#Publication_%d" % publication.id
    namedInd1 = etree.Element("NamedIndividual", IRI="%s" % pub)
    dec1.append(namedInd1)
    return dec1

def testing_handler_method(publication):
    return publication.info()

##########################################################################################

def main(args):
    if len(args) != 1:
        print 'Usage: python parser.py <datasetfile>'
        exit()

    # lala parser starten halt
    p = Parser(args[0])
    #p.iterate_publications(testing_handler_method)

    root = etree.Element("Ontology")
    for i in p.iterate_publications(publications_to_owl):
        print("Debugging...... i is", i)
        root.append(i)
    #TODO append children to root

    print(etree.tostring(root, pretty_print=True))

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
