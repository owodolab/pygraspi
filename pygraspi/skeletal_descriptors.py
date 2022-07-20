"""Computes the skeleton of the microstructures and subsequently
calculates skeleton-based descriptors.
"""

import numpy as np
import networkx as nx
from skimage.morphology import medial_axis, skeletonize
import sknw


def skeletonize(data):
    """Generates the skeleton for a microstructure
    Args:
      data: a single microstructure of any dimension with only two
        phases
    Returns:
      the skeletonized microstructure (a Boolean array) where True is
      the skeleton
    Test case
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> assert np.allclose(
    ...     skeleton,
    ...     [[False, False,  True], [False, False,  True], [True,  True, False]]
    ... )
    """
    return medial_axis(data, return_distance=True)


def f_skeletal_pixels(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> assert(round(f_skeletal_pixels(skeleton),2) == 0.44)
    """
    count = np.count_nonzero(skeleton)
    return count / skeleton.size


def getSkeletalGraph(skeleton):
    graph = sknw.build_sknw(skeleton)
    return graph


def getEndJunction(graph):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> graph = getSkeletalGraph(skeleton)
    >>> assert np.allclose(getEndJunction(graph), [2, 0])
    """
    l = [graph.degree[n] for n in graph.nodes()]
    return np.array([l.count(1), l.count(3)])


def getBranchLen(graph):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> graph = getSkeletalGraph(skeleton)
    >>> assert np.allclose(getBranchLen(graph), [1.00, 3.41])
    """
    b_l = [graph.edges[e]["weight"] for e in graph.edges()]
    return np.array([len(b_l), round(sum(b_l) / len(b_l), 2)])


def number_of_cycles(graph):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> graph = getSkeletalGraph(skeleton)
    >>> assert np.allclose(number_of_cycles(graph), [0, 0])
    """
    cycles = 0
    for cc in sorted(nx.connected_components(graph), key=len, reverse=True):
        if len(cc) > 2:
            sgraph = graph.subgraph(cc)
            cycles += max((sgraph.number_of_edges() - sgraph.number_of_nodes()) + 1, 0)
    return cycles


def getSkeletalDescriptors(data):

    [skeleton_a, distance_map_a] = skeletonize(data)
    [skeleton_b, distance_map_b] = skeletonize(1 - data)

    graph_a = getSkeletalGraph(skeleton_a)
    graph_b = getSkeletalGraph(skeleton_b)

    [e_a, j_a] = getEndJunction(graph_a)
    [bn_a, bl_a] = getBranchLen(graph_a)
    [e_b, j_b] = getEndJunction(graph_b)
    [bn_b, bl_b] = getBranchLen(graph_b)

    dist_on_skel_a = distance_map_a * skeleton_a
    d_a = dist_on_skel_a[skeleton_a]
    dist_on_skel_b = distance_map_b * skeleton_b
    d_b = dist_on_skel_b[skeleton_b]

    return dict(
        f_skeletal_pixels_a=f_skeletal_pixels(skeleton_a),
        f_skeletal_pixels_b=f_skeletal_pixels(skeleton_b),
        number_of_ends_a=e_a,
        number_of_ends_b=e_b,
        number_of_intersections_a=j_a,
        number_of_intersections_b=j_b,
        number_of_branches_a=bn_a,
        number_of_branches_b=bn_b,
        branch_length_a=bl_a,
        branch_length_b=bl_b,
        dist_to_interface_min_a=min(d_a),
        dist_to_interface_min_b=min(d_b),
        dist_to_interface_max_a=max(d_a),
        dist_to_interface_max_b=max(d_b),
        dist_to_interface_avg_a=round(sum(d_a) / len(d_a), 2),
        dist_to_interface_avg_b=round(sum(d_b) / len(d_b), 2),
        number_of_cycles_a=number_of_cycles(graph_a),
        number_of_cycles_b=number_of_cycles(graph_b),
    )
