import networkx as nx
import pandas as pd
from networkx.classes.graph import Graph
from pandas.core.frame import DataFrame


def sort_nodes_by_graph(
    nodes: DataFrame, network: Graph, id_field: str
) -> DataFrame:
    """Sorts the nodes table by the values in the graph
    
    This ensures the data in the network and the data in the table match
    """
    nodes["graph_order"] = nodes[id_field].astype("category")
    graph_node_order = list(network.nodes())
    nodes.graph_order.cat.set_categories(graph_node_order, inplace=True)
    return nodes.sort_values("graph_order")


def load_data(
    id_field, source_field="Source", target_field="Target", graph_dimensions=2
):
    """Obviously can modify with actual queries as needed"""

    # person-level data
    nodes = pd.read_csv(
        "https://programminghistorian.org/assets/exploring-and-analyzing-network-data-with-python/quakers_nodelist.csv"
    )

    # connection data, tall with two columns: source_field, target_field
    edges = pd.read_csv(
        "https://programminghistorian.org/assets/exploring-and-analyzing-network-data-with-python/quakers_edgelist.csv"
    )
    network = nx.from_pandas_edgelist(edges, source_field, target_field)
    # initalizing a graph doesn't do anything, so we add some math to spread points out
    positions = nx.spring_layout(network, dim=graph_dimensions)
    nx.set_node_attributes(network, name="position", values=positions)

    nodes = sort_nodes_by_graph(nodes, network, id_field=id_field)
    return nodes, edges, network
