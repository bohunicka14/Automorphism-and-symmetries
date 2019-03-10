
class Node(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def is_leaf(self):
        return len(self.children) == 1


class Graph():
    def __init__(self):
        self.g = dict()

    def add_edge(self, v1, v2):
        if self.g.get(v1, None) is not None:
            self.g[v1].add(v2)
        else:
            self.g[v1] = {v2}

        if self.g.get(v2, None) is not None:
            self.g[v2].add(v1)
        else:
            self.g[v2] = {v1}

    def is_leaf(self, vertex, graph):
        if graph.get(vertex, None) is not None:
            return len(graph.get(vertex)) == 1
        else:
            return None

    def del_leaf(self, vertex, graph):
        if self.is_leaf(vertex, graph):
            adjacent = next(iter(graph.get(vertex)))
            del graph[vertex]
            graph[adjacent].remove(vertex)
            return adjacent
        return None

    def prufer_code(self):
        copy = dict(self.g)
        result = ''
        while len(copy) > 2:
            sorted_vertices = sorted(list(copy.keys()))
            for vertex in sorted_vertices:
                if self.is_leaf(vertex, copy):
                    result += str(self.del_leaf(vertex, copy))
                    break

        return result


if __name__ == '__main__':
    g = Graph()
    g.add_edge(1, 4)
    g.add_edge(2, 4)
    g.add_edge(3, 4)
    g.add_edge(5, 4)
    g.add_edge(5, 6)

    print(g.prufer_code())





