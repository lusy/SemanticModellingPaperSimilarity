import sys
import timeit
import re

#sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx

def main(args):
    # data import
    G = nx.read_graphml('../data/pubs_till_1975_no_count')

    #For all MSC Klasses, find out which publication is in class
    msc_classes = dict()
    msc_classes_aggregated = dict()

    '''
    for msc, nbrsdict in G.adjacency_iter():
        if G.node[msc]['Class']=='MSC_Class':
            for pub, eattr in nbrsdict.items():
                if eattr.items()[0][1]['Relation']=='hasClassificationCode':
                    try:
                        class_exists = msc_classes[msc]
                        msc_classes[msc].append(pub)
                    except:
                        msc_classes[msc] = [pub]

    #for cl in msc_classes:
        #print("In class %s, there are pubs:" % cl, msc_classes[cl])

    '''
    #pattern = '([0-9]{2}[A-Z\-])[0-9xX]{2}'
    pattern = '([0-9]{2})[A-Z\-][0-9xX]{2}'

    for msc, nbrsdict in G.adjacency_iter():
        if G.node[msc]['Class']=='MSC_Class':
            for pub, eattr in nbrsdict.items():
                if eattr.items()[0][1]['Relation']=='hasClassificationCode':
                    first3digits = re.findall(pattern, msc)
                    if first3digits != []:
                        try:
                            class_exists = msc_classes_aggregated[first3digits[0]]
                            msc_classes_aggregated[first3digits[0]].append(pub)
                        except:
                            msc_classes_aggregated[first3digits[0]] = [pub]
                    else:
                        print('first3digits empty, msc is: ', msc)

    for cl in msc_classes_aggregated:
        print("In class %s, there are pubs:" % cl, msc_classes_aggregated[cl])



if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)


