import networkx as nx
import numpy

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

G = nx.read_graphml('../data/testdata/head200_parsedcomplete_graphml')

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
            #if sim_pub[b][a] (the symmetric case) already there
            try:
                #we don't actually need to compute anything
                publication_similarity = sim_pub[b][a]
            except:
                if a==b:
                    sim_pub[a][b] = 1
                else:
                    sim_pub[a][b] = 0
        elif G.node[a]['Class'] == 'Keyword' and G.node[b]['Class'] == 'Keyword':
            try:
                keyword_similarity = sim_key[b][a]
            except:
                if a==b:
                    sim_key[a][b] = 1
                else:
                    sim_key[a][b] = 0
        elif G.node[a]['Class'] == 'Author' and G.node[b]['Class'] == 'Author':
            try:
                author_similarity = sim_author[b][a]
            except:
                if a==b:
                    sim_author[a][b] = 1
                else:
                    sim_author[a][b] = 0
        elif G.node[a]['Class'] == 'Source' and G.node[b]['Class'] == 'Source':
            try:
                source_similarity = sim_source[b][a]
            except:
                if a==b:
                    sim_source[a][b] = 1
                else:
                    sim_source[a][b] = 0
        elif G.node[a]['Class'] == 'PublicationYear' and G.node[b]['Class'] == 'PublicationYear':
            try:
                year_similarity = sim_year[b][a]
            except:
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
                                    keyPubValue = keyPubValue + sim_key[nka][nkb]

                    authorPubValue = 0
                    authorNeighborsOfA = list()
                    authorNeighborsOfB = list()
                    for naa in G.neighbors_iter(a):
                        if G.node[naa]['Class'] == 'Author':
                            authorNeighborsOfA.append(naa)
                            for nab in G.neighbors_iter(b):
                                if G.node[nab]['Class']== 'Author':
                                    authorNeighborsOfB.append(nab)
                                    authorPubValue = authorPubValue + sim_author[naa][nab]

                    sourcePubValue = 0
                    sourceNeighborsOfA = list()
                    sourceNeighborsOfB = list()
                    for nsa in G.neighbors_iter(a):
                        if G.node[nsa]['Class'] == 'Source':
                            sourceNeighborsOfA.append(nsa)
                            for nsb in G.neighbors_iter(b):
                                if G.node[nsb]['Class']== 'Source':
                                    sourceNeighborsOfB.append(nsb)
                                    sourcePubValue = sourcePubValue + sim_source[nsa][nsb]

                    yearPubValue = 0
                    yearNeighborsOfA = list()
                    yearNeighborsOfB = list()
                    for nya in G.neighbors_iter(a):
                        if G.node[nya]['Class'] == 'PublicationYear':
                            yearNeighborsOfA.append(nya)
                            for nyb in G.neighbors_iter(b):
                                if G.node[nyb]['Class']== 'PublicationYear':
                                    yearNeighborsOfB.append(nyb)
                                    yearPubValue = yearPubValue + sim_year[nya][nyb]


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

                    weighted_pubValue = 0
                    weighted_keyPubValue = 0
                    weighted_authorPubValue = 0
                    weighted_yearPubValue = 0
                    weighted_sourcePubValue = 0

                    if publicationNeighborsOfA != [] and publicationNeighborsOfB != []:
                        weighted_pubValue = l1*c*pubValue / (len(set(publicationNeighborsOfA))*len(set(publicationNeighborsOfB)))

                    if keywordNeighborsOfA != [] and keywordNeighborsOfB != []:
                        weighted_keyPubValue = l2*c*keyPubValue / (len(set(keywordNeighborsOfA))*len(set(keywordNeighborsOfB)))

                    if authorNeighborsOfA != [] and authorNeighborsOfB != []:
                        weighted_authorPubValue =  l3*c*authorPubValue / (len(set(authorNeighborsOfA))*len(set(authorNeighborsOfB)))

                    if yearNeighborsOfA != [] and yearNeighborsOfB != []:
                        weighted_yearPubValue = l4*c*yearPubValue / (len(set(yearNeighborsOfA))*len(set(yearNeighborsOfB)))

                    if sourceNeighborsOfA != [] and sourceNeighborsOfB != []:
                        weighted_sourcePubValue = l5*c*sourcePubValue / (len(set(sourceNeighborsOfA))*len(set(sourceNeighborsOfB)))


                    sim_pub[a][b] = weighted_pubValue + weighted_keyPubValue + weighted_authorPubValue + weighted_yearPubValue + weighted_sourcePubValue

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

                elif G.node[a]['Class'] == 'Author' and G.node[b]['Class'] == 'Author':
                    authorValue = 0
                    neighborsOfA = list()
                    neighborsOfB = list()
                    for na in G.neighbors_iter(a):
                        neighborsOfA.append(na)
                        for nb in G.neighbors_iter(b):
                            neighborsOfB.append(nb)
                            authorValue = authorValue + sim_pub[na][nb] # authors have publications as neighbors

                    sim_author[a][b] = c*authorValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))

                elif G.node[a]['Class'] == 'Source' and G.node[b]['Class'] == 'Source':
                    sourceValue = 0
                    neighborsOfA = list()
                    neighborsOfB = list()
                    for na in G.neighbors_iter(a):
                        neighborsOfA.append(na)
                        for nb in G.neighbors_iter(b):
                            neighborsOfB.append(nb)
                            sourceValue = sourceValue + sim_pub[na][nb] # sources have publications as neighbors

                    sim_source[a][b] = c*sourceValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))

                elif G.node[a]['Class'] == 'PublicationYear' and G.node[b]['Class'] == 'PublicationYear':
                    yearValue = 0
                    neighborsOfA = list()
                    neighborsOfB = list()
                    for na in G.neighbors_iter(a):
                        neighborsOfA.append(na)
                        for nb in G.neighbors_iter(b):
                            neighborsOfB.append(nb)
                            yearValue = yearValue + sim_pub[na][nb] # years have publications as neighbors

                    if neighborsOfA != [] and neighborsOfB != []:
                        sim_year[a][b] = c*yearValue / (len(set(neighborsOfA))*len(set(neighborsOfB)))
                    else:
                        sim_year[a][b] = 0

                else:
                    pass
                    #do nothing, both nodes belong to different classes

    print('Next iteration')
    print ('sim_pub is: ', sim_pub)
    #print ('sim_key is: ', sim_key)
    #print ('sim_author is: ', sim_author)
    #print ('sim_year is: ', sim_year)
    #print ('sim_source is: ', sim_source)
    print('\n')
