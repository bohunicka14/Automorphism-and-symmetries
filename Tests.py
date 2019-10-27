import unittest
import math
from graph_generator import *


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