import networkx as nx
import timeit
import sys

def find_all_paths_max_depth(graph, start, end, maxd, currentd=0, path=[]):
    if currentd > maxd:
        return []
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_node(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths_max_depth(graph, node, end, maxd, currentd+1, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def main(args):
    G = nx.read_graphml('../data/testdata/head200_parsedcomplete_graphml.graphml')

    sim_pub = dict()

    t = 10 #maximum depth
    d = 0.04 #decay factor
    # Weights of the different kinds of edges
    w_cit = 0.5
    w_key = 0.8
    w_sour = 0.2
    w_auth = 0.3
    w_year = 0.2

    #Normalization?????

    #TODO: similarity dict initialize

    for a in G.nodes_iter():
        # we compute similarity for publications only
        if G.node[a]['Class'] == 'Publication':
            sim_pub[a] = {}
            for b in G.nodes_iter():
                if G.node[b]['Class'] == 'Publication':
                    #for every two publication check
                    #whether similarity already computed
                    try:
                        exist_sim = sim_pub[b][a] #do nothing
                    except:
                        #whether shortest path(a,b) <=t -> otherwise similarity=0, will not be saved
                        try:
                            for path in find_all_paths_max_depth(G, a, b, t):
                                pathValue = 0
                                for node in path:
                                    if node == a:
                                        pass
                                    elif node == b:
                                        pass
                                    elif G.node[a]['Class'] == 'Keyword':

                                    elif G.node[a]['Class'] == 'Author':

                                    elif G.node[a]['Class'] == 'PublicationYear':

                                    elif G.node[a]['Class'] == 'Source':

                                    elif G.node[a]['Class'] == 'Publication':

                                    else:
                                        pass
                        except:
                            pass # no path in all paths mit max depth t, similarity=0 and wont be saved

            # compute all paths of the length <= t, with source a
            # for all publication nodes p lying on these paths:
                # compute sim(a,p) (look up if sim(p,a) already exists)
                # sim(a,p) = sum(all paths between a and p) <- Normalization???


if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
