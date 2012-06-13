import networkx as nx
import numpy

G = nx.Graph()

###### Graph Nr 1 ###############################################
#G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'})])

#G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])
#################################################################

###### Graph Nr 2 ###############################################
#G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'})])

#G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])
#################################################################

###### Graph Nr 3 ###############################################
G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Publication_3', {'Class':'Publication'})])

G.add_edges_from([('Publication_3', 'Publication_1', {'Relation':'cites'}), ('Publication_2', 'Publication_3', {'Relation':'cites'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])
#################################################################

sim_pub = dict()
sim_key = dict()
sim_year = dict()
sim_author = dict()
sim_source = dict()

l1 = 0.2 #lambda fuer publications
l2 = 0.5 #lambda fuer keywords
l3 = 0.1 #lambda fuer authors
l4 = 0.1 #lambda fuer years
l5 = 0.1 #lambda fuer source
c = 0.7 #damping factor
k = 12

#initialization
for a in G.nodes_iter():
    if G.node[a]['Class'] == 'Publication':
        sim_pub[a]={}
    elif G.node[a]['Class'] == 'Keyword':
        sim_key[a]={}
    elif G.node[a]['Class'] == 'Author':
        sim_author[a]={}
    elif G.node[a]['Class'] == 'PublicationYear':
        sim_year[a]={}
    elif G.node[a]['Class'] == 'Source':
        sim_source[a]={}
    else:
        pass
        #there are only publications and keywords in the current graph


for a in G.nodes_iter():
    for b in G.nodes_iter():
        if G.node[a]['Class'] == 'Publication' and G.node[b]['Class'] == 'Publication':
            if a==b:
                sim_pub[a][b] = 1
            else:
                sim_pub[a][b] = 0
        elif G.node[a]['Class'] == 'Keyword' and G.node[b]['Class'] == 'Keyword':
            if a==b:
                sim_key[a][b] = 1
            else:
                sim_key[a][b] = 0
        elif G.node[a]['Class'] == 'Author' and G.node[b]['Class'] == 'Author':
            if a==b:
                sim_author[a][b] = 1
            else:
                sim_author[a][b] = 0
        elif G.node[a]['Class'] == 'Source' and G.node[b]['Class'] == 'Source':
            if a==b:
                sim_source[a][b] = 1
            else:
                sim_source[a][b] = 0
        elif G.node[a]['Class'] == 'PublicationYear' and G.node[b]['Class'] == 'PublicationYear':
            if a==b:
                sim_year[a][b] = 1
            else:
                sim_year[a][b] = 0

        else:
            pass
            # a and b belong to different classes and are dissimilar

#print("sim_pub: ", sim_pub)
#print("sim_key: ", sim_key)

#iteration
while k>0:
    k = k-1
    for a in G.nodes_iter():
        for b in G.nodes_iter():
            if a!=b: #otherwise is similarity = 1
                if G.node[a]['Class']=='Publication' and G.node[b]['Class'] == 'Publication':
                    pubValue = 0
                    publicationNeighborsOfA = list()
                    publicationNeighborsOfB = list()
                    for na in G.neighbors_iter(a):
                        if G.node[na]['Class'] =='Publication':
                            publicationNeighborsOfA.append(na)
                            for nb in G.neighbors_iter(b):
                                if G.node[nb]['Class'] == 'Publication':
                                    publicationNeighborsOfB.append(nb)
                                    pubValue = pubValue + sim_pub[na][nb]

                    keyPubValue = 0
                    keywordNeighborsOfA = list()
                    keywordNeighborsOfB = list()
                    for nka in G.neighbors_iter(a):
                        if G.node[nka]['Class'] == 'Keyword':
                            keywordNeighborsOfA.append(nka)
                            for nkb in G.neighbors_iter(b):
                                if G.node[nkb]['Class']== 'Keyword':
                                    keywordNeighborsOfB.append(nkb)
                                    keyPubValue = keyPubValue + sim_key[na][nkb]

                    #print("Debugging...............")
                    #print("a: ", a)
                    #print("b: ", b)
                    #print('neighbors of a: ', G.neighbors(a))
                    #print('neighbors of b: ', G.neighbors(b))
                    #print('pubvalue: ', pubValue)
                    #print('publicationNeighborsOfA: ', publicationNeighborsOfA)
                    #print('publicationNeighborsOfB: ', publicationNeighborsOfB)
                    #print('keyPubValue: ', keyPubValue)
                    #print('keywordNeighborsOfA: ', keywordNeighborsOfA)
                    #print('keywordNeighborsOfB: ', keywordNeighborsOfB)

                    if keywordNeighborsOfA == [] or keywordNeighborsOfB == []:
                        sim_pub[a][b] = l1*c*pubValue / (len(set(publicationNeighborsOfA))*len(set(publicationNeighborsOfB)))
                    else:
                        sim_pub[a][b] = l1*c*pubValue / (len(set(publicationNeighborsOfA))*len(set(publicationNeighborsOfB))) + l2*c*keyPubValue / (len(set(keywordNeighborsOfA))*len(set(keywordNeighborsOfB)))

                    #print('sim_pub: ', sim_pub[a][b])

                elif G.node[a]['Class'] == 'Keyword' and G.node[b]['Class'] == 'Keyword':
                    keywordValue = 0
                    neighborsOfA = list()
                    neighborsOfB = list()
                    for na in G.neighbors_iter(a):
                        neighborsOfA.append(na)
                        for nb in G.neighbors_iter(b):
                            neighborsOfB.append(nb)
                            keywordValue = keywordValue + sim_pub[na][nb] # keyword have publications as neighbors

                    #print("Debuging key..................")
                    #print('a: ', a)
                    #print('b: ', b)
                    #print('neighbors of a: ', G.neighbors(a))
                    #print('neighbors of b: ', G.neighbors(b))
                    #print('keywordvalue: ', keywordValue)
                    #print('NeighborsOfA: ', neighborsOfA)
                    #print('NeighborsOfB: ', neighborsOfB)

                    sim_key[a][b] = c*keywordValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))

                    #print('sim_key: ', sim_key[a][b])

                else:
                    pass
                    #do nothing, both nodes belong to different classes

    print('Next iteration')
    print ('sim_pub is: ', sim_pub)
    print ('sim_key is: ', sim_key)
    print('\n')
