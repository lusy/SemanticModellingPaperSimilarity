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
    print('----------------------------------------------------------------------------')
    print('\n')

    
    # Select 3 Publications of the class 54D35
    pub1 = msc_classes['54D35'][0]
    print('pub1 is', pub1)
    pub2 = msc_classes['54D35'][1]
    print('pub2 is', pub2)
    pub3 = msc_classes['54D35'][15]
    print('pub3 is', pub3)

    print('--------Computing CRank-----------------------------')
    compute_average(pub1, pub2, pub3, '54D35', cr, msc_classes)
    print('----------------------------------------------------')
    print('\n')

    # Select 3 Publications of the class 46-XX
    pub4 = msc_classes['46-XX'][0]
    print('pub4 is', pub4)
    pub5 = msc_classes['46-XX'][13]
    print('pub5 is', pub5)
    pub6 = msc_classes['46-XX'][28]
    print('pub6 is', pub6)

    print('---------Computing CRank-----------------------------')
    compute_average(pub4, pub5, pub6, '46-XX', cr, msc_classes)
    print('-----------------------------------------------------')
    print('\n')

    # Select 3 Publications of the class 11-02
    pub7 = msc_classes['11-02'][2]
    print('pub7 is', pub7)
    pub8 = msc_classes['11-02'][29]
    print('pub8 is', pub8)
    pub9 = msc_classes['11-02'][34]
    print('pub9 is', pub9)
    
    print('---------Computing CRank-----------------------------')
    compute_average(pub7, pub8, pub9, '11-02', cr, msc_classes)


def compute_average(pub1, pub2, pub3, mscClass, used_method, msc_classes):
    #print('Dict of %s is' % pub1, used_method[pub1])
    #print('Dict of %s is' % pub2, used_method[pub2])
    #print('Dict of %s is' % pub3, used_method[pub3])

    total_pubs = 3095
    # compute average scores
    # for pub1
    pubs_in_a = len(msc_classes[mscClass])
    pubs_not_in_a = total_pubs - pubs_in_a

    p1_sum_papes_in_a = 0 #todo: devide by number papes in a
    p1_sum_papes_not_in_a = 0

    p2_sum_papes_in_a = 0
    p2_sum_papes_not_in_a = 0

    p3_sum_papes_in_a = 0
    p3_sum_papes_not_in_a = 0

    for v in used_method[pub1]:
        if v != pub1:
            if v in msc_classes[mscClass]:
                p1_sum_papes_in_a = p1_sum_papes_in_a + used_method[pub1][v]
            else:
                p1_sum_papes_not_in_a = p1_sum_papes_not_in_a + used_method[pub1][v]

    for v in used_method[pub2]:
        if v != pub2:
            if v in msc_classes[mscClass]:
                p2_sum_papes_in_a = p2_sum_papes_in_a + used_method[pub2][v]
            else:
                p2_sum_papes_not_in_a = p2_sum_papes_not_in_a + used_method[pub2][v]

    for v in used_method[pub3]:
        if v != pub3:
            if v in msc_classes[mscClass]:
                p3_sum_papes_in_a = p3_sum_papes_in_a + used_method[pub3][v]
            else:
                p3_sum_papes_not_in_a = p3_sum_papes_not_in_a + used_method[pub3][v]

    for key in used_method:
        if key == pub1:
            for v in used_method[key]:
                if v == pub2:
                    #print('pub2! 1mal')
                    p2_sum_papes_in_a = p2_sum_papes_in_a + used_method[key][v]
                elif v == pub3:
                    #print('pub3! 1mal')
                    p3_sum_papes_in_a = p3_sum_papes_in_a + used_method[key][v]

        elif key == pub2:
            for v in used_method[key]:
                if v == pub1:
                    #print('pub1! 1mal')
                    p1_sum_papes_in_a = p1_sum_papes_in_a + used_method[key][v]
                elif v == pub3:
                    #print('pub3! 2mal')
                    p3_sum_papes_in_a = p3_sum_papes_in_a + used_method[key][v]

        elif key == pub3:
            for v in used_method[key]:
                if v == pub2:
                    #print('pub2! 2mal')
                    p2_sum_papes_in_a = p2_sum_papes_in_a + used_method[key][v]
                elif v == pub1:
                    #print('pub1! 2mal')
                    p1_sum_papes_in_a = p1_sum_papes_in_a + used_method[key][v]


        else: # to add to all
            for v in used_method[key]:
                if v==pub1:
                    #print('pub1! 1mal!')
                    if key in msc_classes[mscClass]:
                        p1_sum_papes_in_a = p1_sum_papes_in_a + used_method[key][v]
                    else:
                        p1_sum_papes_not_in_a = p1_sum_papes_not_in_a + used_method[key][v]
                elif v == pub2:
                    #print('pub2! 3mal!')
                    if key in msc_classes[mscClass]:
                        p2_sum_papes_in_a = p2_sum_papes_in_a + used_method[key][v]
                    else:
                        p2_sum_papes_not_in_a = p2_sum_papes_not_in_a + used_method[key][v]
                elif v == pub3:
                    #print('pub3! 3mal!')
                    if key in msc_classes[mscClass]:
                        p3_sum_papes_in_a = p3_sum_papes_in_a + used_method[key][v]
                    else:
                        p3_sum_papes_not_in_a = p3_sum_papes_not_in_a + used_method[key][v]


    print('%s _sum_papes_in_a is' % pub1, p1_sum_papes_in_a)
    print('%s _sum_papes_not_in_a' % pub1, p1_sum_papes_not_in_a)

    print('%s _sum_papes_in_a' % pub2, p2_sum_papes_in_a)
    print('%s _sum_papes_not_in_a' % pub2, p2_sum_papes_not_in_a)

    print('%s _sum_papes_in_a' % pub3, p3_sum_papes_in_a)
    print('%s _sum_papes_not_in_a' % pub3, p3_sum_papes_not_in_a)

    aver_p1_papes_in_a = p1_sum_papes_in_a/pubs_in_a
    aver_p1_papes_not_in_a = p1_sum_papes_not_in_a / pubs_not_in_a
    aver_p1_all_pubs = (p1_sum_papes_in_a + p1_sum_papes_not_in_a)/total_pubs

    aver_p2_papes_in_a = p2_sum_papes_in_a/pubs_in_a
    aver_p2_papes_not_in_a = p2_sum_papes_not_in_a / pubs_not_in_a
    aver_p2_all_pubs = (p2_sum_papes_in_a + p2_sum_papes_not_in_a)/total_pubs

    aver_p3_papes_in_a = p3_sum_papes_in_a/pubs_in_a
    aver_p3_papes_not_in_a = p3_sum_papes_not_in_a / pubs_not_in_a
    aver_p3_all_pubs = (p3_sum_papes_in_a + p3_sum_papes_not_in_a)/total_pubs

    print('%s aver_papes_in_a' % pub1, aver_p1_papes_in_a)
    print('%s aver_papes_not_in_a' % pub1, aver_p1_papes_not_in_a)
    print('%s aver_all_pubs' % pub1, aver_p1_all_pubs)

    print('%s aver_p2_papes_in_a' % pub2, aver_p2_papes_in_a)
    print('%s aver_p2_papes_not_in_a' % pub2, aver_p2_papes_not_in_a)
    print('%s aver_p2_all_pubs' % pub2, aver_p2_all_pubs)

    print('%s aver_p3_papes_in_a' % pub3, aver_p3_papes_in_a)
    print('%s aver_p3_papes_not_in_a' % pub3, aver_p3_papes_not_in_a)
    print('%s aver_p3_all_pubs' % pub3, aver_p3_all_pubs)


    try:
        p1_in_a_to_p1_not_in_a = aver_p1_papes_in_a / aver_p1_papes_not_in_a
    except:
        print('Zero division at aver_p1_papes_in_a/aver_p1_papes_not_in_a for %s' % pub1)
        p1_in_a_to_p1_not_in_a = 0

    try:
        p1_in_a_to_all = aver_p1_papes_in_a / aver_p1_all_pubs
    except:
        print('Zero division at aver_p1_papes_in_a/aver_p1_all_pubs for %s' % pub1)
        p1_in_a_to_all = 0

    try:
        p2_in_a_to_p2_not_in_a = aver_p2_papes_in_a / aver_p2_papes_not_in_a
    except:
        print('Zero division at aver_p2_papes_in_a/aver_p2_papes_not_in_a for %s' % pub2)
        p2_in_a_to_p2_not_in_a = 0

    try:
        p2_in_a_to_all = aver_p2_papes_in_a / aver_p2_all_pubs
    except:
        print('Zero division at aver_p2_papes_in_a/aver_p2_all_pubs for %s' % pub2)
        p2_in_a_to_all = 0

    try:
        p3_in_a_to_p3_not_in_a = aver_p3_papes_in_a / aver_p3_papes_not_in_a
    except:
        print('Zero division at aver_p3_papes_in_a/aver_p3_papes_not_in_a for %s' % pub3)
        p3_in_a_to_p3_not_in_a = 0

    try:
        p3_in_a_to_all = aver_p3_papes_in_a / aver_p3_all_pubs
    except:
        print('Zero division at aver_p3_papes_in_a/aver_p3_all_pubs for %s' % pub3)
        p3_in_a_to_all = 0


    print('%s p1_in_a_to_p1_not_in_a' % pub1 , p1_in_a_to_p1_not_in_a)
    print('%s p1_in_a_to_all' % pub1, p1_in_a_to_all)

    print('%s p2_in_a_to_p1_not_in_a' % pub2, p2_in_a_to_p2_not_in_a)
    print('%s p2_in_a_to_all' % pub2, p2_in_a_to_all)

    print('%s p3_in_a_to_p1_not_in_a' % pub3, p3_in_a_to_p3_not_in_a)
    print('%s p3_in_a_to_all' % pub3, p3_in_a_to_all)


if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
