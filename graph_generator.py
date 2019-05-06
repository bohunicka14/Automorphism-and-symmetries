import random
import copy
# import numpy
# import matplotlib.pyplot as plt

class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.visited = False

    def degree(self):
        return len(self.edges)


class Edge(object):
    def __init__(self, value, node_from, node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to

class Graph(object):
    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes or []
        self.edges = edges or []
        self.node_names = []
        self._node_map = {} # node_val / node obj

    def set_node_names(self, names):
        """The Nth name in names should correspond to node number N.
        Node numbers are 0 based (starting at 0).
        """
        self.node_names = list(names)

    def number_of_edges(self):
        return len(self.edges)

    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_leaves(self):
        result = 0
        for node in self.nodes:
            if len(node.edges) == 1:
                result += 1
        return result if result != 0 else -1

    def degree_sequence(self):
        result = []
        for node in self.nodes:
            result.append(len(node.edges))
        result.sort(reverse=True)
        return result

    def check_k_regularity(self, k):
        for node in self.nodes:
            if node.degree() != k:
                return False
        return True

    def insert_node(self, new_node_val):
        "Insert a new node with value new_node_val"
        new_node = Node(new_node_val)
        self.nodes.append(new_node)
        self._node_map[new_node_val] = new_node
        return new_node

    def insert_edge(self, new_edge_val, node_from_val, node_to_val):
        "Insert a new edge, creating new nodes if necessary"
        nodes = {node_from_val: None, node_to_val: None}
        for node in self.nodes:
            if node.value in nodes:
                nodes[node.value] = node
                if all(nodes.values()):
                    break
        for node_val in nodes:
            nodes[node_val] = nodes[node_val] or self.insert_node(node_val)
        node_from = nodes[node_from_val]
        node_to = nodes[node_to_val]

        for edge in node_from.edges:
            if edge.node_to == node_from and edge.node_from == node_to:
                return False

        new_edge = Edge(new_edge_val, node_from, node_to)
        # new_edge2 = Edge(new_edge_val, node_to, node_from)
        node_from.edges.append(new_edge)
        node_to.edges.append(new_edge)
        self.edges.append(new_edge)
        return True

    def get_edge_list(self):
        """Return a list of triples that looks like this:
        (Edge Value, From Node, To Node)"""
        return [(e.value, e.node_from.value, e.node_to.value)
                for e in self.edges]

    def get_edge_list_names(self):
        """Return a list of triples that looks like this:
        (Edge Value, From Node Name, To Node Name)"""
        return [(edge.value,
                 self.node_names[edge.node_from.value],
                 self.node_names[edge.node_to.value])
                for edge in self.edges]

    def get_adjacency_list(self):
        """Return a list of lists.
        The indecies of the outer list represent "from" nodes.
        Each section in the list will store a list
        of tuples that looks like this:
        (To Node, Edge Value)"""
        max_index = self.find_max_index()
        adjacency_list = [[] for _ in range(max_index)]
        for edg in self.edges:
            from_value, to_value = edg.node_from.value, edg.node_to.value
            adjacency_list[from_value].append((to_value, edg.value))
        return [a or None for a in adjacency_list]  # replace []'s with None

    def get_adjacency_list_names(self):
        """Each section in the list will store a list
        of tuples that looks like this:
        (To Node Name, Edge Value).
        Node names should come from the names set
        with set_node_names."""
        adjacency_list = self.get_adjacency_list()

        def convert_to_names(pair, graph=self):
            node_number, value = pair
            return (graph.node_names[node_number], value)

        def map_conversion(adjacency_list_for_node):
            if adjacency_list_for_node is None:
                return None
            return map(convert_to_names, adjacency_list_for_node)

        return [map_conversion(adjacency_list_for_node)
                for adjacency_list_for_node in adjacency_list]

    def get_adjacency_matrix(self):
        """Return a matrix, or 2D list.
        Row numbers represent from nodes,
        column numbers represent to nodes.
        Store the edge values in each spot,
        and a 0 if no edge exists."""
        max_index = self.find_max_index()
        adjacency_matrix = [[0] * (max_index+1) for _ in range(max_index+1)]
        for edg in self.edges:
            from_index, to_index = edg.node_from.value, edg.node_to.value
            adjacency_matrix[from_index][to_index] = edg.value
            adjacency_matrix[to_index][from_index] = edg.value
        return adjacency_matrix

    def find_max_index(self):
        """Return the highest found node number
        Or the length of the node names if set with set_node_names()."""
        if len(self.node_names) > 0:
            return len(self.node_names)
        max_index = -1
        if len(self.nodes):
            for node in self.nodes:
                if node.value > max_index:
                    max_index = node.value
        return max_index

    def find_node(self, node_number):
        "Return the node with value node_number or None"
        return self._node_map.get(node_number)

    def _clear_visited(self):
        for node in self.nodes:
            node.visited = False

    def dfs_helper(self, start_node):
        """
        of Depth First Search iterating through a node's edges. The
        output should be a list of numbers corresponding to the
        values of the traversed nodes.
        ARGUMENTS: start_node is the starting Node
        MODIFIES: the value of the visited property of nodes in self.nodes
        RETURN: a list of the traversed node values (integers).
        """
        ret_list = [start_node.value]
        start_node.visited = True
        edges_out = [e for e in start_node.edges
                     if e.node_to.value != start_node.value]
        for edge in edges_out:
            if not edge.node_to.visited:
                ret_list.extend(self.dfs_helper(edge.node_to))
        return ret_list

    def dfs(self, start_node_num):
        """Outputs a list of numbers corresponding to the traversed nodes
        in a Depth First Search.
        ARGUMENTS: start_node_num is the starting node number (integer)
        MODIFIES: the value of the visited property of nodes in self.nodes
        RETURN: a list of the node values (integers)."""
        self._clear_visited()
        start_node = self.find_node(start_node_num)
        return self.dfs_helper(start_node)

    def dfs_names(self, start_node_num):
        """Return the results of dfs with numbers converted to names."""
        return [self.node_names[num] for num in self.dfs(start_node_num)]

    def bfs(self, start_node_num):
        """
        iterating through a node's edges. The output should be a list of
        numbers corresponding to the traversed nodes.
        ARGUMENTS: start_node_num is the node number (integer)
        MODIFIES: the value of the visited property of nodes in self.nodes
        RETURN: a list of the node values (integers)."""
        node = self.find_node(start_node_num)
        self._clear_visited()
        ret_list = []
        # Your code here
        queue = [node]
        node.visited = True

        def enqueue(n, q=queue):
            n.visited = True
            q.append(n)

        def unvisited_outgoing_edge(n, e):
            return ((e.node_from.value == n.value) and
                    (not e.node_to.visited))

        while queue:
            node = queue.pop(0)
            ret_list.append(node.value)
            for e in node.edges:
                if unvisited_outgoing_edge(node, e):
                    enqueue(e.node_to)

        return ret_list

    def bfs_names(self, start_node_num):
        """Return the results of bfs with numbers converted to names."""
        return [self.node_names[num] for num in self.bfs(start_node_num)]


    def node_degree(self, node_val):
        for node in self.nodes:
            if node.value == node_val:
                return node.degree()

        return -1

    def average_distance(self):
        result = 0
        passes = 0

        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                passes += 1
                result += self.node_distance(self.nodes[i], self.nodes[j].value)

        return result/passes

    def node_distance(self, node, node_to_val):
        self._clear_visited()
        queue = [(node, 0)]
        node.visited = True

        def enqueue(n, dist, q=queue):
            n.visited = True
            q.append((n, dist))

        def unvisited_outgoing_edge(n, e):
            return ((e.node_from.value == n.value) and
                    (not e.node_to.visited))

        def unvisited_ingoing_edge(n, e):
            return (((e.node_to.value == n.value) and
                     (not e.node_from.visited)))

        while queue:
            node, dist = queue.pop(0)

            if node.value == node_to_val:
                return dist

            for e in node.edges:
                if unvisited_outgoing_edge(node, e):
                    enqueue(e.node_to, dist + 1)
                if unvisited_ingoing_edge(node, e):
                    enqueue(e.node_from, dist + 1)
        return -1

    def is_path(self):
        degree1 = 0
        degree2 = 0
        for node in self.nodes:
            if node.degree() == 1:
                degree1 += 1
            elif node.degree() == 2:
                degree2 += 1
            else:
                return False

        if degree1 == 2:
            return True

    def is_star(self):
        degree1 = 0
        middle_degree = 0
        for node in self.nodes:
            if node.degree() == 1:
                degree1 += 1
            else:
                middle_degree = node.degree()
        return degree1 == len(self.nodes)-1 and middle_degree == len(self.nodes)-1



    def is_bipartite(self, src):
        # Create a color array to store colors
        # assigned to all veritces. Vertex
        # number is used as index in this array.
        # The value '-1' of  colorArr[i] is used to
        # indicate that no color is assigned to
        # vertex 'i'. The value 1 is used to indicate
        # first color is assigned and value 0
        # indicates second color is assigned.
        colorArr = [-1] * len(self.nodes)

        # Assign first color to source
        colorArr[src] = 1

        # Create a queue (FIFO) of vertex numbers and
        # enqueue source vertex for BFS traversal
        queue = []
        queue.append(src)

        adjacency_matrix = self.get_adjacency_matrix()

        # Run while there are vertices in queue
        # (Similar to BFS)
        while queue:

            u = queue.pop()

            # Return false if there is a self-loop
            if adjacency_matrix[u][u] == 1:
                return False

            for v in range(len(self.nodes)):

                # An edge from u to v exists and destination
                # v is not colored
                if adjacency_matrix[u][v] == 1 and colorArr[v] == -1:

                    # Assign alternate color to this
                    # adjacent v of u
                    colorArr[v] = 1 - colorArr[u]
                    queue.append(v)

                    # An edge from u to v exists and destination
                # v is colored with same color as u
                elif adjacency_matrix[u][v] == 1 and colorArr[v] == colorArr[u]:
                    return False

        # If we reach here, then all adjacent
        # vertices can be colored with alternate
        # color
        return True

    def is_isomorphic(self, g):
        if self.number_of_nodes() != g.number_of_nodes():
            return False
        if self.number_of_edges() != g.number_of_edges():
            return False
        if self.number_of_leaves() != g.number_of_leaves():
            return False
        if self.degree_sequence() != g.degree_sequence():
            return False
        # todo: add other tests

        return True

class GraphGenerator():

    def __init__(self, number_of_nodes):
        self.n = number_of_nodes

    def generate_star(self):
        g = Graph()
        for i in range(1, self.n):
            g.insert_edge(1, 0, i)
        return g

    def generate_path(self):
        g = Graph()
        for i in range(self.n - 1):
            g.insert_edge(1, i, i + 1)
        return g

    def create_all_graphs_by_adding_new_edge(self, graph):
        output = []
        num = graph.number_of_nodes()
        for i in range(num):
            new_graph = copy.deepcopy(graph)
            new_graph.insert_edge(0, i, num+i)
            if not self.check_isomorphism(new_graph, output):
                output.append(new_graph)

        return output

    def generate_graphs(self, graphs):
        output = []
        for g in graphs:
            output.append(self.create_all_graphs_by_adding_new_edge(g))

        return output


    def check_isomorphism(self, graph, graphs = []):
        for g in graphs:
            if graph.is_isomorphic(g):
                return True
        return False

if __name__ == '__main__':
    # 4 vertices graphs
    # g1 = Graph()
    # g2 = Graph()
    #
    # g1.insert_edge(0, 0, 1)
    # g1.insert_edge(0, 1, 2)
    # g1.insert_edge(0, 2, 3)
    #
    # g2.insert_edge(0, 0, 1)
    # g2.insert_edge(0, 0, 2)
    # g2.insert_edge(0, 0, 3)

    gn = GraphGenerator(4)
    path = gn.generate_path()
    star = gn.generate_star()
    out = gn.generate_graphs([path, star])
    print(len(out[0]), len(out[1]))

