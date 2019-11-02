from typing import Dict, List, Tuple

import pandas as pd
from networkx.classes.graph import Graph


def unpack_edges(network: Graph) -> Tuple[List[float]]:
    """Manipulates the wonky network data into wonky lists
    
    Lists will be as follows:
    [point 1 x0, point 1 x1, np.nan, point 2 x0, point 2 x2, np.nan]

    The lists are one-dimensionsal; each dimension will have its
    own list
    """
    positions = []
    for edge in network.edges():
        # `edge` is a container with two values
        source = edge[0]
        target = edge[1]

        # "position" is an array with one element per network dimension
        source_coords = network.node[source]["position"]
        target_coords = network.node[target]["position"]
        padding = [None for _ in source_coords]

        positions.append(source_coords)
        positions.append(target_coords)
        positions.append(padding)

    # Transpose the list to get ndim lists of len(network.edges())
    transposed = pd.DataFrame(positions).T.values
    return transposed
