import numpy as np
import doctest
from skimage.morphology import medial_axis, skeletonize

# from skan import Skeleton, summarize
import sknw

import pytest

pytest.skip(allow_module_level=True)


def neighborhood(nx, ny):
    vertex_list = np.array(range(nx * ny))
    # neighborhood = np.zeros([vertex_list.shape[0], 8])

    return neighborhood


def skeletonize(morph):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert np.allclose(skeleton, [[False, False,  True], [False, False,  True], [True,  True, False]])
    """
    skel, distance = medial_axis(morph, return_distance=True)
    return skel


def skeletal_len(skeleton):
    return np.count_nonzero(skeleton)


def f_skeletal_pixels(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert(f_skeletal_pixels(skeleton) == 0.44)
    """
    count = np.count_nonzero(skeleton)
    return round(count / skeleton.size, 2)


def branch_descriptors(skeleton):
    branch_data = summarize(Skeleton(skeleton))
    return branch_data


def count_branch(branch_data):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> branch = branch_descriptors(skeleton)
    >>> assert(count_branch(branch) == 1)
    """
    return branch_data.shape[0]


def branch_len(branch_data):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> branch = branch_descriptors(skeleton)
    >>> assert(branch_len(branch) == 3.41)
    """
    return round(branch_data["branch-distance"].mean(), 2)


def count_junctions(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert(count_junctions(skeleton) == 0)
    """
    graph = sknw.build_sknw(skeleton)
    neighbors = []
    for x in graph.nodes():
        c = 0
        for n in graph.neighbors(x):
            c += 1
        neighbors.append(c)
    J = len([i for i in neighbors if i > 1])
    return J


def count_ends(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert(count_ends(skeleton) == 2)
    """
    graph = sknw.build_sknw(skeleton)
    neighbors = []
    for x in graph.nodes():
        c = 0
        for n in graph.neighbors(x):
            c += 1
        neighbors.append(c)
    E = len([i for i in neighbors if i == 1])
    return E
