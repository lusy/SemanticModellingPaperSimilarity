# -*- coding: utf-8 -*-

import sys
import os
import timeit
import logging
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

    logger = logging.getLogger("parse")
    # overwrite log file everytime we parse
    hdlr = logging.FileHandler('parse.log', mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    def __init__(self, inputFile):
        self.inputFile = inputFile

    def iterate_publications(self, handleMethod):
        result = list()
        #used for capturing tuple tag-content, content can be empty
        pattern = ':([a-z/:]{2,5}):\t?(.*)'

        # we define these here, so that we can look up what the last
        # valid tag was in case new line has no tag
        tag = ''
        content = ''
        lasttag = ''

        for line in fileinput.input(self.inputFile):
            pline = re.findall(pattern, line)
            # If tag has no content (end of record), than a single value is written to list, not a tuple
            try:
                if type(pline[0]) == tuple:
                    tag = pline[0][0]
                    content = pline[0][1]
                else:
                    tag = pline[0]
                    content = ''
            # exceptions due to nothing matches the regex pattern, no valid tag is there
            except:
                # for now only handle case, new line is part of an abstract
                # if last tag was abstract
                if tag == 'ab/en' or lasttag == 'ab/en':
                    currentPub.abstract = currentPub.abstract + "\n" + line.rstrip("\n")
                    tag = ''
                    lasttag = 'ab/en'

                else:
                    self.logger.warning("Omitting a line, it doesn't match the regex pattern. Last tag is %s" % tag)
                    #print("The line is", line)

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

            elif tag == 'py':
                # publication year is never empty
                currentPub.publicationYear = content
                #print ("py: ", currentPub.publicationYear)

            elif tag == 'au':
                # save authors temporarily and simulate ai out of it if :ai: field empty
                # case of :au: empty is handled below
                tempAuthor =  content.split("; ")
                #print("Debuggging....... tempAuthor is", tempAuthor)

            elif tag == 'ai' and content != '' and content != "; " and not(("; ;") in content):
                currentPub.authors = content.split("; ")
                #print ("authors: ", currentPub.authors)

            # Simulate :ai: out of :au: if :ai: empty or containing just ";"s (only if :au: was not empty)
            elif tag =='ai' and (content == '' or content == "; " or ("; ;") in content) and tempAuthor != ['']:
                self.logger.info("For publication %d we generate :ai: out of :au:" % currentPub.id)
                # Check if one author or list of authors
                if type(tempAuthor) == str :
                    try:
                        (lastName, firstName) = tempAuthor.lower().split(", ")
                        lastName = lastName.replace(" ", "-")
                        firstName = firstName.rstrip(" (ed.)").replace(".","-").replace(" ","-").rstrip("-")
                        currentPub.authors.append("%s.%s" % (lastName, firstName))
                    except:
                       self.logger.warning("For publication %d authors have funny format, no :ai: generated" % currentPub.id)
                       self.logger.warning("For publication %d we've got %s in tempAuthor" % (currentPub.id, tempAuthor))

                else:
                    for auth in tempAuthor:
                        try:
                            (lastName, firstName) = auth.lower().split(", ")
                            lastName = lastName.replace(" ", "-")
                            firstName = firstName.rstrip(" (ed.)").replace(".","-").replace(" ","-").rstrip("-")
                            currentPub.authors.append("%s.%s" % (lastName, firstName))
                        except:
                            self.logger.warning("For publication %d authors have funny format, no :ai: generated" % currentPub.id)

            elif tag == 'ti' and content != '':
                currentPub.titleString = content
                #TODO extract title somehow
                #print ("title: ", currentPub.titleString)

            elif tag == 'so':
                # source is never empty
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
                currentPub.language = content.split(' ')

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
                del currentPub
                #mach was mit dem erzeugten objekt
                #zerstoere das objekt am ende

            else:
                # question: when do we actually come to this case?
                #self.logger.info("No of the expected tags seen at the beginning")
                #print "An unexpected line occured in the input file or content of tag was empty."
                pass

        #print result
        #print ("self.languages contains", self.languages)
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
    # TODO modify method so that it can append publications to existing owl file
    # or consider merging the headers to this one

    result = []

    #Publication Individual
    pub = "Publication_%d" % publication.id
    decPub = owl_declaration(pub)
    classAsserPub = owl_class_assertion(pub, "Publication")
    result.append(decPub)
    result.append(classAsserPub)

    #ID
    dataPropAsserId = owl_data_property_assertion(pub, "hasId", "&xsd;positiveInteger", publication.id)
    result.append(dataPropAsserId)

    #an
    if publication.an != '':
        dataPropAsserAn = owl_data_property_assertion(pub, "hasAccessionNumber", "&rdf;PlainLiteral", publication.an)
        result.append(dataPropAsserAn)

    #abstract
    if publication.abstract != '':
        dataPropAsserAb = owl_data_property_assertion(pub, "hasAbstract", "&rdf;PlainLiteral", publication.abstract)
        result.append(dataPropAsserAb)

    #titleString
    if publication.titleString !='':
        dataPropAsserTi = owl_data_property_assertion(pub, "hasTitleString", "&rdf;PlainLiteral", publication.titleString)
        result.append(dataPropAsserTi)

    #title
    #TODO extracting title from title string

    #source
    #TODO extracting source

    #publication year
    decPy = owl_declaration(str(publication.publicationYear))
    classAsserPy = owl_class_assertion(str(publication.publicationYear), "PublicationYear")
    objPropAsserPy = owl_object_property_assertion("wasPublishedInYear", pub, str(publication.publicationYear))
    result.append(decPy)
    result.append(classAsserPy)
    result.append(objPropAsserPy)

    #authors
    #print("Debuggging.....authors are", publication.authors)
    for auth in publication.authors:
        if auth !='':
            decAuth = owl_declaration(auth)
            classAsserAuth = owl_class_assertion(auth, "Author")
            objPropAsserAuth = owl_object_property_assertion("isAuthorOf", auth, pub)
            result.append(decAuth)
            result.append(classAsserAuth)
            result.append(objPropAsserAuth)

    #msc classes
    for cl in publication.mscClasses:
        decClass = owl_declaration(cl)
        classAsserCl = owl_class_assertion(cl, "MSC_Class")
        objPropAsserCl = owl_object_property_assertion("hasClassificationCode", pub, cl)
        result.append(decClass)
        result.append(classAsserCl)
        result.append(objPropAsserCl)

    #languages

    #TODO consider striking out duplicates (how?)
    #create language variable for the handler method
    #append new languages , return it
    # problem: how do we look up whats already there?
        #look up if it's already in languages, if not, add it
                #handles cases of one/more languages
                #if ' ' in content:
                    #for l in currentPub.language:
                        #if l not in self.languages:
                            #self.languages.append(l)
                #else:
                    #if content not in self.languages:
                        #self.languages.append(content)


    if type(publication.language) == str:
        if publication.language not in Parser.languages:
            Parser.languages.append(publication.language)
            decLan = owl_declaration(publication.language)
            classAsserLan = owl_class_assertion(publication.language, "Language")
            objPropAsserLan = owl_object_property_assertion("hasLanguage", pub, publication.language)
            result.append(decLan)
            result.append(classAsserLan)
            result.append(objPropAsserLan)

    #if more than one languages
    else:
        for lan in publication.language:
            decLan = owl_declaration(lan)
            classAsserLan = owl_class_assertion(lan, "Language")
            objPropAsserLan = owl_object_property_assertion("hasLanguage", pub, lan)
            result.append(decLan)
            result.append(classAsserLan)
            result.append(objPropAsserLan)

    #english keywords
    if publication.englishKeywords != []:
        for k in publication.englishKeywords:
            decKey = owl_declaration(k)
            classAsserKey = owl_class_assertion(k, "EnglishKeywod")
            objPropAsserKey = owl_object_property_assertion("hasKeyword", pub, k)
            result.append(decKey)
            result.append(classAsserKey)
            result.append(objPropAsserKey)

    #citations
    # do we create new publications here for every citation? at first, no
    # for now the citations are put into new class: Reference
    if publication.citations != []:
        for ci in publication.citations:
            decCit = owl_declaration(ci)
            classAsserCit = owl_class_assertion(ci, "Reference")
            objPropAsserCit = owl_object_property_assertion("cites", pub, ci)
            result.append(decCit)
            result.append(classAsserCit)
            result.append(objPropAsserCit)



    return result

def testing_handler_method(publication):
    return publication.info()

def extract_authors(publication):
    print (publication.authors)
    #for auth in publication.authors:
        #if auth !='':
            #print("%s" % auth)

def extract_keywords(publication):
    print (publication.englishKeywords)
    #for k in publication.englishKeywords:
        #print("%s" % k)

def extract_citations(publication):
    print (publication.citations)
    #for ci in publication.citations:
        #print("%s" % ci)

def extract_mscClasses(publication):
    print(publication.mscClasses)
    #for cc in publication.mscClasses:
        #print("%s" % cc)

def extract_languages(publication):
    print(publication.language)
    #for l in publication.language:
        #print("%s" % l)
##########################################################################################

################## OWl Helper Methods ########################################################
def owl_declaration(elem):
    dec = etree.Element("Declaration")
    namedInd = etree.Element("NamedIndividual", IRI="#%s" % elem)
    dec.append(namedInd)
    return dec

def owl_class_assertion(elem, owlClass):
    classAsser = etree.Element("ClassAssertion")
    classTag = etree.Element("Class", IRI="#%s" % owlClass)
    namedInd = etree.Element("NamedIndividual", IRI="#%s" % elem)
    classAsser.append(classTag)
    classAsser.append(namedInd)
    return classAsser

def owl_data_property_assertion(elem, dataProp, dataType, value):
    dataPropAsser = etree.Element("DataPropertyAssertion")
    dataProp1 = etree.Element("DataProperty", IRI="#%s" % dataProp)
    namedInd = etree.Element("NamedIndividual", IRI="#%s" % elem)
    literal = etree.Element("Literal", datatypeIRI="%s" % dataType)
    literal.text = "%s" % str(value)
    dataPropAsser.append(dataProp1)
    dataPropAsser.append(namedInd)
    dataPropAsser.append(literal)
    return dataPropAsser

def owl_object_property_assertion(objProp, elem1, elem2):
    objPropAsser = etree.Element("ObjectPropertyAssertion")
    objProp1 = etree.Element("ObjectProperty", IRI="#%s" % objProp)
    namedInd1 = etree.Element("NamedIndividual", IRI="#%s" % elem1)
    namedInd2 = etree.Element("NamedIndividual", IRI="#%s" % elem2)
    objPropAsser.append(objProp1)
    objPropAsser.append(namedInd1)
    objPropAsser.append(namedInd2)
    return objPropAsser

##########################################################################################

def main(args):
    if len(args) != 1:
        print 'Usage: python parser.py <datasetfile>'
        exit()

    # lala parser starten halt
    p = Parser(args[0])
    #p.iterate_publications(testing_handler_method)

    #p.iterate_publications(extract_authors)
    p.iterate_publications(extract_keywords)
    #p.iterate_publications(extract_citations)
    #p.iterate_publications(extract_mscClasses)
    #p.iterate_publications(extract_languages)

##### parsing to xml/owl##################################
    #root = etree.Element("Ontology")
    ## i contains all the nodes belonging to one publication
    ## j are the individual nodes for one publication
    #for i in p.iterate_publications(publications_to_owl):
        #for j in i:
            #root.append(j)
    #TODO append children to root

    #print(etree.tostring(root, pretty_print=True))

#############################################################

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
