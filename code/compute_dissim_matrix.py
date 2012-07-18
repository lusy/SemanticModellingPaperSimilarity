import sys
import timeit

#sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx

def main(args):
    # data import
    G = nx.read_graphml('../output/graphml_pubs_till_1975_no_count')
    #param1 = open('../output/output_till_1975_pubs_param1').read()
    #param2 = open('../output/output_till_1975_pubs_param2').read()
    #param3 = open('../output/output_till_1975_pubs_param3').read()
    #crank = open('../output/output_crank_till_1975_no_title').read()

    total_pubs = 3095

    #p1 = eval(param1)
    #print('Parametrization 1 read')
    #p2 = eval(param2)
    #print('Parametrization 2 read')
    #p3 = eval(param3)
    #print('Parametrization 3 read')
    #cr = eval(crank)
    #print('Crank read')

    dict_pubs_indices, dict_indices_pubs = map_pubs_to_matrix_indices(G)
    print ("Pubs -> indices: ", dict_pubs_indices)
    print ("----------------------------------------------------------")
    print ("Indices -> pubs: ", dict_indices_pubs)

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

def compute_dissim(distribution_dict):
    pass

if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
