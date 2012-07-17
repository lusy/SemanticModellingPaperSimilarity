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

    total_pubs = 3095
    
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
    pub2 = msc_classes['54D35'][1]
    print('pub2 is', pub2)
    pub3 = msc_classes['54D35'][15]
    print('pub3 is', pub3)

    # compute average scores
    # for pub1
    pubs_in_a = len(msc_classes['54D35'])
    pubs_not_in_a = total_pubs - pubs_in_a

    p1_sum_papes_in_a = 0 #todo: devide by number papes in a
    p1_sum_papes_not_in_a = 0

    p2_sum_papes_in_a = 0
    p2_sum_papes_not_in_a = 0

    p3_sum_papes_in_a = 0
    p3_sum_papes_not_in_a = 0

    for v in cr[pub1]:
        if v != pub1:
            if v in msc_classes['54D35']:
                p1_sum_papes_in_a = p1_sum_papes_in_a + cr[pub1][v]
            else:
                p1_sum_papes_not_in_a = p1_sum_papes_not_in_a + cr[pub1][v]

    for v in cr[pub2]:
        if v != pub2:
            if v in msc_classes['54D35']:
                p2_sum_papes_in_a = p2_sum_papes_in_a + cr[pub2][v]
            else:
                p2_sum_papes_not_in_a = p2_sum_papes_not_in_a + cr[pub2][v]

    for v in cr[pub3]:
        if v != pub3:
            if v in msc_classes['54D35']:
                p3_sum_papes_in_a = p3_sum_papes_in_a + cr[pub3][v]
            else:
                p3_sum_papes_not_in_a = p3_sum_papes_not_in_a + cr[pub3][v]

    for key in cr:
        if key == pub1:
            for v in cr[key]:
                if v == pub2:
                    print('pub2! 1mal')
                    p2_sum_papes_in_a = p2_sum_papes_in_a + cr[key][v]
                elif v == pub3:
                    print('pub3! 1mal')
                    p3_sum_papes_in_a = p3_sum_papes_in_a + cr[key][v]

        elif key == pub2:
            for v in cr[key]:
                if v == pub1:
                    print('pub1! 1mal')
                    p1_sum_papes_in_a = p1_sum_papes_in_a + cr[key][v]
                elif v == pub3:
                    print('pub3! 2mal')
                    p3_sum_papes_in_a = p3_sum_papes_in_a + cr[key][v]

        elif key == pub3:
            for v in cr[key]:
                if v == pub2:
                    print('pub2! 2mal')
                    p2_sum_papes_in_a = p2_sum_papes_in_a + cr[key][v]
                elif v == pub1:
                    print('pub1! 2mal')
                    p1_sum_papes_in_a = p1_sum_papes_in_a + cr[key][v]


        else: # to add to all
            for v in cr[key]:
                if v==pub1:
                    print('pub1! 1mal!')
                    if key in msc_classes['54D35']:
                        p1_sum_papes_in_a = p1_sum_papes_in_a + cr[key][v]
                    else:
                        p1_sum_papes_not_in_a = p1_sum_papes_not_in_a + cr[key][v]
                elif v == pub2:
                    print('pub2! 3mal!')
                    if key in msc_classes['54D35']:
                        p2_sum_papes_in_a = p2_sum_papes_in_a + cr[key][v]
                    else:
                        p2_sum_papes_not_in_a = p2_sum_papes_not_in_a + cr[key][v]
                elif v == pub3:
                    print('pub3! 3mal!')
                    if key in msc_classes['54D35']:
                        p3_sum_papes_in_a = p3_sum_papes_in_a + cr[key][v]
                    else:
                        p3_sum_papes_not_in_a = p3_sum_papes_not_in_a + cr[key][v]


    aver_p1_papes_in_a = p1_sum_papes_in_a/pubs_in_a
    aver_p1_papes_not_in_a = p1_sum_papes_not_in_a / pubs_not_in_a
    aver_p1_all_pubs = (p1_sum_papes_in_a + p1_sum_papes_not_in_a)/total_pubs

    aver_p2_papes_in_a = p2_sum_papes_in_a/pubs_in_a
    aver_p2_papes_not_in_a = p2_sum_papes_not_in_a / pubs_not_in_a
    aver_p2_all_pubs = (p2_sum_papes_in_a + p2_sum_papes_not_in_a)/total_pubs

    aver_p3_papes_in_a = p3_sum_papes_in_a/pubs_in_a
    aver_p3_papes_not_in_a = p3_sum_papes_not_in_a / pubs_not_in_a
    aver_p3_all_pubs = (p3_sum_papes_in_a + p3_sum_papes_not_in_a)/total_pubs

    #pubs_in_a = len(msc_classes['54D35'])
    #pubs_not_in_a = total_pubs - pubs_in_a

    p1_in_a_to_p1_not_in_a = aver_p1_papes_in_a / aver_p1_papes_not_in_a
    p1_in_a_to_all = aver_p1_papes_in_a / aver_p1_all_pubs

    p2_in_a_to_p2_not_in_a = aver_p2_papes_in_a / aver_p2_papes_not_in_a
    p2_in_a_to_all = aver_p2_papes_in_a / aver_p2_all_pubs

    p3_in_a_to_p3_not_in_a = aver_p3_papes_in_a / aver_p3_papes_not_in_a
    p3_in_a_to_all = aver_p3_papes_in_a / aver_p3_all_pubs

    print('p1_sum_papes_in_a is', p1_sum_papes_in_a)
    print('p1_sum_papes_not_in_a', p1_sum_papes_not_in_a)

    print('p2_sum_papes_in_a', p2_sum_papes_in_a)
    print('p2_sum_papes_not_in_a', p2_sum_papes_not_in_a)

    print('p3_sum_papes_in_a', p3_sum_papes_in_a)
    print('p3_sum_papes_not_in_a', p3_sum_papes_not_in_a)

    print('pub2s dic', cr[pub2])

    print('aver_p1_papes_in_a', aver_p1_papes_in_a)
    print('aver_p1_papes_not_in_a', aver_p1_papes_not_in_a)
    print('aver_p1_all_pubs', aver_p1_all_pubs)

    print('aver_p2_papes_in_a', aver_p2_papes_in_a)
    print('aver_p2_papes_not_in_a', aver_p2_papes_not_in_a)
    print('aver_p2_all_pubs', aver_p2_all_pubs)

    print('aver_p3_papes_in_a', aver_p3_papes_in_a)
    print('aver_p3_papes_not_in_a', aver_p3_papes_not_in_a)
    print('aver_p3_all_pubs', aver_p3_all_pubs)

    print('p1_in_a_to_p1_not_in_a', p1_in_a_to_p1_not_in_a)
    print('p1_in_a_to_all', p1_in_a_to_all)

    print('p2_in_a_to_p1_not_in_a', p2_in_a_to_p2_not_in_a)
    print('p2_in_a_to_all', p2_in_a_to_all)

    print('p3_in_a_to_p1_not_in_a', p3_in_a_to_p3_not_in_a)
    print('p3_in_a_to_all', p3_in_a_to_all)


if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
