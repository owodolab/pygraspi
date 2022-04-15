import numpy as np
import networkx as nx
import doctest
from .makeGridGraph import make_grid_graph


def graphConstruction(morph):
    m, n = morph.shape
    G = nx.grid_2d_graph(m, n, periodic=False, create_using=None)
    return G


def numberofEdges(G):
    """
    >>> data = np.array([[0,1,0],\
                [0,1,0],\
                [0,1,0]])
    >>> G = graphConstruction(data)
    >>> assert(numberofEdges(G) == 12)
    """
    return G.number_of_edges()


def numberofVertices(G):
    """
    >>> data = np.array([[0,1,0],\
                [0,1,0],\
                [0,1,0]])
    >>> G = graphConstruction(data)
    >>> assert(numberofVertices(G) == 9)
    """
    return G.number_of_nodes()


def setPhaseAttributes(G, morph):
    mapping = {
        (i, j): morph[i][j]
        for i in range(0, morph.shape[0])
        for j in range(0, morph.shape[1])
    }
    nx.set_node_attributes(G, mapping, name="color")

    return G


def numberofPhaseVertices(G, phase):
    """
    >>> data = np.array([[0, 1], [0, 1]])
    >>> G = graphConstruction(data)
    >>> G = add_phaseAttributes(G, data)
    >>> assert(numberofPhaseVertices(G, 0) == 2)
    """
    phases = nx.get_node_attributes(G, "color")
    phase_list = list(phases.values())
    return phase_list.count(phase)


def add_phaseAttributes(G, morph):
    mapping = {
        (i, j): morph[i][j]
        for i in range(0, morph.shape[0])
        for j in range(0, morph.shape[1])
    }
    nx.set_node_attributes(G, mapping, name="color")
    return G


def node_phaseA(n, G):
    nodes = G.nodes
    return nodes[n]["color"] == 0


def node_phaseB(n, G):
    nodes = G.nodes
    return nodes[n]["color"] == 1


def makeInterfaceEdges(G):
    """
    >>> data = np.array([[0, 1], [0, 1]])
    >>> G = graphConstruction(data)
    >>> G = add_phaseAttributes(G, data)
    >>> G.add_edge((0,0), (1, 1))
    >>> G.add_edge((0,1), (1, 0))
    >>> assert(len(makeInterfaceEdges(G)) == 4)
    """
    interface = [
        (n, u)
        for n, u in G.edges()
        if (node_phaseA(n, G) and node_phaseB(u, G))
        or (node_phaseB(n, G) and node_phaseA(u, G))
    ]
    return interface


def makeConnectedComponents(G, phase)
    """
    >>> data = np.array([[0, 1], [0, 1]])
    >>> G = graphConstruction(data)
    >>> G = add_phaseAttributes(G, data)
    >>> G.add_edge((0,0), (1, 1))
    >>> G.add_edge((0,1), (1, 0))
    >>> assert(makeConnectedComponents(G, 0) == 1)
    """
    nodes = (node for node, data in G.nodes(data=True) if data.get("color") == phase)
    subgraph = G.subgraph(nodes)
    subgraph.nodes
    return nx.number_connected_components(subgraph)


def graph_example(nx, ny, nz):
    """
    >>> g = graph_example(3, 3, 2)
    >>> assert(g.number_of_edges() == 89)
    """
    return make_grid_graph((nx, ny, nz))
