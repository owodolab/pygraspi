import numpy as np
import doctest
from skimage.morphology import medial_axis, skeletonize
import sknw


def neighborhood(nx, ny):
    vertex_list = np.array(range(nx * ny))
    #neighborhood = np.zeros([vertex_list.shape[0], 8])

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
    return (np.count_nonzero(skeleton))


def f_skeletal_pixels(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)[0]
    >>> assert(f_skeletal_pixels(skeleton) == 0.44)
    """
    count = np.count_nonzero(skeleton)
    return round(count/skeleton.size, 2)

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
    b_l = [graph.edges[e]['weight'] for e in graph.edges()]
    return np.array([len(b_l), round(sum(b_l)/len(b_l), 2)])   
