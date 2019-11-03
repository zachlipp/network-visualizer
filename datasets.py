import networkx as nx
import pandas as pd
import civis

from networkx.classes.graph import Graph
from pandas.core.frame import DataFrame

with open("lipsum.txt", "r") as infile:
    helper_text = infile.read()


def find_edges():
    q = """
        select
            md5(cc.voter_id) as source
            ,md5(rc.lal_voter_id) as target

        from bern_app.relational_relationalcontact as rc

        join bern_app.canvass_canvasser as cc
            on rc.canvasser_id= cc.id

        join bern_app.accounts_user as au
            on cc.user_id=au.id

        where rc.lal_voter_id is not null
            and rc.state='IA'
            and cc.voter_id is not null
            and rc.lal_voter_id is not null;
        """

    df = civis.io.read_civis_sql(
        sql=q,
        database='Bernie 2020',
        use_pandas=True)

    return df


def find_nodes():
    q = """
        select

            voterid,
            md5(voters_firstname) as first_name,
            md5(voters_lastname) as last_name,
            l2.voters_gender as gender,
            l2.precinct,
            l2.file_state

            from bernie_gsanchez.ia_social_network_nodebase as b
            join l2.ia_demographics_clean as l2
                on b.voterid=md5(l2.lalvoterid)

            where l2.voters_gender is not null
        """

    df = civis.io.read_civis_sql(
        sql=q,
        database='Bernie 2020',
        use_pandas=True)

    return df


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
    id_field, source_field="source", target_field="target", graph_dimensions=2):
    """Obviously can modify with actual queries as needed"""

    
    nodes = pd.read_csv(
        "/Users/gsanchez/Desktop/data/nodes.csv",
        sep=",")

    edges = pd.read_csv(
        "/Users/gsanchez/Desktop/data/edges.csv",
        sep=",")


    #nodes = find_nodes()
    #edges = find_edges()

    '''
    # person-level data
    nodes = pd.read_csv(
        "https://programminghistorian.org/assets/exploring-and-analyzing-network-data-with-python/quakers_nodelist.csv"
    )

    # connection data, tall with two columns: source_field, target_field
    edges = pd.read_csv(
        "https://programminghistorian.org/assets/exploring-and-analyzing-network-data-with-python/quakers_edgelist.csv"
    )
    '''

    network = nx.from_pandas_edgelist(edges, source_field, target_field)
    # initalizing a graph doesn't do anything, so we add some math to spread points out
    positions = nx.spring_layout(network, dim=graph_dimensions)
    nx.set_node_attributes(network, name="position", values=positions)

    nodes = sort_nodes_by_graph(nodes, network, id_field=id_field)
    return nodes, edges, network
