import sys
import timeit

#sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx

def main(args):
    # data import
    G = nx.read_graphml('output/pubs_till_1975_no_count')
    #param1 = open('../output/output_till_1975_pubs_param1').read()
    #param2 = open('../output/output_till_1975_pubs_param2').read()
    #param3 = open('../output/output_till_1975_pubs_param3').read()
    crank = open('benchmarks/output_crank_till_1975_no_title').read()
    
    #p1 = eval(param1)
    #print('Parametrization 1 read')
    #p2 = eval(param2)
    #print('Parametrization 2 read')
    #p3 = eval(param3)
    #print('Parametrization 3 read')
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

    # Select 3 Publications of the class 54D35
    pub1 = msc_classes['54D35'][0]
    print('pub1 is', pub1)
    pub2 = msc_classes['54D35'][2]
    print('pub2 is', pub2)
    pub3 = msc_classes['54D35'][15]
    print('pub3 is', pub3)

    # compute average scores
    # for pub1
    p1_sum_papes_in_a = 0 #todo: devide by number papes in a
    p1_sum_papes_not_in_a = 0

    for v in cr[pub1]:
        if v != pub1:
            if v in msc_classes['54D35']:
                p1_sum_papes_in_a = p1_sum_papes_in_a + cr[pub1][v]
            else:
                p1_sum_papes_not_in_a = p1_sum_papes_not_in_a + cr[pub1][v]

    for v in cr[pub2]:

    for v in cr[pub3]:

    for key in cr:
        if key == pub1:
            # to add only to pub2 and pub3
        elif key == pub2:
            # to add only to pub1 und pub3
        elif key == pub3:
            # to add only to pub1 und pub2

        else: # to add to all
            for v in cr[key]:
                if v==pub1:
                    if v in msc_classes['54D35']:
                        p1_sum_papes_in_a = p1_sum_papes_in_a + cr[key][v]
                    else:
                        p1_sum_papes_not_in_a = p1_sum_papes_not_in_a + cr[key][v]
                elif v == pub2:
                    #analogous
                elif v == pub3:
                    #..



if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
