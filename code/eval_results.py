import sys
import timeit

sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx

def main(args):
    # data import
    G = nx.read_graphml('../output/graphml_pubs_till_1975_no_count')
    param1 = open('../output/output_till_1975_pubs_param1').read()
    param2 = open('../output/output_till_1975_pubs_param2').read()
    param3 = open('../output/output_till_1975_pubs_param3').read()
    crank = open('../output/output_crank_till_1975_no_title').read()
    
    p1 = eval(param1)
    print('Parametrization 1 read')
    p2 = eval(param2)
    print('Parametrization 2 read')
    p3 = eval(param3)
    print('Parametrization 3 read')
    cr = eval(crank)
    print('Crank read')


    # data structure initialization
    msc_classes = dict()
        #For all MSC Klasses, find out which publication is in class
    for msc, nbrsdict in G.adjacency_iter():
        if G.node[msc]['Class']=='MSC_Class':
            for pub, eattr in nbrsdict.items():
                if eattr.items()[0][1]['Relation']=='hasClassificationCode':
                    try:
                        class_exists = msc_classes[msc]
                        msc_classes[msc].append(pub)
                    except:
                        msc_classes[msc] = [pub]

    print ('msc_classes initialized')

if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
