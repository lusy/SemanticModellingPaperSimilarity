import networkx as nx
import timeit
import sys

def main(args):
    G = nx.read_graphml('../data/testdata/head200_parsedcomplete_graphml.graphml')

    sim_pub = dict()

    t = 10 #maximum depth
    # Weights of the different kinds of edges
    w_cit = 0.5
    w_key = 0.8
    w_sour = 0.2
    w_auth = 0.3
    w_year = 0.2

    #Normalization?????

    for a in G.nodes_iter():
        # we compute similarity for publications only
        if G.node[a]['Class'] == 'Publication':
            # compute all paths of the length <= t, with source a
            # for all publication nodes p lying on these paths:
                # compute sim(a,p) (look up if sim(p,a) already exists)
                # sim(a,p) = sum(all paths between a and p) <- Normalization???


if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
