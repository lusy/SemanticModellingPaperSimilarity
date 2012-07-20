import sys
import timeit
import re

sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx
from numpy import *

def main(args):
    # data import
    G = nx.read_graphml('../data/pubs_till_1975_no_count')

    # import crank clustering vector as a test
    f = open("../data/crank_clustering_vector_65_cluster_eval_input")
    clusteringVector = f.read().splitlines()
    #clusteringVector #TODO import it

    # computing classifications
    dict_pubs_indices, dict_indices_pubs = map_pubs_to_matrix_indices(G)
    msc_classes_aggregated, dict_pubs_msc_classes = compute_msc_classes_pubs(G, dict_pubs_indices)
    
    # map msc classes to some indices
    dict_msc_classes_to_indices, dict_indices_to_msc_classes = map_msc_classes_to_indices(msc_classes_aggregated)
       
    # build table cluster/class
    evalTable = zeros((65,65))

    for indOfPub, clusterAssignedToPub in enumerate(clusteringVector):
        # clusteringVector[indOfPub] = clusterAssignedToPub
        pub = dict_indices_pubs[indOfPub+1]

        # for all classes the publication is in, add 1 to row cluster/class
        if type(dict_pubs_msc_classes[pub]) == list :
            for cl in dict_pubs_msc_classes[pub]:
                indOfCl = dict_msc_classes_to_indices[cl]
                evalTable[int(clusterAssignedToPub)-1][indOfCl-1] += 1
        else:
            cl = dict_pubs_msc_classes[pub]
            indOfCl = dict_msc_classes_to_indices[cl]
            evalTable[int(clusterAssignedToPub)-1][indOfCl-1] += 1

    #for l in evalTable:
    #    print l
    
    #print evalTable[0]
    
    total_papes = 6484
    # compute entropie, purity
    entropieVector = []
    purityVector = []
    overallEntropie = 0
    overallPurity = 0

    numberPapesInAllCluster = []
    for cluster in evalTable:
        numberPapesInCluster = 0
        for mscClass in cluster:
            numberPapesInCluster = numberPapesInCluster + mscClass
        
        numberPapesInAllCluster.append(numberPapesInCluster)
        
    #print numberPapesInAllCluster    
 
    # entropie
    for indOfCluster, cluster in enumerate(evalTable):
        entropieOfCurrentCluster = 0
        for mscClass in cluster:
            prob = mscClass / numberPapesInAllCluster[indOfCluster]
            #print ("prob is:", prob)
            if prob != 0:
                entropieOfCurrentCluster += prob*math.log(prob,2)
            #else: do nothing, we should add prob=0 to entropie..    

        entropieVector.append(entropieOfCurrentCluster)    

    #print entropieVector    

    # overall entropie
    for indOfEn, en in enumerate(entropieVector):
        overallEntropie += (numberPapesInAllCluster[indOfEn]/total_papes)*entropieVector[indOfEn]

    #print overallEntropie    
    
    #purity
    for indOfCluster, cluster in enumerate(evalTable):
        purityOfCurrentCluster = 0
        for mscClass in cluster:
            prob = mscClass / numberPapesInAllCluster[indOfCluster]
            purityOfCurrentCluster = max(purityOfCurrentCluster, prob)

        purityVector.append(purityOfCurrentCluster)    

    print purityVector   

    # overall purity
    for indOfPur, pur in enumerate(purityVector):
        overallPurity += (numberPapesInAllCluster[indOfPur]/total_papes) * purityVector[indOfPur]

    print overallPurity    
    

def compute_msc_classes_pubs(G, dict_pubs_indices):
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


    return msc_classes_aggregated, dict_pubs_msc_classes


def map_msc_classes_to_indices(input_dict):
    dict_msc_classes_to_indices = dict()
    dict_indices_to_msc_classes = dict()
    ctr = 0
    
    for cl in input_dict.keys():
        ctr = ctr +1
        dict_msc_classes_to_indices[cl] = ctr
        dict_indices_to_msc_classes[ctr] = cl
        
    return dict_msc_classes_to_indices, dict_indices_to_msc_classes
 


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


