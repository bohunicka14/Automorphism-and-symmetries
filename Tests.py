import unittest
import math
import UseCase
from UseCase import *
from graph_generator import *

class TestInsertingEdges(unittest.TestCase):

    def test(self):
        g = Graph()
        g.insert_edge(0, 0, 1)
        self.assertFalse(g.insert_edge(0, 0, 1))

class TestAutomorphisms(unittest.TestCase):

    def test_symmetric_tree(self):
        g = Graph()
        g.insert_edge(0, 0, 1)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 3, 4)
        g.insert_edge(0, 4, 5)
        g.insert_edge(0, 4, 6)
        self.assertEqual(8, g.number_of_automorphisms())

    def test_another_symmetric_tree(self):
        g = Graph()
        g.insert_edge(0, 0, 1)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 2, 3)
        g.insert_edge(0, 2, 4)
        g.insert_edge(0, 4, 5)
        self.assertEqual(2, g.number_of_automorphisms())

    def test_symmetric_star(self):
        g = GraphGenerator.generate_star(5)
        self.assertEqual(math.factorial(4), g.number_of_automorphisms())

    def test_symmetric_path(self):
        g = GraphGenerator.generate_path(10)
        self.assertEqual(2, g.number_of_automorphisms())

    def test_assymetric_tree(self):
        g = Graph()
        g.insert_edge(0, 0, 1)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 2, 3)
        g.insert_edge(0, 3, 4)
        g.insert_edge(0, 3, 5)
        g.insert_edge(0, 5, 6)
        self.assertEqual(1, g.number_of_automorphisms())

    def test_symmetric_tree2(self):
        g = Graph()
        g.insert_edge(0, 0, 1)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 3, 4)
        g.insert_edge(0, 3, 5)
        self.assertEqual(8, g.number_of_automorphisms())

        g = Graph()
        g.insert_edge(0, 0, 1)
        g.insert_edge(0, 1, 2)
        g.insert_edge(0, 1, 3)
        g.insert_edge(0, 3, 4)
        g.insert_edge(0, 4, 5)
        g.insert_edge(0, 5, 6)
        g.insert_edge(0, 6, 7)
        g.insert_edge(0, 6, 8)

        self.assertEqual(8, g.number_of_automorphisms())


class TestTreeIsomorphisms(unittest.TestCase):

    def test_parent_sequence(self):
        path = GraphGenerator.generate_path(2)
        self.assertEqual([1, 1], path.parent_sequence())
        star = GraphGenerator.generate_star(5)
        self.assertEqual([4], star.parent_sequence())

    def test_tree_with_2_nodes(self):
        path = GraphGenerator.generate_path(2)
        out = GraphGenerator.generate_non_isomorphic_graphs([path])
        self.assertEqual(1, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        self.assertEqual(2, len(out))

    def test_tree_with_n_nodes(self):
        path = GraphGenerator.generate_path(4)
        star = GraphGenerator.generate_star(4)
        out = GraphGenerator.generate_non_isomorphic_graphs([path, star])
        # 5 nodes
        self.assertEqual(3, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 6 nodes
        self.assertEqual(6, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 7 nodes
        self.assertEqual(11, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 8 nodes
        self.assertEqual(23, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 9 nodes
        self.assertEqual(47, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 10 nodes
        self.assertEqual(106, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 11 nodes
        self.assertEqual(235, len(out))
        out = GraphGenerator.generate_non_isomorphic_graphs(out)
        # 12 nodes
        self.assertEqual(551, len(out))
        # out = GraphGenerator.generate_isomorphic_graphs(out)
        # # 13 nodes
        # self.assertEqual(1301, len(out))
        # out = GraphGenerator.generate_isomorphic_graphs(out)
        # # 14 nodes
        # self.assertEqual(3159, len(out))
        # out = GraphGenerator.generate_isomorphic_graphs(out)
        # # 15 nodes
        # self.assertEqual(7741, len(out))


class TestTreeJoining(unittest.TestCase):

    def test_trivial_tree_join(self):
        g1 = GraphGenerator.generate_trivial_graph()
        g2 = GraphGenerator.generate_trivial_graph()
        result = GraphGenerator.join_graphs_by_node(g1, g2, g1.nodes[0], g2.nodes[0])
        self.assertEqual(g1.number_of_nodes(), result.number_of_nodes())
        self.assertEqual(g2.number_of_nodes(), result.number_of_nodes())
        self.assertEqual(g1.number_of_edges() + g2.number_of_edges(), result.number_of_edges())
        self.assertEqual(1, result.number_of_automorphisms())

        result = GraphGenerator.join_graphs_by_edge(g1, g2, g1.nodes[0], g2.nodes[0])
        self.assertEqual(g1.number_of_nodes() + g2.number_of_nodes(), result.number_of_nodes())
        self.assertEqual(g1.number_of_edges() + g2.number_of_edges() + 1, result.number_of_edges())
        self.assertEqual(2, result.number_of_automorphisms())

if __name__ == '__main__':
    unittest.main()


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

    # path = GraphGenerator.generate_path(4)
    # star = GraphGenerator.generate_star(4)
    # out = GraphGenerator.generate_isomorphic_graphs([path, star])
    # # # for g in out:
    # # #     print(g.leaf_sequence())
    # # print(len(out))
    # # print('5 vrcholove:')
    # # for g in out:
    # #     print(g)
    # out = GraphGenerator.generate_isomorphic_graphs(out)
    #
    # # print('6 vrcholove')
    # # for g in out:
    # #     print(g)
    # # print(len(out))
    # #
    # out = GraphGenerator.generate_isomorphic_graphs(out)
    #
    # for i in range(5):
    #     out = GraphGenerator.generate_isomorphic_graphs(out)
    #     print(len(out))
    #
    # for g in out:
    #     g.draw()
    # #
    # # out = GraphGenerator.generate_isomorphic_graphs(out)
    # # print(len(out))