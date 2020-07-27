import networkx as nx
from utils.utils import *
from utils import *
import copy
import nxmetis


if __name__ == '__main__':
    from data_loader import Dataloader
    file = 'baltimore_data'
    dataloader = Dataloader('/root/baltimore')
    dataset = dataloader.load_files(file, 1000)


retweet_snapshots = dynamic_graph(dataset, graph_type='retweet', discrete_bin=3600, sentiment=False, cumulative=True)
mention_snapshots = dynamic_graph(dataset, graph_type='mention', discrete_bin=3600, sentiment=False, cumulative=True)
reply_snapshots = dynamic_graph(dataset, graph_type='reply', discrete_bin=3600, sentiment=False, cumulative=True)


def all_snapshots(retweet_snapshots, mention_snapshots, reply_snapshots):
    snapshot_tuples = []
    for key in retweet_snapshots.keys():
        snapshot_tuples.append((retweet_snapshots[key], mention_snapshots[key], reply_snapshots[key]))
    return snapshot_tuples

snapshots = all_snapshots(retweet_snapshots, mention_snapshots, reply_snapshots)

# obtain three graphs in each snapshot in graph_type
def three_graph(snapshot_tuple, graph_type):
    retweet_graph = snapshot_tuple[0]
    mention_graph = snapshot_tuple[1]
    reply_graph = snapshot_tuple[2]
    partitions = nxmetis.partition(retweet_graph.to_undirected(), 2)
    left_side_nodes = partitions[1][0]
    right_side_nodes = partitions[1][1]
    if graph_type == 'retweet':
        main_graph = retweet_graph
        left_side = retweet_graph.subgraph(left_side_nodes)
        right_side = retweet_graph.subgraph(right_side_nodes)
    elif graph_type == 'mention':
        main_graph = mention_graph
        left_side = mention_graph.subgraph(left_side_nodes)
        right_side= mention_graph.subgraph(right_side_nodes)
    elif graph_type == 'reply':
        main_graph = reply_graph
        left_side = reply_graph.subgraph(left_side_nodes)
        right_side = reply_graph.subgraph(right_side_nodes)
    return tuple((main_graph, left_side, right_side))


#retweettt = three_graph(snapshots[0], 'retweet') # return retweet and left and right sides of retweet graph in snapshot 1

# obtain clustering coeff
def clustering_coeff(snapshots, graph_type):
    cc = []
    for item in snapshots:
        (main_graph,left_side, right_side) = three_graph(item, graph_type)
        cc.append((nx.average_clustering(main_graph),
                   nx.average_clustering(left_side),
                   nx.average_clustering(right_side)))
    return cc

mention_clustering_coeff = clustering_coeff(snapshots, graph_type = 'mention')


# degree distributions

