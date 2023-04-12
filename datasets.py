import networkx as nx
import numpy as np
import pandas as pd
from networkx.classes.graph import Graph
from pandas.core.frame import DataFrame

np.random.seed(538)


def sort_nodes_by_graph(
    nodes: DataFrame, network: Graph, id_field: str
) -> DataFrame:
    """Sorts the nodes table by the values in the graph

    This ensures the data in the network and the data in the table match
    """
    nodes["graph_order"] = nodes[id_field].astype("category")
    graph_node_order = list(network.nodes())
    nodes.graph_order = nodes.graph_order.cat.set_categories(graph_node_order)
    return nodes.sort_values("graph_order")


def make_nodes(n):
    voter_ids = [f"IA-{_id}" for _id in np.random.randint(0, 100_000, n)]
    first_names = np.random.choice(
        ["Steve", "Jane", "Bob", "Mary", "Mike", "Sarah"], n
    )
    last_names = np.random.choice(["Johnson", "Smith", "Jackson"], n)
    phones = np.random.randint(0, 10000, n)
    precincts = np.random.randint(0, 5, n)
    supports = np.random.choice(
        [
            "1 - Support",
            "2 - Lean Support",
            "3 - Undecided",
            "4 - Lean Oppose",
            "5 - Oppose",
        ],
        n,
    )

    return pd.DataFrame(
        {
            "voter_id": voter_ids,
            "first_name": first_names,
            "last_name": last_names,
            "phone": phones,
            "precinct": precincts,
            "support": supports,
        }
    )


def make_edges(nodes, n, source_field, target_field):
    assert n > nodes.shape[0]

    # Generate too many points, discard invalid ones
    pairs = np.random.choice(nodes["voter_id"], size=(n * 5, 2))
    df = pd.DataFrame(pairs)

    df.drop_duplicates(inplace=True)
    unique = df[df[0] != df[1]]

    # May error if proportions are off
    sample = unique.sample(n)
    sample.columns = [source_field, target_field]
    return sample


def mock_data(n_nodes=100, n_edges=150, dim=3):
    source = "source"
    target = "target"
    nodes = make_nodes(n_nodes)
    edges = make_edges(nodes, n_edges, source, target)
    network = nx.from_pandas_edgelist(edges, source, target)
    # initalizing a graph doesn't do anything, so we add some math to spread points out
    positions = nx.spring_layout(network, dim=dim)
    nx.set_node_attributes(network, name="position", values=positions)

    nodes = sort_nodes_by_graph(nodes, network, "voter_id")
    return nodes, edges, network


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
