import networkx as nx
from pandas import read_csv
from matplotlib.pyplot import *
from math import sqrt

def distance_eucl(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

def carre_distance(pos_i,pos_j):
    return distance_eucl(pos_i,pos_j)**2

def CSV2Graph(emplacement,poids=distance_eucl,distance_communication=40000):
    """
        emplacement : string du fichier csv
        poids : fonction calculant le poids d'une arête, en fonction des deux extrémités
        distance_communication : par défaut 40000, valeur maximale de communication entre 2 satellites
    """
    csv = read_csv(emplacement)

    graphe = nx.Graph()

    for index, row in csv.iterrows():
        graphe.add_node(index, pos=(row['x'], row['y'], row['z']))

    for i in range(len(csv)):
        for j in range(i + 1, len(csv)):
            pos_i = graphe.nodes[i]['pos']
            pos_j = graphe.nodes[j]['pos']

            if distance_eucl(pos_i, pos_j) < distance_communication:
                graphe.add_edge(i, j, weight=poids(pos_i,pos_j))

    return graphe

def Graph2Plot(graphe,avec_labels=True):

    pos = {node: (data['pos'][0], data['pos'][1], data['pos'][2]) for node, data in graphe.nodes(data=True)}

    fig = figure()
    troisDim = fig.add_subplot(111, projection='3d')

    for node, (x, y, z) in pos.items():
        troisDim.scatter(x, y, z, color='blue', s=30)
        if avec_labels:
            troisDim.text(x, y, z, s=str(node), fontsize=10)

    for edge in graphe.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        z = [pos[edge[0]][2], pos[edge[1]][2]]
        troisDim.plot(x, y, z, color='black', linewidth=1)

    

def GraphsInSubplots(graphes, avec_labels=True):
    """
    Affiche les graphes donnés dans une grille 3x3 de subplots.
    
    graphes : liste de graphes à afficher.
    avec_labels : booléen, indique s'il faut afficher les labels des noeuds.
    """
    # Déterminer la taille de la grille
    n = len(graphes)
    rows = cols = 3

    fig, axes = subplots(rows, cols, subplot_kw={'projection': '3d'}, figsize=(15, 15))
    axes = axes.flatten()

    for i, graphe in enumerate(graphes):
        pos = {node: (data['pos'][0], data['pos'][1], data['pos'][2]) for node, data in graphe.nodes(data=True)}

        ax = axes[i] 

        for node, (x, y, z) in pos.items():
            ax.scatter(x, y, z, color='blue', s=30)
            if avec_labels:
                ax.text(x, y, z, s=str(node), fontsize=10)

        for edge in graphe.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            z = [pos[edge[0]][2], pos[edge[1]][2]]
            ax.plot(x, y, z, color='black', linewidth=1)

        ax.grid(True)
        

        ax.set_title(f"Graphe {i+1}")#

    for j in range(n, len(axes)):
        fig.delaxes(axes[j])

    tight_layout()
    show()


def AllGraphs(ranges = [20000,40000,60000],poids=distance_eucl):
    """
        ranges : liste distances pour lesquelles calculer les graphes
        poids : fonction prenant deux positions et calculant un poids associé à l'arête reliant ces deux noeuds
    """
    topologies = ["csv/topology_low.csv","csv/topology_avg.csv","csv/topology_high.csv"]

    graphes = []
    for i in range(len(ranges)):
        s_graphes = []
        for j in range(len(topologies)):
            s_graphes.append(CSV2Graph(topologies[j],poids,ranges[i]))
        graphes.append(s_graphes)

    # En colonne la densité augmente
    # En ligne la distance de communciation augmente
    return graphes

def Partie1():
    ### Toutes les configurations
    GraphsInSubplots([y for x in AllGraphs() for y in x],False)

def CalculCaractéristiques(graphe,cout=None):
    """ 
        graphe : nx.Graph
        cout : par défaut None. Function with three positional arguments: the two endpoints of an edge and the dictionary of edge attributes for that edge. The function must return a number.
    """
    moy_degres = sum(dict(graphe.degree()).values()) / graphe.number_of_nodes()

    distribution_degres = dict(graphe.degree()).values()

    moy_clustering = nx.average_clustering(graphe)
    distribution_clustering = nx.clustering(graphe)

    cliques = list(nx.find_cliques(graphe))
    nb_cliques = len(cliques)
    ordres_cliques = [len(clique) for clique in cliques]

    composantes_connexes = list(nx.connected_components(graphe))
    nb_composantes_connexes = len(composantes_connexes)
    ordres_composantes = [len(component) for component in composantes_connexes]

    pcc = dict(nx.shortest_path_length(graphe,weight=cout))
    distribution_pcc = [length for dico_dist in pcc.values() for length in dico_dist.values()]
    len_distribution_pcc = len(distribution_pcc)

    return {"moy_degres":moy_degres,"distribution_degres":distribution_degres,
            "moy_clustering":moy_clustering,"distribution_clustering":distribution_clustering,
            "nb_cliques":nb_cliques,"ordres_cliques":ordres_cliques,
            "nb_composantes_connexes":nb_composantes_connexes,"ordres_composantes":ordres_composantes,
            "distribution_pcc":distribution_pcc,"len_distribution_pcc":len_distribution_pcc}

def Partie2():
    data=[]
    for graphe_k in AllGraphs():
        data_i=[]
        for graphe in graphe_k:
            data_i.append(CalculCaractéristiques(graphe))
        data.append(data_i)
    
    return data

def Partie3():
    data=[]
    for graphe_k in AllGraphs([60000],poids=carre_distance):
        data_i=[]
        for graphe in graphe_k:
            data_i.append(CalculCaractéristiques(graphe,cout=lambda noeud_a,noeud_b,dico_edge : dico_edge["weight"]))
        data.append(data_i)
    return data

def plotDistribDeg(graphe,cout = None):

    cle = "distribution_degres"
    
    fig, ax = subplots(1, 3, sharex=True, sharey=True, tight_layout=True)
    fig.set_size_inches(8,2, forward= True)
    
    graph = CSV2Graph(graphe,distance_communication=20000)
    dico = CalculCaractéristiques(graph,cout)
    ax[0].title.set_text("20 km")
    ax[0].hist(dico[cle], bins= "auto")

    graph = CSV2Graph(graphe,distance_communication=40000)
    dico = CalculCaractéristiques(graph,cout)
    ax[1].title.set_text("40 km")
    ax[1].hist(dico[cle], bins= "auto")

    graph = CSV2Graph(graphe,distance_communication=60000)
    dico = CalculCaractéristiques(graph,cout)
    ax[2].title.set_text("60 km")
    ax[2].hist(dico[cle], bins= "auto")

    show()

def plotClustering(graphe,cout = None):

    cle = "distribution_clustering"
    
    fig, ax = subplots(1, 3, sharex=True, sharey=True, tight_layout=True)
    fig.set_size_inches(8,2, forward= True)

    graph = CSV2Graph(graphe,distance_communication=20000)
    dico = CalculCaractéristiques(graph,cout)
    ax[0].title.set_text("20 km")
    ax[0].hist(dico[cle].values())

    graph = CSV2Graph(graphe,distance_communication=40000)
    dico = CalculCaractéristiques(graph,cout)
    ax[1].title.set_text("40 km")
    ax[1].hist(dico[cle].values())

    graph = CSV2Graph(graphe,distance_communication=60000)
    dico = CalculCaractéristiques(graph,cout)
    ax[2].title.set_text("60 km")
    ax[2].hist(dico[cle].values())

    show()

def Moyennes():
    data = Partie2()
    moy_deg = [[x["moy_degres"] for x in lst] for lst in data]
    moy_clu = [[x["moy_clustering"] for x in lst] for lst in data]
    return moy_deg, moy_clu

def nbCliques_CompConnexes():
    data = Partie2()
    nbCliques = [[x["nb_cliques"] for x in lst] for lst in data]
    nbConnexes = [[x["nb_composantes_connexes"] for x in lst] for lst in data]
    return nbCliques,nbConnexes

def plotOrdresCliques_CompConnexes():
    data = Partie2()
    ordres_cliques = [[x["ordres_cliques"] for x in lst] for lst in data]
    moy = [[sum(x)/len(x) for x in lst] for lst in ordres_cliques]

    fig, ax = subplots(3,3, sharex=True, sharey=True,tight_layout = True)
    for i in range(3):
        for j in range(3) :
            print(ordres_cliques[i][j])
            ax[i][j].hist(ordres_cliques[i][j], bins= "auto")
    print(moy)
    show()

def plotPcc(graphe,cout=None,poids=distance_eucl):
    
    cle = "distribution_pcc"
    
    fig, ax = subplots(1, 3, sharex=True, sharey=True, tight_layout=True)
    fig.set_size_inches(8,2, forward= True)

    graph = CSV2Graph(graphe,distance_communication=20000,poids=poids)
    dico = CalculCaractéristiques(graph,cout)
    ax[0].title.set_text("20 km - nb pcc = " + str(len(dico[cle])))
    ax[0].hist(dico[cle], bins= "auto")

    graph = CSV2Graph(graphe,distance_communication=40000,poids=poids)
    dico = CalculCaractéristiques(graph,cout)
    ax[1].title.set_text("40 km - nb pcc = " + str(len(dico[cle])))
    ax[1].hist(dico[cle], bins= "auto")

    graph = CSV2Graph(graphe,distance_communication=60000,poids=poids)
    dico = CalculCaractéristiques(graph,cout)
    ax[2].title.set_text("60 km - nb pcc = " + str(len(dico[cle])))
    ax[2].hist(dico[cle], bins= "auto")

    show()

### Main ###

## Partie 1
# Partie1()

## Partie 2
# Partie2()
# plotDistribDeg("csv/topology_avg.csv")
# plotClustering("csv/topology_low.csv")
# print(Moyennes())
# print(nbCliques_CompConnexes())
# plotOrdresCliques_CompConnexes()
# plotPcc("csv/topology_high.c
# sv")

## Partie 3
#plotPcc("csv/topology_high.csv",lambda noeud_a,noeud_b,dico_edge : dico_edge["weight"],carre_distance)

