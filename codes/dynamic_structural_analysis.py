from codes.utils.data_loader import *
import networkx as nx
from codes.utils.network_building import dynamic_graph
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

def all_snapshots(retweet_snapshots, mention_snapshots, reply_snapshots):
    snapshot_tuples = []
    for key in retweet_snapshots.keys():
        snapshot_tuples.append((retweet_snapshots[key], mention_snapshots[key], reply_snapshots[key]))
    return snapshot_tuples

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


# obtain clustering coeff
def clustering_coeff(snapshots, graph_type):
    cc = []
    for item in snapshots:
        (main_graph,left_side, right_side) = three_graph(item, graph_type)
        cc.append((nx.average_clustering(main_graph),
                   nx.average_clustering(left_side),
                   nx.average_clustering(right_side)))
    return cc

if __name__ == '__main__':
#    from data_loader import Dataloader
    file = 'baltimore_data'
    dataloader = Dataloader('/home/behdad/Desktop')
    dataset = dataloader.load_files(file, 1000)
    retweet_snapshots = dynamic_graph(dataset, graph_type='retweet', discrete_bin=3600, sentiment=False,
                                      cumulative=True)
    mention_snapshots = dynamic_graph(dataset, graph_type='mention', discrete_bin=3600, sentiment=False,
                                      cumulative=True)
    reply_snapshots = dynamic_graph(dataset, graph_type='reply', discrete_bin=3600, sentiment=False, cumulative=True)
    snapshots = all_snapshots(retweet_snapshots, mention_snapshots, reply_snapshots)


import collections
(main_graph, left_side, right_side) = three_graph(snapshots[34], 'reply')
degree_sequence_main = sorted([d for n, d in main_graph.degree()], reverse=True)
degree_count_main = collections.Counter(degree_sequence_main)
deg_main, cnt_main = zip(*degree_count_main.items())
cnt_main = list(cnt_main)
deg_main = list(deg_main)
degree_sequence_left_side = sorted([d for n, d in left_side.degree()], reverse=True)
degree_count_left = collections.Counter(degree_sequence_left_side)
deg_left, cnt_left = zip(*degree_count_left.items())
cnt_left = list(cnt_left)
deg_left = list(deg_left)
degree_sequence_right_side = sorted([d for n, d in right_side.degree()], reverse=True)
degree_count_right = collections.Counter(degree_sequence_right_side)
deg_right, cnt_right = zip(*degree_count_right.items())
cnt_right = list(cnt_right)
deg_right = list(deg_right)
#fig, ax = plt.subplots()
a = plt.scatter(deg_main, cnt_main, color='b')
b = plt.scatter(deg_left, cnt_left, color='g')
c = plt.scatter(deg_right, cnt_right, color='r')
plt.xscale('log')
plt.yscale('log')
plt.xlim(0,10000)
plt.ylim(0.1,1000)
plt.legend((a, b, c), ('main', 'left', 'right'))
plt.savefig('beefban reply snapshot 34')
plt.clf()

# this function returns specified centrality measure in a snapshot
# snapshot = snapshots[34]
def centrality(snapshot, centrality_measure, graph_type=None):
    if graph_type is not None:
        (main_graph, left_side, right_side) = three_graph(snapshot, graph_type)
        if centrality_measure == 'betweenness':
            centraliy_main = nx.betweenness_centrality(main_graph)
            centraliy_left = nx.betweenness_centrality(left_side)
            centraliy_right = nx.betweenness_centrality(right_side)
        elif centrality_measure == 'eigenvector':
            centraliy_main = nx.eigenvector_centrality(main_graph)
            centraliy_left = nx.eigenvector_centrality(left_side)
            centraliy_right = nx.eigenvector_centrality(right_side)
        elif centrality_measure == 'closeness':
            centraliy_main = nx.closeness_centrality(main_graph)
            centraliy_left = nx.closeness_centrality(left_side)
            centraliy_right = nx.closeness_centrality(right_side)
        return tuple((centraliy_main, centraliy_left, centraliy_right))

c = []
iter = 0
for item in snapshots[44:]:
    print(iter)
    c.append(centrality(item, 'closeness', graph_type = 'retweet'))
    iter += 1