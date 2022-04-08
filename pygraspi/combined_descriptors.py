import numpy as np
import networkx as nx
import doctest
import pandas as pd
from .skeletal_descriptors import *


def getpygraspi_descriptors(morphs):
#    column_names = ["F. skeletal pixels", "N. ends", "N. intersections", "N. branches", "Avg. len. Branches"]
#    pygraspi_descriptors = pd.DataFrame(columns = column_names)
#    d = getSkeletalDescriptors(morph)
#    pygraspi_descriptors.loc[len(pygraspi_descriptors)] = d
    #s = getGraphDescriptors(morph)
#    return pygraspi_descriptors
    return pd.DataFrame([getSkeletalDescriptors(x) for x in morphs])
