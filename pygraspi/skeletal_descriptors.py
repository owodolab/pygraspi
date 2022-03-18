import numpy as np
import doctest
from skimage.morphology import medial_axis, skeletonize
from skan import Skeleton, summarize
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
    >>> skeleton = skeletonize(data)
    >>> assert np.allclose(skeleton, [[False, False,  True], [False, False,  True], [True,  True, False]])
    """
    skel, distance = medial_axis(morph, return_distance=True)
    return skel

def lengthofSkeleton(skeleton):
    return (np.count_nonzero(skeleton))

def numberofEnds(skeleton):
    neighbors = (neighborhood(skeleton.shape[0], skeleton.shape[1])).flatten()
    skeleton_1D = skeleton.tolist()
    neighbors = neighbors[neighbors!=-1]
    return sum(skeleton_1D[neighbors])

def fractionSkeletalPixels(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert(fractionSkeletalPixels(skeleton) == 0.44)
    """
    count = np.count_nonzero(skeleton)
    return round(count/skeleton.size, 2)

def branchDescriptors(skeleton):
    branch_data = summarize(Skeleton(skeleton))
    return branch_data

def numberofBranches(branch_data):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> branch = branchDescriptors(skeleton)
    >>> assert(numberofBranches(branch) == 1)
    """
    return branch_data.shape[0]

def avgBranchLen(branch_data):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> branch = branchDescriptors(skeleton)
    >>> assert(avgBranchLen(branch) == 3.41)
    """
    return round(branch_data["branch-distance"].mean(), 2)

def getJunctionData(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert(getJunctionData(skeleton) == 0)
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


def getEndData(skeleton):
    """
    >>> data = np.array([[1,1,1],\
                [1,1,1],\
                [1,1,1]])
    >>> skeleton = skeletonize(data)
    >>> assert(getEndData(skeleton) == 2)
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

doctest.testmod()
