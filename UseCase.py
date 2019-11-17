from graph_generator import *

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
        if n < 2: return
        out = GraphGenerator.generate_path(2)
        all_graphs = [out]
        # generate all non isomorphic graphs with maximum n vertices
        for i in range(n-2):
            if out != list:
                out = GraphGenerator.generate_isomorphic_graphs([out])
            else:
                out = GraphGenerator.generate_isomorphic_graphs(out)
            all_graphs.extend(out)

        for i in range(len(all_graphs)):
            for j in range(i, len(all_graphs)):
                result = GraphGenerator.join_graphs_by_node_all_possibilities(all_graphs[i], all_graphs[j])
                all_graphs[i].draw('Firt graph to be joined')
                all_graphs[j].draw('Second graph to be joined')
                for g in result:
                    g.draw('Result from joining 2 graphs')


if __name__ == '__main__':
    # UseCase.generate_graphs_iteratively_by_joining(3)
    result = UseCase.join_2_simple_graphs2()
