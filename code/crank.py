import networkx as nx
#import numpy
import timeit
import sys

'''Implementation of C-Rank for testing purposes'''

def main(args):
    #G = nx.Graph()

    ###### Graph Nr 1 ###############################################
    #G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'})])

    #G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])
    #################################################################

    ###### Graph Nr 2 ###############################################
    #G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'})])

    #G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])
    #################################################################

    ###### Graph Nr 3 ###############################################
    #G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Publication_3', {'Class':'Publication'})])

    #G.add_edges_from([('Publication_3', 'Publication_1', {'Relation':'cites'}), ('Publication_2', 'Publication_3', {'Relation':'cites'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])
    #################################################################

    ###### Graph Nr 4 ###############################################
    #G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Publication_3', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'}), ('Year_1', {'Class':'PublicationYear'}), ('Year_2', {'Class':'PublicationYear'}), ('Source_1', {'Class':'Source'}), ('Source_2', {'Class':'Source'}), ('Author_1', {'Class':'Author'}), ('Author_2', {'Class':'Author'}), ('Author_3', {'Class':'Author'})])

    #G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_1', 'Year_1', {'Relation':'wasPublishedInYear'}), ('Publication_1', 'Author_1', {'Relation':'hasAuthor'}), ('Publication_1', 'Source_1', {'Relation':'isPublishedIn'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Year_2', {'Relation':'wasPublishedInYear'}), ('Publication_2', 'Source_2', {'Relation':'isPublishedIn'}), ('Publication_2', 'Author_1', {'Relation':'hasAuthor'}), ('Publication_2', 'Author_2', {'Relation':'hasAuthor'}), ('Publication_3', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_3', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_3', 'Source_1', {'Relation':'isPublishedIn'}), ('Publication_3', 'Author_3', {'Relation':'hasAuthor'}), ('Publication_3', 'Year_2', {'Relation':'wasPublishedInYear'}), ('Publication_1', 'Publication_2', {'Relation':'cites'}), ('Publication_1', 'Publication_3', {'Relation':'cites'})])
    #################################################################

    G = nx.read_graphml('../data/testdata/head200_parsedcomplete_graphml.graphml')

    sim_pub = dict()

    c = 0.6 #damping factor
    k = 7 # number of iterations

    #initialization
    for a in G.nodes_iter():
        if G.node[a]['Class'] == 'Publication':
            sim_pub[a]={}
        else:
            pass
            #there are only publications and keywords in the current graph

    ctr_init = 0
    for a in G.nodes_iter():
        ctr_init = ctr_init + 1
        print("initializing node %d" % ctr_init)
        for b in G.nodes_iter():
            if G.node[a]['Class'] == 'Publication' and G.node[b]['Class'] == 'Publication':
                #if sim_pub[b][a] (the symmetric case) already there
                try:
                    #we don't actually need to compute anything
                    publication_similarity = sim_pub[b][a]
                except:
                    if a==b:
                        sim_pub[a][b] = 1
                    # try to optimize: we dont actually need to store all the zeroes...
                    #else:
                        #sim_pub[a][b] = 0
            else:
                pass
                # a and b belong to different classes and are dissimilar

    #print("sim_pub: ", sim_pub)
    #print("sim_key: ", sim_key)

    #iteration
    while k>0:
        k = k-1
        nodectr = 0
        for a in G.nodes_iter():
            nodectr = nodectr + 1
            print ("in iteration %d, begin computing node %d" % (k, nodectr))
            for b in G.nodes_iter():
                if a!=b: #otherwise is similarity = 1
                    if G.node[a]['Class']=='Publication' and G.node[b]['Class'] == 'Publication':
                        pubValue = 0
                        neighborsOfA = list()
                        neighborsOfB = list()
                        for na in G.neighbors_iter(a):
                            neighborsOfA.append(na)
                            for nb in G.neighbors_iter(b):
                                neighborsOfB.append(nb)
                                try:
                                    pubValue = pubValue + sim_pub[na][nb] # we just have a look at citations
                                except:
                                    try:
                                        pubValue = pubValue + sim_pub[nb][na]
                                    except:
                                        pubValue = pubValue + 0

                        #print("Debuging key..................")
                        #print('a: ', a)
                        #print('b: ', b)
                        #print('neighbors of a: ', G.neighbors(a))
                        #print('neighbors of b: ', G.neighbors(b))
                        #print('keywordvalue: ', keywordValue)
                        #print('NeighborsOfA: ', neighborsOfA)
                        #print('NeighborsOfB: ', neighborsOfB)

                        # only update similarity, if computed score not zero
                        if pubValue != 0:
                            try:
                                exist_sim = sim_pub[a][b]
                                sim_pub[a][b] = c*pubValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))
                            except:
                                try:
                                    exist_sim = sim_pub[b][a]
                                    sim_pub[b][a] = c*pubValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))
                                # if none of them was saved yet because they were both zero, save it now
                                except:
                                    sim_pub[a][b] = c*pubValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))


                        #print('sim_key: ', sim_key[a][b])

                    else:
                        pass
                        #do nothing, both nodes belong to different classes

        #pretty print
        #print('Next iteration\n')

        #print("------sim_pub------\n")
        #for i in sim_pub.iterkeys():
            #print(i)
            #print(sim_pub[i])


        #print ('sim_pub is: ', sim_pub)
        #print('\n')

#Print final results
    f = open('output_crank_head200', 'w')
    f.write("------sim_pub------\n")
    for i in sim_pub.iterkeys():
        f.write(str(i))
        f.write(": ")
        f.write(str(sim_pub[i]))
        f.write('\n\n')

    f.write('\n')
    f.close()

if __name__ == "__main__":
    t = timeit.Timer("main(args)", "from __main__ import main; args=%r" % sys.argv[1:])
    print t.timeit(number=1)
