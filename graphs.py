""" Graph Class
A simple Python graph class, this class holds basic graph operations
"""

class Graph(object):
    def __init__(self, grap_dict=None):
        """ initializes a graph object
        If no directory or None is fiven,
        an empty directionary will be used
        """
        if grap_dict == None:
            graph_dict = {}
        self.__graph_dict = grap_dict
    
    def vertices(self):
        #return the edges of a graph
        return list(self.__graph_dict.keys())
    
    def edges(self):
        #return the edges of a graph
        return self.__generate_edges()
    
    def vertex_degree(self, vertex):
        #The degree of a vertex is the number of edges connecting it
        adj_vertices = self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree
    
    def add_vertex(self, vertex):
        """ If the vertex is not in self.__graph_dict,
            a key "vertex" with an empty
            list as a value is added to the dictionary.
            Ohterwise nothing as to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
    
    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple of list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]
    
    def __generate_edges(self):
        """ A stsatic method generating the edge of the
            graph "graph". Edges are represented as sets
            with one ( a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges
    
    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\edges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res