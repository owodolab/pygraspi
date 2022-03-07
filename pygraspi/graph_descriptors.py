import numpy as np
import networkx as nx
import doctest

def getNeighborhood1D(dim_x, dim_y):
    vertex_list = np.array(range(dim_x * dim_y))
    #neighborhood = np.zeros([vertex_list.shape[0], 8])

    neighborhood = np.array([[p-dim_x, (p-dim_x) + 1, p + 1, p + dim_x + 1, p + dim_x,
                             (p+dim_x) - 1, p - 1, (p - dim_x) - 1 ] for p in vertex_list])
    neighborhood[::dim_x, [5, 6, 7]] = -1
    neighborhood[dim_x-1::dim_x, [1, 2, 3]] = -1
    neighborhood[0, [0, 1, 5, 6, 7]] = -1
    neighborhood[dim_x-1, [0, 1, 2, 3, 7]] = -1
    neighborhood[dim_x * (dim_y -1), [3, 4, 5, 6, 7]] = -1
    neighborhood[-1, [1, 2, 3, 4, 5]] = -1
    neighborhood[0:dim_x, [0, 1, 7]] = -1
    neighborhood[dim_x * (dim_y -1):, [3, 4, 5]] = -1

    return neighborhood

def graphConstruction(morph):

    dim_x, dim_y = morph.shape
    vertex_list = range(dim_x*dim_y)
    G = nx.Graph()
    #vertex_colors = input_morph.flatten()
    G.add_nodes_from(vertex_list)

    neighborhood = getNeighborhood1D(dim_x, dim_y)
    edge_list = []
    for i in (vertex_list):
        for n in neighborhood[i, :]:
            if n == -1: continue
            e = sorted([i, n])
            if e not in edge_list:
                edge_list.append(e)

    G.add_edges_from(edge_list)

    return G


def numberofEdges(G):
    """
    >>> data = np.array([[0,1,0],\
                [0,1,0],\
                [0,1,0]])
    >>> G = graphConstruction(data)
    >>> assert(numberofEdges(G) == 20)
    """
    return G.number_of_edges()

def numberofNodes(G):
    """
    >>> data = np.array([[0,1,0],\
                [0,1,0],\
                [0,1,0]])
    >>> G = graphConstruction(data)
    >>> assert(numberofNodes(G) == 9)
    """
    return G.number_of_nodes()

doctest.testmod()
