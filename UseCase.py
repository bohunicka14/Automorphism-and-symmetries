from graph_generator import *
import os, shutil

FOLDER = r'./results'

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
    def generate_graphs_iteratively_by_joining(n):

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
            shutil.rmtree(FOLDER + '/' + item)

        if n < 2:
            return

        out = GraphGenerator.generate_path(2)
        all_graphs = [out]
        # generate all non isomorphic graphs with maximum n vertices
        for i in range(n-2):
            if not isinstance(out, list):
                out = GraphGenerator.generate_isomorphic_graphs([out])
            else:
                out = GraphGenerator.generate_isomorphic_graphs(out)
            all_graphs.extend(out)

        for i in range(len(all_graphs)):
            for j in range(i, len(all_graphs)):
                if all_graphs[i].number_of_nodes() < all_graphs[j].number_of_nodes():
                    max_iteration = get_max_folder_iteration(str(all_graphs[i].number_of_nodes()) + '_' + str(all_graphs[j].number_of_nodes()))
                    print('max iteration: ', max_iteration)
                    new_folder = FOLDER + r'/' + str(all_graphs[i].number_of_nodes()) + '_' + \
                                 str(all_graphs[j].number_of_nodes()) + '_iteration_' + str(max_iteration + 1)
                    os.mkdir(new_folder)
                else:
                    max_iteration = get_max_folder_iteration(str(all_graphs[j].number_of_nodes()) + '_' + str(all_graphs[i].number_of_nodes()))
                    new_folder = FOLDER + r'/' + str(all_graphs[j].number_of_nodes()) + '_' + \
                                 str(all_graphs[i].number_of_nodes()) + '_iteration_' + str(max_iteration + 1)
                    os.mkdir(new_folder)

                result = GraphGenerator.join_graphs_by_node_all_possibilities(all_graphs[i], all_graphs[j])
                all_graphs[i].draw('First graph to be joined', True, new_folder + '/first.jpg')
                all_graphs[j].draw('Second graph to be joined', True, new_folder + '/second.jpg')
                image_file_count = 0
                for g in result:
                    g.draw('Result from joining 2 graphs', True, new_folder + '/' + str(image_file_count) + '.jpg')
                    image_file_count += 1


if __name__ == '__main__':
    UseCase.generate_graphs_iteratively_by_joining(6)
    # result = UseCase.join_2_simple_graphs2()
