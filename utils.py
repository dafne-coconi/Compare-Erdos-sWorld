
from datetime import datetime
import random
import math

class Nodo:
   """
   Clase Nodo
   :param value: number of nodes
   """
   def __init__(self, name):
      self.name = f'N{name}'
      #self.node_list = list()
      self.nodos_adyacentes = list()
      self.nodo_explored = 0
      self.degree = 0
      
   def get_node_list(self, m = 1, n = 1, simple = 0):

      if simple == 0:
         list_of_lists = [[0 for i in range(1, n + 1)] for _ in range(m)]
         num_nodos = 0
         for i in range(m):
            for j in range(n):
               #print(list_of_lists[i][j])
               num_nodos += 1
               node = self.get_name(f'{num_nodos}')
               list_of_lists[i][j] = node
               #print(list_of_lists)
      elif simple == 1:
         list_of_lists = [0] * n
         for i in range(n):
            node = self.get_name(f'{i+1}')
            list_of_lists[i] = node
 
      self.node_list = list_of_lists

      return self.node_list
   
   def nodo_list_geo(self, n = 1):
      list_of_lists = [[0 for i in range(1, 4)] for _ in range(n)]
      #print(list_of_lists)
      for i in range(len(list_of_lists)):
         node = self.get_name(f'{i+1}')
         list_of_lists[i][0] = node
         list_of_lists[i][1] = random.random()
         list_of_lists[i][2] = random.random()

      #self.node_list = 
      return list_of_lists
   
   def add_nodos_adyacentes(self, nodo):
      self.nodos_adyacentes.append(nodo)
      self.degree = self.degree + 1

   def remove_nodo_adyacente(self, nodo_ad):
      self.nodos_adyacentes.remove(nodo_ad)
      self.degree = self.degree - 1
   
   def explored(self):
      self.nodo_explored = 1

   def not_explored(self):
      self.nodo_explored = 0

   def __key(self):
      return self.name

   def __hash__(self):
      return hash(self.__key())
      
   def __repr__(self):
      return f'{self.name}'
   
   def __cmp__(self, other):
      return self.name == other.name
   def __eq__(self, other):
      return self.name == other.name


class Arista_undirected:
   """
   Clase Arista
   :param value: number of nodes
   """
   
   def __init__(self, n1: Nodo, n2: Nodo, weight = random.randint(2,50)):
      self.n1 = n1
      self.n2 = n2
      self.lista_arista = list()
      self.weight = weight
      self.is_explored = 0
        
   def get_n1(self):
      return self.n1

   def get_n2(self):
      return self.n2
   
   def create_list_arista(self):
      #self.lista_arista = [self.n1, self.n2, self.weight]
      self.lista_arista = [self.n1, self.n2]
      self.n1.add_nodos_adyacentes(self.n2)
      self.n2.add_nodos_adyacentes(self.n1)
      return self.lista_arista
   
   def explored(self):
      self.is_explored = 1
   
   def __repr__(self):
        return f'[{self.n1}, {self.n2}]'
        #return f'({self.n1}, {self.n2})
        # 
   def __key(self):
      return (self.n1.name, self.n2.name)

   def __hash__(self):
      return hash(self.__key())
   
   def __cmp__(self, other):
      return (self.n1.name == other.n1.name and self.n2.name == other.n2.name) or (self.n1.name == other.n2.name and self.n2.name == other.n1.name)

   def __eq__(self, other):
      return (self.n1.name == other.n1.name and self.n2.name == other.n2.name) or (self.n1.name == other.n2.name and self.n2.name == other.n1.name)


class Grafo:
   """
   Clase Grafo
   """
   def __init__(self, name, nodes_list, directed):
      self.name = name
      self.nodes_list = nodes_list
      self.directed = directed
      self.edges_list = []
      self.graph_dict = dict()
      self.capas = dict()
      self.bfs_dict = dict()
      self.dfs_i_dict = dict()
      self.dfs_r_dict = dict()
      self.dijkstra_dict = dict()
      self.prim_dict = dict()
      self.dict_distance_node = {}
      self.nodos_drawed_dict = dict()
      self.vec_fuerzas = dict()
      #for node in self.nodes_list:
       #  self.dfs_r_dict[node] = []
    
   def new_edge(self, n1: Nodo, n2: Nodo, weight = random.randint(2,50)):
      self.n1 = n1
      self.n2 = n2
      """
      Insert an edge to the list of edges in the graph
      :param n1: starting node of the edge
      :param n2: ending node of the edge
      """
      edge = Arista_undirected(n1, n2, weight)
      
      #print(edge)
      if edge not in self.edges_list: 
         self.edges_list.append(edge)
         edge.create_list_arista()

   def simplify_list_node(self):
      new_node_list = list()
      for i in range(len(self.nodes_list)):
         if (len(self.nodes_list[i]) > 1):
            for j in self.nodes_list[i]:
               new_node_list.append(j)
         else:
            new_node_list.append(self.nodes_list[i])
      
      self.nodes_list = new_node_list
      
      return self.nodes_list
   
   def distance_nodes(self, node_1, node_2):
      distance_nodes = math.sqrt((node_1[1] - node_2[1])**2 + (node_1[2] - node_2[2])**2)
      return distance_nodes
   
   def node_in_out(self, node):
      list_node_in_out = list()
      for nodes in self.edges_list:
         if (node in nodes):
            if (nodes.index(node) == 0):
               if (nodes[1] not in list_node_in_out):
                  list_node_in_out.append(nodes[1])
            else:
               if (nodes[1] not in list_node_in_out):
                  list_node_in_out.append(nodes[0])
      return list_node_in_out
   
   def create_graph_notation(self):
      """
      if (self.name == "geografico_simple"):
         new_list_node =  []
         for node in self.nodes_list:
            new_list_node.append(node[0])
         self.nodes_list = new_list_node
         """
      #print(f'Node in node list {type(self.nodes_list[0])}')
      for node in self.nodes_list:
         self.graph_dict[node] = []

      changing_edges_list = self.edges_list
      for node in self.nodes_list:
         list_value = list()
         #print(node.name)
         for edge in changing_edges_list: 
            #if (node.name == str(edge).split(",",2)[0].split("[")[1]):
            if (node == edge.n1):
               #print("true dat")
               #list_value.append(str(edge).split(",",2)[1].strip())
               list_value.append(edge.n2)
               #changing_edges_list.remove(edge)
            
         self.graph_dict[node] = list_value
      #print(f'Nodes {self.nodes_list}')
      #print(f'Edges {self.edges_list}')
      #print(f'Graph {self.graph_dict}')

   def save_graph(self, type_graph: str ):
      current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
      if type_graph == "BFS":
         graph = self.bfs_dict
         #print(f'Imprimir {graph}')
         filename = f"{self.name}_BFS_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "DFS_R":
         graph = self.dfs_r_dict
         #print(f'Imprimir {graph}')
         filename = f"{self.name}_DFS_R_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "DFS_I":
         graph = self.dfs_i_dict
         #print(f'Imprimir {graph}')
         filename = f"{self.name}_DFS_I_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "DIJKSTRA":
         graph = self.dijkstra_dict
         filename = f"{self.name}_DIJKSTRA_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "PRIM":
         graph = self.prim_dict
         filename = f"{self.name}_PRIM_{len(self.nodes_list)}_{current_datetime}.dot"
      else:
         graph = self.graph_dict
         #print(f'grafo regular {self.graph_dict}')
         filename = f"{self.name}_{len(self.nodes_list)}_{current_datetime}.dot"
   
      
          
      filepath = f"archivos/{filename}"

      list_v = []
      with open(filepath, "w", encoding="UTF") as file:
         file.write(f"graph {self.name}" + "{\n")
         count = 0
         line = str
         for key in graph:
            value = graph[key]
            #print(value)
            if (len(value) > 0):
        
               for single_value in value:
                  if key == single_value:
                     continue
                  #print(single_value)
                  #line = f'{key} ->' + '{' + f'{value_as_string}' + '}\n'
                  if type_graph == "DIJKSTRA" or type_graph == "PRIM":
                     line = f'{single_value}_{self.dict_distance_node[single_value]} -> ' + f'{key}_{self.dict_distance_node[key]}' + ';\n'
                     file.write(line)
                  else:
                     line = f'{key} -> ' + f'{single_value}' + ';\n'
                     file.write(line)

            else:
               if type_graph == "DIJKSTRA" or type_graph == "PRIM":
                  line = f'{key}_0'+ '\n'
               else:
                  line = f'{key}'+ '\n'
               file.write(line)
            
            
         file.write("\n}")

      #print(self.edges_list)
      print(f"Graph saved to {filepath} ")

   def save_graph_edges(self, type_graph: str,  new_edges_list):
      current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
      if type_graph == "BFS":
         filename = f"{self.name}_BFS_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "DFS_R":
         filename = f"{self.name}_DFS_R_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "DFS_I":
         filename = f"{self.name}_DFS_I_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "DIJKSTRA":
         filename = f"{self.name}_DIJKSTRA_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "KrustalD":
         filename = f"{self.name}_KrustalD_{len(self.nodes_list)}_{current_datetime}.dot"
      elif type_graph == "KrustalI":
         filename = f"{self.name}_KrustalI_{len(self.nodes_list)}_{current_datetime}.dot"
      else:
         filename = f"{self.name}_edges_{len(self.nodes_list)}_{current_datetime}.dot"
   
      
          
      filepath = f"archivos/{filename}"

      list_v = []
      with open(filepath, "w", encoding="UTF") as file:
         file.write(f"graph {self.name}" + "{\n")
         count = 0
         line = str
         for edge in new_edges_list:
            
            line = f'{edge.n1} -> ' + f'{edge.n2}[Label={edge.weight}]' + ';\n'
            file.write(line)
            
         file.write("\n}")

      #print(self.edges_list)
      print(f"Graph saved to {filepath}")

   def not_explored_nodes(self):
      for node in self.nodes_list:
         node.not_explored()


