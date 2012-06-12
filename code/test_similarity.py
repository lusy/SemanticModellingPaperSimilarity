import networkx as nx
import numpy

G = nx.DiGraph()

G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'})])

G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])

sim_pub = dict()
sim_key = dict()

l1 = 0.5 #lambda fuer publications
l2 = 0.5 #lambda fuer keywords
c = 0.8 #damping factor
k = 5

#initialization
for a in G.nodes_iter():
    for b in G.nodes_iter():
        if G.node[a]['Class'] == 'Publication' and G.node[b]['Class'] == 'Publication':
            if a==b:
                sim_pub[a][b] = 1
            else:
                sim_pub[a][b] = 0
                sim_pub[b][a] = 0
        elif G.node[a]['Class'] == 'Keyword' and G.node[b]['Class'] == 'Keyword':
            if a==b:
                sim_key[a][b] = 1
            else:
                sim_key[a][b] = 0
                sim_key[b][a] = 0
        else:
            pass
            # a and b belong to different classes and are dissimilar


#iteration
while k>0:
    k = k-1
    for a in G.nodes_iter():
        for b in G.nodes_iter():
            if G.node[a]['Class']=='Publication' and G.node[b]['Class'] == 'Publication':
                pubValue = 0
                publicationNeighborsOfA = list()
                publicationNeighborsOfB = list()
                for na in G.neighbors_iter(a) and G.node[na]['Class'] =='Publication':
                    publicationNeighborsOfA.append(na)
                    for nb in G.neighbors_iter(b) and G.node[nb]['Class'] == 'Publication':
                        publicationNeighborsOfB.append(nb)
                        pubValue = pubValue + sim_pub[na][nb]

                keyPubValue = 0
                keywordNeighborsOfA = list()
                keywordNeighborsOfB = list()
                for na in G.neighbors_iter(a) and G.node[na]['Class'] == 'Keyword':
                    keywordNeighborsOfA.append(na)
                    for nb in G.neighbors_iter(b) and G.node[nb]['Class']== 'Keyword':
                        keywordNeighborsOfB.append(nb)
                        keyPubValue = keyPubValue + sim_key[na][nb]

                sim_pub[a][b] = l1*c*pubValue / (len(publicationNeighborsOfA)*len(publicationNeighborsOfB)) + l2*c*keyPubValue / (len(keywordNeighborsOfA)*len(keywordNeighborsOfB))

            elif G.node[a]['Class'] == 'Keyword' and G.node[b]['Class'] == 'Keyword':
                keywordValue = 0
                neighborsOfA = list()
                neighborsOfB = list()
                for na in neighborsOfA:
                    neighborsOfA.append(na)
                    for nb in neighborsOfB:
                        neighborsOfB.append(nb)
                        keywordValue = keywordValue + sim_pub[na][nb] # keyword have publications as neighbors

                sim_key[a][b] = c*keywordValue / (len(neighborsOfA)*len(neighborsOfB))

            else:
                pass
                #do nothing, both nodes belong to different classes

    print('Next iteration')
    print (sim_pub)
    print (sim_key)

