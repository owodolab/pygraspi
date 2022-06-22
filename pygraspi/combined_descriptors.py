"""The main PyGraSPI module with the public API
"""

import pandas as pd
from toolz.curried import map as fmap
from toolz.curried import pipe

from .skeletal_descriptors import getSkeletalDescriptors
from .graph_graphtool import getGraspiDescriptors


def _map_to_dataframe(func, data):
    return pipe(
        data,
        fmap(func),
        list,
        lambda x: pd.DataFrame(x, columns=sorted(x[0].keys())),
    )


def make_descriptors(data):
    """Generate microstructure descriptors

    Args:
      data: the microstructure morphologies, (n_sample, n_x, n_y, ...)

    Returns:
      a pandas dataframe of samples by features

    The methods used here first represent the microstructures topology
    with a distance map, which is then used to derive a "skeleton"
    graph. The skeleton is then segmented to calculate quantities such
    as the number of branches, branch length or number of
    intersections.

    Currently this only works with two phase materials "a" and "b".

    The column descriptors are as follows.

    ========================= ===========
    Column Name               Description
    ========================= ===========
    branch_length_a           average branch length of skeleton graph in phase 0
    branch_length_b           average branch length of skeleton graph in phase 1
    dist_to_interface_avg_a   average distance to the interface from the skeleton in phase 0
    dist_to_interface_avg_b   average distance to the interface from the skeleton in phase 1
    dist_to_interface_max_a   maximum distance to the interface from the skeleton in phase 0
    dist_to_interface_max_b   maximum distance to the interface from the skeleton in phase 1
    dist_to_interface_min_a   minimum distance to the interface from the skeleton in phase 0
    dist_to_interface_min_b   minimum distance to the interface from the skeleton in phase 1
    distance_to_interface     average of shortest distances to nearest interface from all pixels
    distance_to_interface_0   average of shortest distances to nearest interface from all pixels in phase 0
    distance_to_interface_1   average of shortest distances to nearest interface from all pixels in phase 1
    f_skeletal_pixels_a       fraction of skeleton pixels in phase 0
    f_skeletal_pixels_b       fraction of skeleton pixels in phase 1
    interfacial_area          number of pixels on the interface
    number_of_branches_a      number of branches on the skeleton graph in phase 0
    number_of_branches_b      number of branches on the skeleton graph in phase 1
    number_of_ends_a          number of branch ends on the skeleton graph in phase 0
    number_of_ends_b          number of branch ends on the skeleton graph in phase 1
    number_of_intersections_a number of junctions in the skeleton graph on phase 0
    number_of_intersections_b number of junctions in the skeleton graph on phase 1
    phase_0_cc                number of connected components in phase 0
    phase_0_count             number of pixels in phase 0
    phase_0_interface         number of pixels on the interface in phase 0
    phase_1_cc                number of connected components in phase 1
    phase_1_count             number of pixels in phase 1
    phase_1_interface         number of pixels on the interface in phase 1
    ========================= ===========

    Test case

    >>> import numpy as np
    >>> data = np.array([
    ...     [[0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 1]],
    ...     [[0, 1, 1], [1, 1, 1], [0, 0, 0], [1, 0, 0], [1, 0, 1]]
    ... ])
    >>> actual = make_descriptors(data)
    >>> actual
       branch_length_a  branch_length_b  ...  phase_1_count  phase_1_interface
    0             2.00             2.91  ...              6                  6
    1             2.41             3.83  ...              8                  7
    <BLANKLINE>
    [2 rows x 26 columns]



    """  # pylint: disable=line-too-long
    return pd.concat(
        [
            _map_to_dataframe(getSkeletalDescriptors, data),
            _map_to_dataframe(getGraspiDescriptors, data),
        ],
        axis=1,
        join="inner",
    )
