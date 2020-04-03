from graph_generator import *
import os, shutil, csv, datetime
import nautyRunner

FOLDER = r'./results_joining_by_node_linux'
FULL_CSV_PATH = FOLDER + '/results.csv'
CREATE_IMAGES = True

class UseCase():

    @staticmethod
    def join_2_simple_graphs1():
        g1 = GraphGenerator.generate_path(4)
        g2 = GraphGenerator.generate_path(3)
        result = GraphGenerator.join_graphs_by_node_all_possibilities(g1, g2)
        for g in result:
            g.draw()

    @staticmethod
    def join_2_simple_graphs2():
        g1 = GraphGenerator.generate_star(4)
        g2 = GraphGenerator.generate_path(3)

        result = GraphGenerator.join_graphs_by_node_all_possibilities(g1, g2)
        for g in result:
            g.draw()

    @staticmethod
    def join_2_simple_graphs3():
        g1 = GraphGenerator.generate_star(4)
        g2 = GraphGenerator.generate_path(5)
        g1.draw('first')
        g2.draw('second')
        result = GraphGenerator.join_graphs_by_node_all_possibilities(g1, g2)
        for g in result:
            g.draw()

        return result

    @staticmethod
    def join_2_big_asymmetric_trees(n):
        g1 = GraphGenerator.generate_big_asymemtric_tree(n)
        g2 = GraphGenerator.generate_big_asymemtric_tree(n)
        print('|Aut(g1)| = ', g1.number_of_automorphisms())
        print('|Aut(g2)| = ', g2.number_of_automorphisms())
        node1 = g1.find_node(0)
        node2 = g2.find_node(0)
        g = GraphGenerator.join_graphs_by_node(g1, g2, node1, node2)
        print('|Aut(G)| = ', g.number_of_automorphisms())
        print('|V(G)| = ', g.number_of_nodes())

    @staticmethod
    def join_big_small_graph_version_path(n1, n2):
        big = GraphGenerator.generate_big_asymemtric_tree(n1)
        small = GraphGenerator.generate_path(n2)
        UseCase.join_2_trees(big, small)

    @staticmethod
    def join_big_small_graph_version_star(n1, n2):
        big = GraphGenerator.generate_big_asymemtric_tree(n1)
        small = GraphGenerator.generate_star(n2)
        UseCase.join_2_trees(big, small)

    @staticmethod
    def join_big_small_graph_version_random_binary_tree_and_star(n1, n2):
        big = GraphGenerator.generate_random_binary_tree(n1)
        small = GraphGenerator.generate_star(n2)
        UseCase.join_2_trees(big, small)

    @staticmethod
    def join_big_small_graph_version_random_binary_tree_and_path(n1, n2):
        big = GraphGenerator.generate_random_binary_tree(n1)
        small = GraphGenerator.generate_path(n2)
        UseCase.join_2_trees(big, small)

    @staticmethod
    def join_2_random_binary_trees(n1, n2):
        big = GraphGenerator.generate_random_binary_tree(n1)
        small = GraphGenerator.generate_random_binary_tree(n2)
        UseCase.join_2_trees(big, small)

    @staticmethod
    def join_2_random_trees(n1, n2):
        big = GraphGenerator.generate_random_tree(n1)
        small = GraphGenerator.generate_random_tree(n2)
        UseCase.join_2_trees(big, small)

    @staticmethod
    def join_2_trees(tree1, tree2):
        '''
        Function for joining 2 trees. tree1 is usually bigger (or should be) than tree2.
        This function also print |Aut| for input trees and for result tree after joining two input trees.
        '''
        small_node = tree2.find_node(0)
        print('|V| = ', tree1.number_of_nodes())
        print('|Aut(big)| = ', tree1.number_of_automorphisms())
        print('|Aut(small)| = ', tree2.number_of_automorphisms())
        for node in tree1.nodes:
            g = GraphGenerator.join_graphs_by_node(tree1, tree2, node, small_node)
            print('|Aut(result)| = ', g.number_of_automorphisms())

    @staticmethod
    def test_generating_sets():
        tree1 = GraphGenerator.generate_path(5)
        tree2 = GraphGenerator.generate_star(6)
        tree1.serialize_to_nauty_format()
        result1 = nautyRunner.nauty_get_aut_group()
        tree2.serialize_to_nauty_format()
        result2 = nautyRunner.nauty_get_aut_group()
        print("Path aut group: \n", result1)
        print("Star aut group: \n", result2)
        joined = GraphGenerator.join_graphs_by_node(tree1, tree2, tree1.nodes[0], tree2.nodes[0])
        joined.serialize_to_nauty_format()
        result_joined = nautyRunner.nauty_get_aut_group()
        print("Joined tree aut group: \n", result_joined)

    @staticmethod
    def generate_graphs_iteratively_by_joining(n, by_node=True):

        def folder_exists(name):
            for item in os.listdir(FOLDER):
                if name in item:
                    return True
            return False

        def get_max_folder_iteration(name):
            # example: 2_3_iteration_2 means in this folder are stored pictures of results of joining graphs with 2 and 3 nodes, iteration 2
            if not folder_exists(name):
                return 0
            max_value = 1
            for item in os.listdir(FOLDER):
                if name in item:
                    if max_value < int(item.split('_')[3]):
                        max_value = int(item.split('_')[3])
            return max_value

        if not os.path.exists(FOLDER):
            os.mkdir(FOLDER)
        for item in os.listdir(FOLDER):
            if os.path.isdir(FOLDER + '/' + item):
                shutil.rmtree(FOLDER + '/' + item)
            else:
                os.remove(FOLDER + '/' + item)

        if n < 2:
            return

        out = GraphGenerator.generate_path(2)
        all_graphs = [out]
        # generate all non isomorphic graphs with maximum n vertices
        for i in range(n-2):
            if not isinstance(out, list):
                out = GraphGenerator.generate_non_isomorphic_graphs([out])
            else:
                out = GraphGenerator.generate_non_isomorphic_graphs(out)
            all_graphs.extend(out)

        with open(FULL_CSV_PATH, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            for i in range(len(all_graphs)):
                for j in range(i, len(all_graphs)):
                    if CREATE_IMAGES:
                        if all_graphs[i].number_of_nodes() < all_graphs[j].number_of_nodes():
                            max_iteration = get_max_folder_iteration(str(all_graphs[i].number_of_nodes()) + '_' + str(all_graphs[j].number_of_nodes()))
                            # print('max iteration: ', max_iteration)
                            new_folder = FOLDER + r'/' + str(all_graphs[i].number_of_nodes()) + '_' + \
                                         str(all_graphs[j].number_of_nodes()) + '_iteration_' + str(max_iteration + 1)
                            os.mkdir(new_folder)
                        else:
                            max_iteration = get_max_folder_iteration(str(all_graphs[j].number_of_nodes()) + '_' + str(all_graphs[i].number_of_nodes()))
                            new_folder = FOLDER + r'/' + str(all_graphs[j].number_of_nodes()) + '_' + \
                                         str(all_graphs[i].number_of_nodes()) + '_iteration_' + str(max_iteration + 1)
                            os.mkdir(new_folder)

                    if by_node:
                        result = GraphGenerator.join_graphs_by_node_all_possibilities(all_graphs[i], all_graphs[j])
                    else:
                        result = GraphGenerator.join_graphs_by_edge_all_possibilities(all_graphs[i], all_graphs[j])

                    if CREATE_IMAGES:
                        if sys.platform == 'windows':
                            all_graphs[i].draw('First graph to be joined', True, new_folder + '/first.jpg')
                            all_graphs[j].draw('Second graph to be joined', True, new_folder + '/second.jpg')
                        elif sys.platform == 'linux':
                            all_graphs[i].serialize_to_nauty_format()
                            nautyRunner.nauty_dre_to_dot(new_folder + '/first.dot')
                            all_graphs[j].serialize_to_nauty_format()
                            nautyRunner.nauty_dre_to_dot(new_folder + '/second.dot')

                    if CREATE_IMAGES:
                        csv_writer.writerow(['', '', '', '', '', '', '', '', '', '', '', ''])
                        csv_writer.writerow(['|T1|', '|T2|', '|Joined|', '|Aut(T1)|', '|Aut(T2)|', '|Aut(Joined)|',
                                             'Aut(T1)', 'Aut(T2)', 'Aut(Joined)', 'T1 path', 'T2 path', 'Joined path'])
                    else:
                        csv_writer.writerow(['', '', '', '', '', '', '', '', ''])
                        csv_writer.writerow(['|T1|', '|T2|', '|Joined|', '|Aut(T1)|', '|Aut(T2)|', '|Aut(Joined)|',
                                             'Aut(T1)', 'Aut(T2)', 'Aut(Joined)'])

                    image_file_count = 0
                    for g in result:
                        if CREATE_IMAGES:
                            if sys.platform == 'windows':
                                g.draw('Result from joining 2 graphs', True, new_folder + '/' + str(image_file_count) + '.jpg')
                            elif sys.platform == 'linux':
                                g.serialize_to_nauty_format()
                                nautyRunner.nauty_dre_to_dot(new_folder + '/' + str(image_file_count) + '.dot')

                        g.serialize_to_nauty_format()
                        joined_aut_size, joined_aut = nautyRunner.nauty_get_automorphism_group_info()
                        joined_aut = ','.join(joined_aut.split('\n'))

                        if CREATE_IMAGES:
                            joined_path = new_folder + '/' + str(image_file_count) + '.dot'

                        if image_file_count == 0:
                            # csv_writer.writerow(
                            #     [str(all_graphs[i].number_of_automorphisms()) + '(' + str(all_graphs[i].number_of_nodes()) + ')',
                            #      str(all_graphs[j].number_of_automorphisms()) + '(' + str(all_graphs[j].number_of_nodes()) + ')',
                            #      str(g.number_of_automorphisms()) + '(' + str(g.number_of_nodes()) + ')'])

                            t1_size = str(all_graphs[i].number_of_nodes())
                            t2_size = str(all_graphs[j].number_of_nodes())
                            joined_size = str(g.number_of_nodes())

                            all_graphs[i].serialize_to_nauty_format()
                            t1_aut_size, t1_aut = nautyRunner.nauty_get_automorphism_group_info()
                            t1_aut = ','.join(t1_aut.split('\n'))
                            all_graphs[j].serialize_to_nauty_format()
                            t2_aut_size, t2_aut = nautyRunner.nauty_get_automorphism_group_info()
                            t2_aut = ','.join(t2_aut.split('\n'))

                            if CREATE_IMAGES:
                                t1_path = new_folder + '/first.dot'
                                t2_path = new_folder + '/second.dot'

                                csv_writer.writerow([t1_size, t2_size, joined_size,
                                                     str(t1_aut_size), str(t2_aut_size), str(joined_aut_size),
                                                     t1_aut, t2_aut, joined_aut,
                                                     t1_path, t2_path, joined_path])
                            else:
                                csv_writer.writerow([t1_size, t2_size, joined_size,
                                                     str(t1_aut_size), str(t2_aut_size), str(joined_aut_size),
                                                     t1_aut, t2_aut, joined_aut])

                        else:
                            # csv_writer.writerow([' ', ' ', str(g.number_of_automorphisms()) + '(' + str(g.number_of_nodes()) + ')'])
                            if CREATE_IMAGES:
                                csv_writer.writerow(['', '', '',
                                                     '', '', str(joined_aut_size),
                                                     '', '', joined_aut,
                                                     '', '', joined_path])
                            else:
                                csv_writer.writerow(['', '', '',
                                                     '', '', str(joined_aut_size),
                                                     '', '', joined_aut])

                        image_file_count += 1


if __name__ == '__main__':
    start = datetime.datetime.now()
    # UseCase.join_2_random_trees(100, 100)
    UseCase.generate_graphs_iteratively_by_joining(5)
    print('Duration: ', datetime.datetime.now() - start)
    # result = UseCase.join_2_simple_graphs2()
