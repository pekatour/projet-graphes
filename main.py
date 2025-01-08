import networkx as nx
from pandas import *
from matplotlib.pyplot import *
from math import sqrt

def distance_eucl(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

def CSV2Graph(emplacement,poids,distance_communication=40000):
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
            # print(distance_eucl(pos_i, pos_j) < distance_communication)
            if distance_eucl(pos_i, pos_j) < distance_communication:
                graphe.add_edge(i, j, weight=poids(pos_i,pos_j))

    return graphe

def Graph2Plot(graphe):

    pos = {node: (data['pos'][0], data['pos'][1], data['pos'][2]) for node, data in graphe.nodes(data=True)}

    fig = figure()
    troisDim = fig.add_subplot(111, projection='3d')

    for node, (x, y, z) in pos.items():
        troisDim.scatter(x, y, z, color='blue', s=30)
        troisDim.text(x, y, z, s=str(node), fontsize=10)

    for edge in graphe.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        z = [pos[edge[0]][2], pos[edge[1]][2]]
        troisDim.plot(x, y, z, color='black', linewidth=1)

    show()

def AllGraphs(ranges = [20000,40000,60000],poids=distance_eucl):
    """
        ranges : liste distances pour lesquelles calculer les graphes
        poids : fonction prenant deux positions et calculant un poids associé à l'arête reliant ces deux noeuds
    """
    topologies = ["csv/topology_low.csv","csv/topology_avg.csv","csv/topology_high.csv"]

    graphes = []
    for i in range(len(topologies)):
        s_graphes = []
        for j in range(len(ranges)):
            s_graphes.append(CSV2Graph(topologies[i],poids,ranges[j]))
        graphes.append(s_graphes)

    return graphes

def Partie1():
    for graphe_k in AllGraphs():
        for graphe in graphe_k:
            Graph2Plot(graphe)

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

    return moy_degres,distribution_degres,moy_clustering,distribution_clustering,nb_cliques,ordres_cliques,nb_composantes_connexes,ordres_composantes,pcc,distribution_pcc,len_distribution_pcc

def Partie2():
    data=[]
    for graphe_k in AllGraphs():
        data_i=[]
        for graphe in graphe_k:
            data_i.append(CalculCaractéristiques(graphe))
        data.append(data_i)
    return data

def carre_distance(pos_i,pos_j):
    return distance_eucl(pos_i,pos_j)**2

def Partie3():
    data=[]
    for graphe_k in AllGraphs([60000],poids=carre_distance):
        data_i=[]
        for graphe in graphe_k:
            data_i.append(CalculCaractéristiques(graphe,cout=lambda a,b,c : c["weight"]))
        data.append(data_i)
    return data

print(Partie3())

# print(CSV2Graph("csv/topology_low.csv",distance_eucl).edges())