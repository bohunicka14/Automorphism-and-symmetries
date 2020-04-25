from graph import *
from graph_generator import *
import matplotlib.pyplot as plt

def run():
    x = []
    y = []
    loop = [10, 50, 100]
    loop.extend(list(range(200, 1001, 100)))
    for i in loop:
        g = GraphGenerator.generate_random_tree(i)
        start = datetime.datetime.now()
        size = g.number_of_automorphisms()
        duration_secs = (datetime.datetime.now() - start).total_seconds()
        print(size, duration_secs, 'seconds')
        x.append(i)
        y.append(duration_secs)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('tree size')
    ax.set_ylabel('time [s]')
    # plt.scatter(x, y)
    plt.show()



if __name__ == '__main__':
    run()