import networkx as nx
from pandas import *
from matplotlib.pyplot import *
from math import sqrt

def CSV2Graph(emplacement,distance_communication=40000):
    csv = read_csv(emplacement)

    graphe = nx.Graph()

    for index, row in csv.iterrows():
        graphe.add_node(index, pos=(row['x'], row['y'], row['z']))

    def distance_eucl(point1, point2):
        return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

    for i in range(len(csv)):
        for j in range(i + 1, len(csv)):
            pos_i = graphe.nodes[i]['pos']
            pos_j = graphe.nodes[j]['pos']
            # print(distance_eucl(pos_i, pos_j) < distance_communication)
            if distance_eucl(pos_i, pos_j) < distance_communication:
                graphe.add_edge(i, j)

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

def AllGraphs():
    topologies = ["csv/topology_low.csv","csv/topology_avg.csv","csv/topology_high.csv"]
    ranges = [20000,40000,60000]

    graphes = []
    for i in range(len(topologies)):
        s_graphes = []
        for j in range(len(ranges)):
            s_graphes.append(CSV2Graph(topologies[i],ranges[j]))
        graphes.append(s_graphes)

    return graphes




# Afficher tous les graphes
# for graphe_k in AllGraphs():
#     for graphe in graphe_k:
#         Graph2Plot(graphe)


