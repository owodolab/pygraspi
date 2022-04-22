import numpy as np
import networkx as nx
import doctest
import pandas as pd
from skeletal_descriptors import *
from graph_descriptors import getGraspiDescriptors
from toolz.curried import map as fmap
from toolz.curried import pipe


def make_descriptors(data):
    """Generate multiple microstructure descriptors using graphs

    Generate descriptors for multiple microstructures using Graph
    based methods. See ... for more details about the methods.

    Args:
      data: the microstructure morphologies, (n_sample, n_x, n_y, ...)

    Returns:
      a pandas dataframe of samples by features

    Test case

    >>> data = np.array([
    ...     [[0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 1]],
    ...     [[0, 1, 1], [1, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 1]]
    ... ])
    >>> actual = make_descriptors(data)
    >>> actual
       branch_length_a  branch_length_b  ...  number_of_intersections_a  number_of_intersections_b
    0             2.00             2.91  ...                          0                          0
    1             2.41             3.83  ...                          0                          0
    <BLANKLINE>
    [2 rows x 16 columns]
    """
    return pipe(
        data,
        fmap(getSkeletalDescriptors),
        list,
        lambda x: pd.DataFrame(x, columns=sorted(x[0].keys())),
    )

def make_graphdescriptors(data):
    """Generate multiple microstructure descriptors using graphs

    Generate descriptors for multiple microstructures using Graph
    based methods. See ... for more details about the methods.

    Args:
      data: the microstructure morphologies, (n_sample, n_x, n_y, ...)

    Returns:
      a pandas dataframe of samples by features

    Test case

    >>> data = np.array([
    ...     [[0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 1]],
    ...     [[0, 1, 1], [1, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 1]]
    ... ])
    >>> make_graphdescriptors(data)
       distance_to_interface  interfacial_area  phase_0_cc  ...  phase_1_cc  phase_1_count  phase_1_interface
    0               2.000000                15           2  ...           3              6                  6
    1               2.066667                14           2  ...           3              8                  7
    <BLANKLINE>
    [2 rows x 8 columns]            
    """
    return pipe(
        data,
        fmap(getGraspiDescriptors),
        list,
        lambda x: pd.DataFrame(x, columns=sorted(x[0].keys())),
    )

doctest.testmod()