import networkx as nx
import numpy as np
import pandas as pd
from networkx.classes.graph import Graph
from pandas.core.frame import DataFrame

np.random.seed(538)


def get_first_names(n: int):
    """
    Sample n first names from the most popular names for
    American babies born in 2000. Does not consider
    gender assigned at birth

    See https://www.ssa.gov/cgi-bin/popularnames.cgi
    """
    possible_names = [
        "Jacob",
        "Michael",
        "Matthew",
        "Joshua",
        "Christopher",
        "Nicholas",
        "Andrew",
        "Joseph",
        "Daniel",
        "Tyler",
        "Emily",
        "Hannah",
        "Madison",
        "Ashley",
        "Sarah",
        "Alexis",
        "Samantha",
        "Jessica",
        "Elizabeth",
        "Taylor",
    ]
    return np.random.choice(possible_names, n)


def get_last_names(n: int):
    """
    Sample n surnames from the 25 most common surnames
    in the 2010 USA census.


    See https://www.census.gov/topics/population/genealogy/data/2010_surnames.html
    """
    possible_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
    ]
    return np.random.choice(possible_names, n)


def sort_nodes_by_graph(nodes: DataFrame, network: Graph, id_field: str) -> DataFrame:
    """Sorts the nodes table by the values in the graph

    This ensures the data in the network and the data in the table match
    """
    nodes["graph_order"] = nodes[id_field].astype("category")
    graph_node_order = list(network.nodes())
    nodes.graph_order = nodes.graph_order.cat.set_categories(graph_node_order)
    return nodes.sort_values("graph_order")


def make_nodes(n):
    voter_ids = [f"IA-{_id}" for _id in np.random.randint(0, 100_000, n)]
    first_names = get_first_names(n)
    last_names = get_last_names(n)
    phones = "(123)-555-0123"
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
    genders = np.random.choice(["M", "F", "O"], n)

    return pd.DataFrame(
        {
            "voter_id": voter_ids,
            "first_name": first_names,
            "last_name": last_names,
            "phone": phones,
            "precinct": precincts,
            "support": supports,
            "gender": genders,
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
    # initalizing a graph doesn't do anything
    # so we add some math to spread points out
    positions = nx.spring_layout(network, dim=dim)
    nx.set_node_attributes(network, name="position", values=positions)

    nodes = sort_nodes_by_graph(nodes, network, "voter_id")
    return nodes, edges, network
