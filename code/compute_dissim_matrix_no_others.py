import sys
import timeit

sys.path.append("/home/sis/lvaseva/python/lib/python2.6/site-packages")

import networkx as nx
import numpy

'''
Routine for computing distance matrix only for the publications,
for which all metadata is present.
'''

def main(args):
    # data import
    G = nx.read_graphml('../output/graphml_pubs_till_1975_no_count')
    param1 = open('../output/output_till_1975_pubs_param1').read()
    #param2 = open('../output/output_till_1975_pubs_param2').read()
    #param3 = open('../output/output_till_1975_pubs_param3').read()
    #crank = open('../benchmarks/output_crank_till_1975_no_title').read()

    total_pubs = 3095 

    p1 = eval(param1)
    print('Parametrization 1 read')
    #p2 = eval(param2)
    #print('Parametrization 2 read')
    #p3 = eval(param3)
    #print('Parametrization 3 read')
    #cr = eval(crank)
    #print('Crank read')

    dict_pubs_indices, dict_indices_pubs = map_pubs_to_matrix_indices(G)
    #print ("Pubs -> indices: ", dict_pubs_indices)
    #print ("----------------------------------------------------------")
    #print ("Indices -> pubs: ", dict_indices_pubs)

    compute_dissim(p1, dict_pubs_indices)

def map_pubs_to_matrix_indices(g):
    '''
    Only for pubs with all metadata present
    '''
    dict_pubs_indices = dict()
    dict_indices_pubs = dict()
    ctr = 0

    for a in g.nodes_iter():
        if g.node[a]['Class'] == 'Publication':
            # add node a to dict only if a has a neighbor which is not publication
            for na in g.neighbors_iter(a):
                if g.node[na]['Class'] != 'Publication':
                    ctr = ctr +1
                    dict_pubs_indices[a] = ctr
                    dict_indices_pubs[ctr] = a
                    break

    return dict_pubs_indices, dict_indices_pubs

def compute_dissim(distribution_dict, dict_pubs_indices):
    '''
    Only for pubs with all metadata present
    '''
    dissim_matrix = numpy.ones((3095, 3095))

    for pub1 in distribution_dict:
        try:
            pub1_has_metadata = dict_pubs_indices[pub1]
            for pub2 in distribution_dict[pub1]:
                try:
                    pub2_has_metadata = dict_pubs_indices[pub2]
                    i = dict_pubs_indices[pub1] - 1 # -1 cause counting in the dict starts at 1
                    #print("i is:", i)
                    j = dict_pubs_indices[pub2] - 1 # and counting in the dissim_matrix at 0
                    #print('j is:', j)
                    dissim_matrix[i][j] = 1 - (distribution_dict[pub1][pub2])
                    dissim_matrix[j][i] = 1 - (distribution_dict[pub1][pub2])
                    #print('dissim_matrix[i][j] is', dissim_matrix[i][j])
                except:
                    print ("No data for pub %r" % pub2)
        except:
            print ("No data for pub %r" % pub1)

    f = open('test_dissim_matrix_p1_short', 'w')

    ctr = 0
    for i in xrange(0, len(dissim_matrix)):
        for j in xrange(0, len(dissim_matrix)):
            f.write(str(dissim_matrix[i][j]))
            f.write(' ')
            #if dissim_matrix[i][j] != 1:
                #print (ctr, dissim_matrix[i][j])
                #ctr = ctr +1
            #f.write(str(i))
        f.write('\n')

    f.close()

if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
