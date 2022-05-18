import numpy as np
import doctest
from skimage.morphology import medial_axis, skeletonize
import sknw


def neighborhood(nx, ny):
    vertex_list = np.array(range(nx * ny))
    # neighborhood = np.zeros([vertex_list.shape[0], 8])

    return neighborhood


def skeletonize(morph):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> assert np.allclose(skeleton, [[False, False,  True], [False, False,  True], [True,  True, False]])
    """
    skel, distance = medial_axis(morph, return_distance=True)
    return skel, distance


def skeletal_len(skeleton):
    return np.count_nonzero(skeleton)


def f_skeletal_pixels(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> assert(f_skeletal_pixels(skeleton) == 0.44)
    """
    count = np.count_nonzero(skeleton)
    return round(count / skeleton.size, 2)


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
    return None


def getSkeletalDescriptors(data):
    # phase 1
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
    )
