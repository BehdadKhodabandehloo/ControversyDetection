import networkx as nx
import copy
import nxmetis
import bigjson
from bigjson.filereader import FileReader
import json
import datetime
import time
import collections
import matplotlib.pyplot as plt

if __name__ == '__main__':
    from data_loader import Dataloader
    file = 'baltimore_data'
    dataloader = Dataloader('/home/behdad/Desktop/baltimore_data.json')
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

#mention_clustering_coeff = clustering_coeff(snapshots, graph_type = 'mention')


#(main_graph, left_side, right_side) = three_graph(snapshots[44], 'mention')
# degree distributions
def degree_distribution(snapshot, graph_type):
    (main_graph, left_side, right_side) = three_graph(snapshot, graph_type)
    degree_sequence_main_graph = sorted([d for n, d in main_graph.degree()], reverse=True)
    degree_sequence_left_side = sorted([d for n, d in left_side.degree()], reverse=True)
    degree_sequence_right_side = sorted([d for n, d in right_side.degree()], reverse=True)
    plt.hist(degree_sequence_main_graph, alpha=0.5, label='main graph')
    plt.hist(degree_sequence_left_side, alpha=0.5, label='left side')
    plt.hist(degree_sequence_right_side, alpha=0.5, label='right side')
    plt.legend(loc='upper right')
    plt.show()

# dd = degree_distribution(snapshot[0], 'mention')