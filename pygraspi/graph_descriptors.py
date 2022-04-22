import numpy as np
import networkx as nx
import doctest
from makeGridGraph import make_grid_graph


def makeImageGraph(morph):
    G = make_grid_graph(morph.shape)
    vertex_colors = morph.flatten()
    mapping = {(i): vertex_colors[i] for i in range(len(vertex_colors))}
    nx.set_node_attributes(G, mapping, name="color")
    return G


def count_of_vertices(G, phase):
    phases = nx.get_node_attributes(G, "color")
    phase_list = list(phases.values())
    return phase_list.count(phase)


def node_phaseA(n, G):
    nodes = G.nodes
    return nodes[n]["color"] == 0


def node_phaseB(n, G):
    nodes = G.nodes
    return nodes[n]["color"] == 1


def makeInterfaceEdges(G):
    interface = [
        (n, u)
        for n, u in G.edges()
        if (node_phaseA(n, G) and node_phaseB(u, G))
        or (node_phaseB(n, G) and node_phaseA(u, G))
    ]
    G.remove_edges_from(interface)
    G.add_node(-1, color="green")
    interface = np.unique(np.array(interface))
    interface_edges = [(x, -1) for x in interface]
    G.add_edges_from(interface_edges)
    return G


def makeConnectedComponents(G, phase):
    nodes = (node for node, data in G.nodes(data=True) if data.get("color") == phase)
    subgraph = G.subgraph(nodes)
    subgraph.nodes
    return nx.number_connected_components(subgraph)


def interfaceArea(G):
    # for neighbor in G.neighbors(x):
    # print(G.nodes[neighbor]["time"])
    nodes_0 = [
        neighbor for neighbor in G.neighbors(-1) if G.nodes[neighbor]["color"] == 0
    ]
    nodes_1 = [
        neighbor for neighbor in G.neighbors(-1) if G.nodes[neighbor]["color"] == 1
    ]
    return G.degree[-1], len(nodes_0), len(nodes_1)


def shortest_distances(G):
    path = nx.single_source_shortest_path(G, -1)
    del path[-1]
    path_length = [len(p) for p in path.values()]
    # print(path_length)
    return sum(path_length) / len(path_length)


def getGraspiDescriptors(data):
    # phase 1
    g = makeImageGraph(data)
    g = makeInterfaceEdges(g)
    [interface_area, phase_0_interface, phase_1_interface] = interfaceArea(g)

    return dict(
        phase_0_count=count_of_vertices(g, 0),
        phase_1_count=count_of_vertices(g, 1),
        phase_0_cc=makeConnectedComponents(g, 0),
        phase_1_cc=makeConnectedComponents(g, 1),
        interfacial_area=interface_area,
        phase_0_interface=phase_0_interface,
        phase_1_interface=phase_1_interface,
        distance_to_interface=shortest_distances(g),
    )
