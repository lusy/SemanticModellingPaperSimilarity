import sys
import timeit
import re

sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx

def main(args):
    # data import
    G = nx.read_graphml('../data/pubs_till_1975_no_count')

    dict_pubs_indices, dict_indices_pubs = map_pubs_to_matrix_indices(G)
   
    #For all MSC Klasses, find out which publication is in class
    msc_classes = dict()
    msc_classes_aggregated = dict()

    dict_pubs_msc_classes = dict()
    
#    for msc, nbrsdict in G.adjacency_iter():
#        if G.node[msc]["Class"]=="MSC_Class":
#            for pub, eattr in nbrsdict.items():
#                if eattr.items()[0][1]["Relation"]=="hasClassificationCode":
#                    try:
#                        class_exists = msc_classes[msc]
#                        msc_classes[msc].append(pub)
#                    except:
#                        msc_classes[msc] = [pub]
#
#    #for cl in msc_classes:
#        #print("In class %s, there are pubs:" % cl, msc_classes[cl])

### 
    pattern = '([0-9]{2})[A-Z\-][0-9xX]{2}'

    for msc, nbrsdict in G.adjacency_iter():
        if G.node[msc]['Class']=='MSC_Class':
            for pub, eattr in nbrsdict.items():
                if eattr.items()[0][1]['Relation']=='hasClassificationCode':
                    first3digits = re.findall(pattern, msc)
                    if first3digits != []:
                        # fill in msc_classes_aggregated
                        try:
                            class_exists = msc_classes_aggregated[first3digits[0]]
                                # check if publication already belongs to the class
                                if pub not in msc_classes_aggregated[first3digits[0]]:
                                    msc_classes_aggregated[first3digits[0]].append(pub)
                        except:
                            msc_classes_aggregated[first3digits[0]] = [pub]

                        # fill in dict_pubs_msc_classes
                        try:
                            pub_exists = dict_pubs_msc_classes[pub]
                            dict_pubs_msc_classes.append(first3digits[0])
                        except:
                            dict_pubs_msc_classes[pub]=first3digits

                    else:
                        print('first3digits empty, msc is: ', msc)

    msc_classes_aggregated['other']=[]
    # find out which publications have no class, assign them to class 'other'
    for p in dict_pubs_indices.keys():
        try:
            pub_has_class = dict_pubs_msc_classes[p]
        except:
            msc_classes_aggregated['other'].append(p)
            dict_pubs_msc_classes[p] = 'other'


def map_pubs_to_matrix_indices(g):
    dict_pubs_indices = dict()
    dict_indices_pubs = dict()
    ctr = 0

    for a in g.nodes_iter():
        if g.node[a]['Class'] == 'Publication':
            ctr = ctr +1
            dict_pubs_indices[a] = ctr
            dict_indices_pubs[ctr] = a
            
    return dict_pubs_indices, dict_indices_pubs
                       

if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)


