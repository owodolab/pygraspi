import numpy as np
import networkx as nx
import doctest
from .makeGridGraph import make_grid_graph_gt
from graph_tool.all import *
from graph_tool.topology import mark_subgraph
from graph_tool.centrality import betweenness
from graph_tool.stats import remove_labeled_edges


def makeImageGraph_gt(morph):
    """
    Construct a graph for an input image. Each pixel on the input matrix is transformed to a vertex in the graph and the connections with eight neighbors are made with edges are made with edges. Currently supports binary image matrices.

    Args:
        morph (ND array): The microstructure, an `(n_x, n_y, nz)`
            shaped array where `n_x, n_y and n_z` are the spatial dimensions.

    >>> data = np.array([[0,0,0],
    ...                  [1,1,1],
    ...                  [0,0,0]])
    >>> g = makeImageGraph_gt(data)
    """
    G = make_grid_graph_gt(morph.shape)
    interfacev = G.add_vertex()

    vertex_colors = morph.flatten()

    phase = G.new_vertex_property("int")
    for i in range(len(vertex_colors)):
        phase[i] = vertex_colors[i]
    phase[int(interfacev)] = -1
    G.vertex_properties["color"] = phase

    ## Add interface vertex and change edge connections for interface vertices
    G.set_fast_edge_removal(fast=True)
    efilt = G.new_edge_property("int")
    interface = []

    for e in G.edges():
        if phase[e.source()] != phase[e.target()]:
            efilt[e] = 1
            interface.append([int(e.source()), int(e.target())])
        else:
            efilt[e] = 0

    graph_tool.stats.remove_labeled_edges(G, efilt)

    interface = np.unique(np.array(interface)).flatten()
    interface_edges = np.vstack(
        (interface, (np.array([int(interfacev)] * interface.shape[0])))
    ).T

    G.add_edge_list(interface_edges)

    return G


def count_of_vertices_gt(G, phase):
    """Count the number of vertices for a given phase.

    Args:
        G: The network representing the input microstructure.
        phase : The identifier of the phase of interest.

    Test to see if the graph is built with the correct number of
    vertices.

    >>> data = np.array([[0,0,0],
    ...                  [1,1,1],
    ...                  [0,0,0]])
    >>> g = makeImageGraph_gt(data)
    >>> assert(count_of_vertices_gt(g, 0) == 6)
    >>> assert(count_of_vertices_gt(g, 1) == 3)

    """
    phases = np.array(list(G.vertex_properties["color"]))
    return (phases == phase).sum()


def makeConnectedComponents_gt(G, phase):
    """Calculate the number of connected components for a phase of the
       microstructure.

    Args:
      G: The network representing the input microstructure.
      phase : The identifier of the phase of interest.

    A subgraph checking the number of connected components.

    >>> data = np.array([[0,0,0],\
                [1,1,1],\
                [0,0,0]])
    >>> g = makeImageGraph_gt(data)
    >>> assert(makeConnectedComponents_gt(g, 0) == 2)
    >>> assert(makeConnectedComponents_gt(g, 1) == 1)

    """
    interfacev = find_vertex(G, G.vertex_properties["color"], -1)
    phases = np.array(list(G.vertex_properties["color"]))
    if phase == 0:
        phases = 1 - phases
    vfilt = phases
    vfilt[int(interfacev[0])] = 0
    sub = GraphView(G, vfilt)
    return len(set(label_components(sub)[0]))


def interfaceArea_gt(G):
    """
    Calculate the interfacial area of the microstructure.

    Args:
        G: The network representing the input microstructure.

    Check that the interface area is correct

    >>> data = np.array([[0,0,0],\
                [1,1,1],\
                [0,0,0]])
    >>> g = makeImageGraph_gt(data)
    >>> assert(interfaceArea_gt(g) == (9, 6, 3))

    """
    interfacev = find_vertex(G, G.vertex_properties["color"], -1)[0]
    phases = np.array(list(G.vertex_properties["color"]))
    interface_1, interface_0 = 0, 0
    for w in G.iter_out_neighbors(interfacev):
        if phases[w] == 1:
            interface_1 += 1
        else:
            interface_0 += 1
    return interface_1 + interface_0, interface_0, interface_1


def shortest_distance_gt(G):
    """
    Calculate the shortest distances to the meta vertices.

    Args:
        G: The network representing the input microstructure.
       phase : The identifier of the phase of interest.

    Not a good test case.

    >>> data = np.array([[0,0,0],\
                [1,1,1],\
                [0,0,0]])
    >>> g = makeImageGraph_gt(data)
    >>> assert(shortest_distance_gt(g) == (1.0, 1.0, 1.0))

    """
    interfacev = find_vertex(G, G.vertex_properties["color"], -1)[0]
    phases = np.array(list(G.vertex_properties["color"]))

    d = shortest_distance(G, interfacev)
    dist_to_interface = sum(list(d)) / (len(list(d)) - 1)

    vfilt = phases
    sub_1 = GraphView(G, vfilt)

    d = shortest_distance(sub_1, interfacev)
    dist_to_interface_1 = sum(list(d)) / (len(list(d)) - 1)

    phases = 1 - phases
    vfilt_0 = phases
    # vfilt_0[int(interfacev)] = 0
    sub_0 = GraphView(G, vfilt_0)

    d = shortest_distance(sub_0, interfacev)
    dist_to_interface_0 = sum(list(d)) / (len(list(d)) - 1)

    return dist_to_interface, dist_to_interface_0, dist_to_interface_1


def tortuosity(G, phase):
    return None


def interface_boundary(G, phase):
    return None


def getGraspiDescriptors(data):
    """
    Calculate the graph descriptors for a segmented microstructure image.

    Args:
        data (ND array): The microstructure, an `(n_x, n_y, nz)`
            shaped array where `n_x, n_y and n_z` are the spatial dimensions.

    Example
    """
    g = makeImageGraph_gt(data)
    [interface_area, phase_0_interface, phase_1_interface] = interfaceArea_gt(g)
    [
        distance_to_interface,
        distance_to_interface_0,
        distance_to_interface_1,
    ] = shortest_distance_gt(g)
    return dict(
        phase_0_count=count_of_vertices_gt(g, 0),
        phase_1_count=count_of_vertices_gt(g, 1),
        phase_0_cc=makeConnectedComponents_gt(g, 0),
        phase_1_cc=makeConnectedComponents_gt(g, 1),
        interfacial_area=interface_area,
        phase_0_interface=phase_0_interface,
        phase_1_interface=phase_1_interface,
        distance_to_interface=distance_to_interface,
        distance_to_interface_0=distance_to_interface_0,
        distance_to_interface_1=distance_to_interface_1,
    )
