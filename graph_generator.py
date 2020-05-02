import random
import copy
from networkx import random_tree, draw
import matplotlib.pyplot as plt
import os
import shutil
import datetime
from graph import *
import nautyRunner
# import numpy
import matplotlib.pyplot as plt

class GraphGenerator:

    @staticmethod
    def generate_random_binary_tree(n):
        g = Graph()
        g.insert_node(0)
        tree = [[-1, -1]]
        free_edges = [(0, 0), (0, 1)]
        while g.number_of_nodes() < n:
            e = random.choice(free_edges)
            node, child = e
            assert tree[node][child] == -1

            k = g.number_of_nodes()
            tree.append([-1, -1])
            g.insert_edge(0, node, k)
            free_edges.extend([(k, 0), (k, 1)])
            free_edges.remove(e)

        return g

    @staticmethod
    def generate_random_tree(n):
        tree = random_tree(n)
        g = Graph()
        for edge in tree.edges:
            g.insert_edge(0, edge[0], edge[1])
        # draw(tree)
        # plt.show()
        # plt.savefig('plt.png')
        # g.draw('', False)
        del tree
        return g

    @staticmethod
    def generate_star(n):
        g = Graph()
        for i in range(1, n):
            g.insert_edge(1, 0, i)
        return g

    @staticmethod
    def generate_trivial_graph():
        g = Graph()
        g.insert_node(0)
        return g

    @staticmethod
    def generate_path(n):
        g = Graph()
        for i in range(n - 1):
            g.insert_edge(1, i, i + 1)
        return g

    @staticmethod
    def generate_big_asymemtric_tree(n):
        g = Graph()
        g.insert_edge(0, 0, 1)
        for i in range(n-2):
            _from = g.number_of_nodes() - 1
            _to = g.number_of_nodes()
            g.insert_edge(0, _from, _to)

        for i in range(1, n):
            g.insert_edge(0, i, g.number_of_nodes())
            for j in range(i):
                g.insert_edge(0, g.number_of_nodes()-1, g.number_of_nodes())
        return g

    @staticmethod
    def generate_big_almost_asymmetric_tree(n):
        g1 = GraphGenerator.generate_big_asymemtric_tree(n)
        # print('|Aut(g)| = ', g1.number_of_automorphisms())
        g1.insert_edge(0, 0, g1.number_of_nodes())
        g1.insert_edge(0, 1, g1.number_of_nodes())
        g1.insert_edge(0, g1.number_of_nodes() - 1, g1.number_of_nodes())
        # print('adding new edges')
        # print('|Aut(g)| = ', g1.number_of_automorphisms())
        # g1.draw('', False)

        return g1

    @staticmethod
    def generate_non_isomorphic_graphs(graphs):
        output = []
        for g in graphs:
            num = g.number_of_nodes()
            for i in range(num):
                new_graph = copy.deepcopy(g)
                new_graph.insert_edge(0, i, num)
                if not GraphGenerator.check_isomorphism(new_graph, output):
                    output.append(new_graph)
        return output

    @staticmethod
    def generate_graph_permutations(self, graph):
        pass

    @staticmethod
    def check_isomorphism(graph, graphs=[]):
        for g in graphs:
            if graph.is_isomorphic(g):
                return True
        return False

    @staticmethod
    def join_graphs_by_node(g1, g2, node_g1, node_g2):
        g1_copy = copy.deepcopy(g1)
        g2_copy = copy.deepcopy(g2)
        for node in g1_copy.nodes:
            if node.value == node_g1.value:
                node_g1_copy = node
                break

        for node in g2_copy.nodes:
            if node.value == node_g2.value:
                node_g2_copy = node
                break

        g1_copy.join_other_graph_by_node(node_g1_copy, node_g2_copy, g2_copy)
        if g1_copy.need_to_reevaluate_node_values():
            g1_copy.reevaluate_node_values()

        return g1_copy

    @staticmethod
    def join_graphs_by_edge(g1, g2, node_g1, node_g2):
        g1_copy = copy.deepcopy(g1)
        g2_copy = copy.deepcopy(g2)
        g1_copy.insert_edge(0, node_g1.value, len(g1_copy.nodes))

        for node in g2_copy.nodes:
            if node.value == node_g2.value:
                node_g2_copy = node

        g1_copy.join_other_graph_by_node(g1_copy.nodes[-1], node_g2_copy, g2_copy, 1)
        if g1_copy.need_to_reevaluate_node_values():
            g1_copy.reevaluate_node_values()

        return g1_copy

    @staticmethod
    def join_graphs_by_node_all_possibilities(g1, g2):
        result = []
        if g1.number_of_nodes() >= g2.number_of_nodes():
            for g1_node in g1.nodes:
                for g2_node in g2.nodes:
                    new_graph = GraphGenerator.join_graphs_by_node(g1, g2, g1_node, g2_node)
                    if not GraphGenerator.check_isomorphism(new_graph, result):
                        result.append(new_graph)
        else:
            for g2_node in g2.nodes:
                for g1_node in g1.nodes:
                    new_graph = GraphGenerator.join_graphs_by_node(g2, g1, g2_node, g1_node)
                    if not GraphGenerator.check_isomorphism(new_graph, result):
                        result.append(new_graph)

        return result

    @staticmethod
    def join_graphs_by_edge_all_possibilities(g1, g2):
        result = []
        if g1.number_of_nodes() >= g2.number_of_nodes():
            for g1_node in g1.nodes:
                for g2_node in g2.nodes:
                    new_graph = GraphGenerator.join_graphs_by_edge(g1, g2, g1_node, g2_node)
                    if not GraphGenerator.check_isomorphism(new_graph, result):
                        result.append(new_graph)
        else:
            for g2_node in g2.nodes:
                for g1_node in g1.nodes:
                    new_graph = GraphGenerator.join_graphs_by_edge(g2, g1, g2_node, g1_node)
                    if not GraphGenerator.check_isomorphism(new_graph, result):
                        result.append(new_graph)

        return result

if __name__ == '__main__':
    # tree = GraphGenerator.generate_big_almost_asymmetric_tree(50)
    # print(tree.number_of_nodes())
    # start = datetime.datetime.now()
    # print('|Aut(tree)| = ', tree.number_of_automorphisms())
    # print('Duration: ', datetime.datetime.now() - start)
    # if tree.need_to_reevaluate_node_values():
    #     tree.reevaluate_node_values()
    # tree.serialize_to_nauty_format()
    # nautyRunner.run_nauty()


    # GraphGenerator.generate_random_tree(10)
    # g = GraphGenerator.generate_big_asymemtric_tree(20)
    # g = Graph()
    # g.insert_edge(0, 1, 2)
    # g.insert_edge(0, 2, 3)
    # g.insert_edge(0, 2, 4)
    # g.insert_edge(0, 4, 5)
    # g.insert_edge(0, 4, 6)
    # print(g.number_of_automorphisms())
    # print(g.get_wolfram_input())

    # g = GraphGenerator.generate_random_binary_tree(20)
    # g.draw("", True, 'binary_tree.jpg', 2000, 600)

    # g.draw("", True, 'big_tree.jpg', 20000, 20000)
    # =================================================
    # g = Graph()
    # g.insert_edge(0, 0, 3)
    # g.insert_edge(0, 1, 3)
    # g.insert_edge(0, 2, 3)
    # g.insert_edge(0, 3, 4)
    # g.insert_edge(0, 4, 5)
    #
    # print(g.parent_sequence())
    # g.draw('', False, '')

    # =================================================
    # for item in os.listdir(r'./debug'):
    #     if os.path.isdir(r'./debug' + '/' + item):
    #         shutil.rmtree(r'./debug' + '/' + item)
    #     else:
    #         os.remove(r'./debug' + '/' + item)
    #
    # path = GraphGenerator.generate_path(4)
    # star = GraphGenerator.generate_star(4)
    # out = GraphGenerator.generate_non_isomorphic_graphs([path, star])
    # # 5 nodes
    # out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # # 6 nodes
    # out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # # 7 nodes
    # out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # # 8 nodes
    # # out = GraphGenerator.generate_isomorphic_graphs(out)
    # # 9 nodes

    # =================================================
    start = datetime.datetime.now()

    path = GraphGenerator.generate_path(4)
    star = GraphGenerator.generate_star(4)
    out = GraphGenerator.generate_non_isomorphic_graphs([path, star])
    # 5 nodes
    # self.assertEqual(3, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 6 nodes
    # self.assertEqual(6, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 7 nodes
    # self.assertEqual(11, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 8 nodes
    # self.assertEqual(23, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 9 nodes
    # self.assertEqual(47, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 10 nodes
    # self.assertEqual(106, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 11 nodes
    # self.assertEqual(235, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 12 nodes
    # self.assertEqual(551, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 13 nodes
    # self.assertEqual(1301, len(out))
    out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # 14 nodes
    # # self.assertEqual(3159, len(out))
    # # out = GraphGenerator.generate_non_isomorphic_graphs(out)
    # # # 15 nodes
    # # self.assertEqual(7741, len(out))
    print('Duration: ', datetime.datetime.now() - start)
    # print(len(out))

    # =================================================
    # g = GraphGenerator.generate_star(10)
    # print(g.degree__number_of_leaves_as_nth_child_sequence(1))

    # =================================================



