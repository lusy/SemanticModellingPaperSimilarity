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

def find_all_paths_max_depth_no_end(graph, start, maxd, currentd=0, path=[]):
    if currentd > maxd:
        return []
    path = path + [start]
    #if start == end:
    #    return [path]
    if not graph.has_node(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths_max_depth(graph, node, maxd, currentd+1, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def main(args):
    #G = nx.read_graphml('../data/testdata/head200_parsedcomplete_graphml.graphml')
    G = nx.Graph()
    ###### Graph Nr 2 ###############################################
    G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'}), ('Publication_3', {'Class':'Publication'})])

    G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'}), ('Publication_1', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_3', 'Keyword_3', {'Relation':'hasKeyword'})])
    #################################################################

    ##### Graph Nr 4 ###############################################
    #G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Publication_3', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'}), ('Year_1', {'Class':'PublicationYear'}), ('Year_2', {'Class':'PublicationYear'}), ('Source_1', {'Class':'Source'}), ('Source_2', {'Class':'Source'}), ('Author_1', {'Class':'Author'}), ('Author_2', {'Class':'Author'}), ('Author_3', {'Class':'Author'})])

    #G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_1', 'Year_1', {'Relation':'wasPublishedInYear'}), ('Publication_1', 'Author_1', {'Relation':'hasAuthor'}), ('Publication_1', 'Source_1', {'Relation':'isPublishedIn'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Year_2', {'Relation':'wasPublishedInYear'}), ('Publication_2', 'Source_2', {'Relation':'isPublishedIn'}), ('Publication_2', 'Author_1', {'Relation':'hasAuthor'}), ('Publication_2', 'Author_2', {'Relation':'hasAuthor'}), ('Publication_3', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_3', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_3', 'Source_1', {'Relation':'isPublishedIn'}), ('Publication_3', 'Author_3', {'Relation':'hasAuthor'}), ('Publication_3', 'Year_2', {'Relation':'wasPublishedInYear'}), ('Publication_1', 'Publication_2', {'Relation':'cites'}), ('Publication_1', 'Publication_3', {'Relation':'cites'})])
    #################################################################


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
                        if find_all_paths_max_depth(G, a, b, t) != [] :
                            simPub = 0
                            for path in find_all_paths_max_depth(G, a, b, t):
                                pathValue = 1
                                ptr_node = 0
                                for node in path:
                                    ptr_node = ptr_node + 1
                                    if node == a:
                                        pass
                                    elif node == b and last_node == a:
                                        pathValue = w_cit * d
                                    elif G.node[node]['Class'] == 'Keyword':
                                        pathValue = pathValue * w_key * (d**min(ptr_node-1, len(path)-1-(ptr_node-1)))
                                    elif G.node[node]['Class'] == 'Author':
                                        pathValue = pathValue * w_auth * (d**min(ptr_node-1, len(path)-1-(ptr_node-1)))
                                    elif G.node[node]['Class'] == 'PublicationYear':
                                        pathValue = pathValue * w_year * (d**min(ptr_node-1, len(path)-1-(ptr_node-1)))
                                    elif G.node[node]['Class'] == 'Source':
                                        pathValue = pathValue * w_sour * (d**min(ptr_node-1, len(path)-1-(ptr_node-1)))
                                    elif G.node[node]['Class'] == 'Publication' and G.node[last_node]['Class'] == 'Publication':
                                        pathValue = pathValue * w_cit * (d**min(ptr_node-1, len(path)-1-(ptr_node-1)))

                                    else:
                                        pass
                                    last_node = node
                                simPub = simPub + pathValue

                            sim_pub[a][b] = simPub
                        else:
                            pass # no path in all paths mit max depth t, similarity=0 and wont be saved

            # compute all paths of the length <= t, with source a
            # for all publication nodes p lying on these paths:
                # compute sim(a,p) (look up if sim(p,a) already exists)
                # sim(a,p) = sum(all paths between a and p) <- Normalization???

    #Print final results
    f = open('output_test1', 'w')
    f.write("------sim_pub------\n")
    for i in sim_pub.iterkeys():
        f.write(str(i))
        f.write(": ")
        f.write(str(sim_pub[i]))
        f.write('\n\n')
    f.close()



if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
