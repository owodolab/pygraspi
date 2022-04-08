import numpy as np
import networkx as nx
import doctest
import pandas as pd
from .skeletal_descriptors import *
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
       branch_length_a  ...  number_of_intersections_b
    0             2.00  ...                          0
    1             2.41  ...                          0
    <BLANKLINE>
    [2 rows x 16 columns]
    """
    return pipe(
        data,
        fmap(getSkeletalDescriptors),
        list,
        lambda x: pd.DataFrame(x, columns=sorted(x[0].keys()))
    )
