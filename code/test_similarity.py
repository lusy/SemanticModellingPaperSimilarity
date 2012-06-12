import networkx as nx
import numpy

G = nx.DiGraph()

G.add_nodes_from([('Publication_1', {'Class':'Publication'}), ('Publication_2', {'Class':'Publication'}), ('Keyword_1', {'Class':'Keyword'}), ('Keyword_2',{'Class':'Keyword'}), ('Keyword_3', {'Class':'Keyword'})])

G.add_edges_from([('Publication_1', 'Keyword_1', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_1', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_2', {'Relation':'hasKeyword'}), ('Publication_2', 'Keyword_3', {'Relation':'hasKeyword'}), ('Publication_1', 'Publication_2', {'Relation':'cites'})])

sim_pub = eye(2)
sim_key = eye(3)

l1 = 0.5 #lambda fuer publications
l2 = 0.5 #lambda fuer keywords
c = 0.8 #damping factor
k = 5

while k>0:
    k = k-1
    for a in G.nodes_iter():
        for b in G.nodes_iter():
            if G.node[a]['Class']=='Publication' and G.node[b]['Class'] == 'Publication':
                pubValue = 0
                for na in neighborsOfA and na['Class'] =='Publication':
                    for nb in neighborsOfB and nb['Class'] == 'Publication':
                        pubValue = pubValue + sim_pub[na][nb]
                keyPubValue = 0
                for na in neighborsOfA and na['Class'] == 'Keyword':
                    for nb in neighborsOfB and nb['Class']== 'Keyword':
                        keyPubValue = keyPubValue + sim_key[na][nb]

                sim_pub[a][b] = l1*c*pubValue / (len(publicationNeighborsOfA)*len(publicationNeighborsOfB)) + l2*c*keyPubValue / (len(keywordNeighborsOfA)*len(keywordNeighborsOfB))

            elif G.node[a]['Class'] == 'Keyword' and G.node[b]['Class'] == 'Keyword':
                keywordValue = 0
                for na in neighborsOfA:
                    for nb in neighborsOfB:
                        keywordValue = keywordValue + sim_pub[na][nb] # keyword have publications as neighbors
                sim_key[a][b] = c*keywordValue / (len(neighborsOfA)*len(neighborsOfB))
            else:
                do nothing, both nodes belong to different classes



