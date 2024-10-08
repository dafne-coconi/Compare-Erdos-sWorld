#import snap
import numpy as np
import matplotlib.pyplot as plt
from utils import Nodo, Arista_undirected, Grafo
import random

# Setup
erdosRenyi = None
smallWorld = None
collabNet = None

def get_node_list(m = 1, n = 1, simple = 0):

      if simple == 0:
         list_of_lists = [[0 for i in range(1, n + 1)] for _ in range(m)]
         #print(list_of_lists)
         num_nodos = 0
         for i in range(m):
            for j in range(n):
               #print(list_of_lists[i][j])
               num_nodos += 1
               node = Nodo(f'{num_nodos}')
               list_of_lists[i][j] = node
               #print(list_of_lists)
      elif simple == 1:
         list_of_lists = [0] * n
         for i in range(n):
            node = Nodo(f'{i+1}')
            list_of_lists[i] = node
            #print(list_of_lists)
      #print(list_of_lists)

      return list_of_lists

def get_node_list_fList(a_list):
    list_of_lists = list()
    for i in a_list:
        node = Nodo(f'{i}')
        list_of_lists.append(node)
    
    return list_of_lists

# Problem 1.1
#def genErdosRenyi(N=5242, E=14484, dirigido = False):
def genErdosRenyi(N=52, E=144, dirigido = False):
    """
    :param - N: number of nodes
    :param - E: number of edges

    return type: snap.PUNGraph
    return: Erdos-Renyi graph with N nodes and E edges
    """
    ############################################################################
    # TODO: Your code here!
    Graph = None

    if E < N - 1:
       return "m debe ser mayor a n"
   
    list_nodos = get_node_list(n = N, simple = 1)
    #list_nodos = nodo.get_node_list(n = n, simple = 1)

    grafo = Grafo("erdos_renyi", list_nodos, directed = dirigido)
   
    for _ in range(E):
       #rand_sample_list = random.sample(grafo.nodes_list, 2)
       rand_sample_list = random.sample(list_nodos, 2)

       if (rand_sample_list[0] != rand_sample_list[1]):
          grafo.new_edge(rand_sample_list[0], rand_sample_list[1], random.randint(2,50))
   
    grafo.create_graph_notation()
   
    grafo.not_explored_nodes()
    grafo.save_graph_edges(type_graph = grafo.name, new_edges_list = grafo.edges_list)

    ############################################################################
    #return Graph
    return grafo


def genCircle(N=5242, dirigido = False):
    """
    :param - N: number of nodes

    return type: snap.PUNGraph
    return: Circle graph with N nodes and N edges. Imagine the nodes form a
        circle and each node is connected to its two direct neighbors.
    """
    ############################################################################
    # TODO: Your code here!
    Graph = None

    list_nodos = get_node_list(n = N, simple = 1)

    grafo = Grafo("circle", list_nodos, directed = dirigido)
   
    for i in range(N):
       grafo.new_edge(list_nodos[i-1], list_nodos[i], weight=1)
   
    grafo.create_graph_notation()
    Graph = grafo

    ############################################################################
    return Graph


def connectNbrOfNbr(Graph, N=5242):
    """
    :param - Graph: snap.PUNGraph object representing a circle graph on N nodes
    :param - N: number of nodes

    return type: snap.PUNGraph
    return: Graph object with additional N edges added by connecting each node
        to the neighbors of its neighbors
    """
    ############################################################################
    # TODO: Your code here!
    for i in range(N//4):
       Graph.new_edge(Graph.nodes_list[4*i-2], Graph.nodes_list[2*i+2], weight = 1)
       Graph.new_edge(Graph.nodes_list[4*i-1], Graph.nodes_list[2*i+3], weight = 1)

    ############################################################################
    return Graph


def connectRandomNodes(Graph, M=4000):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph
    :param - M: number of edges to be added

    return type: snap.PUNGraph
    return: Graph object with additional M edges added by connecting M randomly
        selected pairs of nodes not already connected.
    """
    ############################################################################
    # TODO: Your code here!
    for i in range(M):
       node_1 = random.randint(0, M)
       node_2 = random.randint(0, M)

       if node_1 != node_2:
          Graph.new_edge(Graph.nodes_list[node_1], Graph.nodes_list[node_2], weight = 1)

    ############################################################################
    return Graph


def genSmallWorld(N=5242, E=14484):
    """
    :param - N: number of nodes
    :param - E: number of edges

    return type: snap.PUNGraph
    return: Small-World graph with N nodes and E edges
    """
    Graph = genCircle(N, False)
    Graph = connectNbrOfNbr(Graph, N)
    Graph = connectRandomNodes(Graph, 4000)

    Graph.create_graph_notation()
   
    Graph.not_explored_nodes()
    Graph.save_graph_edges(type_graph = Graph.name, new_edges_list = Graph.edges_list)

    return Graph


def loadCollabNet(path, dirigido = False):
    """
    :param - path: path to edge list file

    return type: snap.PUNGraph
    return: Graph loaded from edge list at `path and self edges removed

    Do not forget to remove the self edges!
    """
    ############################################################################
    # TODO: Your code here!
    Graph = None
    f_nodes_id = list()

    f = open(path, "r")
    for x in f:
        if x[0].isdigit():
            nodes = x.split()
            f_nodes_id.append(nodes[0])
            #grafo.new_edge(list_nodos[int(nodes[0])], list_nodos[int(nodes[1])], weight = 1)
    f_nodes_id = list(set(f_nodes_id))
    
    list_nodos = get_node_list_fList(f_nodes_id)
    grafo = Grafo("CollabNet", list_nodos, directed = dirigido)

    f = open(path, "r")
    for x in f:
        #print(f'lee linea {x}')
        if x[0].isdigit():
            nodes = x.split()
            index_n1 = list_nodos.index(Nodo(f'{nodes[0]}'))
            index_n2 = list_nodos.index(Nodo(f'{nodes[1]}'))
            #print(f'in1 {index_n1} in2 {index_n2}')
            grafo.new_edge(list_nodos[index_n1], list_nodos[index_n2], weight = 1)

    grafo.create_graph_notation()
   
    grafo.not_explored_nodes()
    grafo.save_graph_edges(type_graph = grafo.name, new_edges_list = grafo.edges_list)

    #print(f'From {len(f_nodes_id)}')
    Graph = grafo

    ############################################################################
    return Graph


def getDataPointsToPlot(Graph):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph
    
    return values:
    X: list of degrees
    Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
    """
    ############################################################################
    # TODO: Your code here!
    l_degree = 0
    temp_list = [0] * len(Graph.nodes_list)
    for node in Graph.nodes_list:
        if node.degree > l_degree:
            l_degree = node.degree
        #print(f'Node Degree {node.degree}')
        temp_list[node.degree] = temp_list[node.degree] + 1

    #r_degree = [*range(0, l_degree, 1)]
    X, Y = [*range(0, l_degree, 1)], temp_list[:l_degree]
    #print(Y)

    ############################################################################
    return X, Y


def Q1_1():
    """
    Code for HW1 Q1.1
    """
    global erdosRenyi, smallWorld, collabNet
    erdosRenyi = genErdosRenyi(5242, 14484)
    smallWorld = genSmallWorld(5242, 14484)
    collabNet = loadCollabNet("CA-GrQc.txt", False)
    
    x_erdosRenyi, y_erdosRenyi = getDataPointsToPlot(erdosRenyi)
    plt.loglog(x_erdosRenyi, y_erdosRenyi, color = 'y', label = 'Erdos Renyi Network')
    
    x_smallWorld, y_smallWorld = getDataPointsToPlot(smallWorld)
    plt.loglog(x_smallWorld, y_smallWorld, linestyle = 'dashed', color = 'r', label = 'Small World Network')
    
    x_collabNet, y_collabNet = getDataPointsToPlot(collabNet)
    plt.loglog(x_collabNet, y_collabNet, linestyle = 'dotted', color = 'b', label = 'Collaboration Network')
    
    plt.xlabel('Node Degree (log)')
    plt.ylabel('Proportion of Nodes with a Given Degree (log)')
    plt.title('Degree Distribution of Erdos Renyi, Small World, and Collaboration Networks')
    plt.savefig('Erdos_Small_Collaboration')
    plt.legend()
    plt.show()
    
    


# Execute code for Q1.1
Q1_1()
