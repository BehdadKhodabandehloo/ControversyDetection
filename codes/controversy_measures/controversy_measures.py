import networkx as nx
import nxmetis
from scipy import stats
import random
import numpy as np


def betweenness_centrality_controversy(graph, seprated_graph, num_samples=10000):
    betweeness_edges = nx.algorithms.centrality.edge_betweenness_centrality(graph, k=len(graph.nodes))
    cut_edges, rest_edges = seprate_graph_with_betweenness(seprated_graph, betweeness_edges)
    pdf_cut_edges = stats.norm.pdf(list(cut_edges.values()))
    pdf_rest_edges = stats.norm.pdf(list(betweeness_edges.values()))
    rsamples_pdf_cut_edges = random.choices(pdf_cut_edges, k=num_samples)
    rsamples_pdf_rest_edges = random.choices(pdf_rest_edges, k=num_samples)
    kl = stats.entropy(rsamples_pdf_cut_edges, rsamples_pdf_rest_edges)
    BCC = 1 - (1 / np.exp(kl))
    return BCC


def seprate_graph_with_betweenness(seprated_graph, betweeenes_edges):
    first_cut = seprated_graph[1][0]
    second_cut = seprated_graph[1][1]
    cut_edges = {}
    rest_edges = {}
    for betweeenes_edge in betweeenes_edges:
        if betweeenes_edge[0] in first_cut:
            if betweeenes_edge[1] in first_cut:
                rest_edges[betweeenes_edge] = betweeenes_edges[betweeenes_edge]
            else:
                cut_edges[betweeenes_edge] = betweeenes_edges[betweeenes_edge]
        else:
            if betweeenes_edge[1] in second_cut:
                rest_edges[betweeenes_edge] = betweeenes_edges[betweeenes_edge]
            else:
                cut_edges[betweeenes_edge] = betweeenes_edges[betweeenes_edge]
    return cut_edges, rest_edges


"""
if __name__ == '__main__':
    file = 'baltimore_data'
    dataloader = Dataloader('path)
    dataset = dataloader.load_files(file, 10000)
    print(len(dataset))
    print(dataset[0])
"""


def roulette_wheel_selection(List):
    L = []
    r = random.random()
    print(r)
    for i in range(len(List)):
        L.append(List[i])
        if r <= sum(L):
            return i


# graph = static_retweet_graph(dataset)
# Graph partitioning
g = graph
h = g.to_undirected()
partitions = nxmetis.partition(h, 2)

def random_walk_conteroversy(graph, partitions, iterations):
    # Adjacency Matrix
    A = nx.adjacency_matrix(graph)
    adj_matrix = np.transpose(A.todense())

    # Modify Adjacency Matrix
    adjacency = np.copy(adj_matrix)
    adjacency = adjacency.astype(float)
    size = np.size(adjacency, 1)
    for i in range(size):
        if int(sum(adjacency[:, i])) == 0:
            adjacency[:, i] = (1 / size) * np.ones((size, 1)).reshape(size)

    d = 0.85
    modified_adj_matrix = d * adjacency + (1 / size) * (1 - d) * np.ones((size, size))

    # Graph partitioning
    # g = graph
    # h = g.to_undirected()
    # partitions = nxmetis.partition(h, 2)
    
    # whole graph
    all_nodes = list(graph.nodes())
    all_nodes_out_degree = []
    all_nodes_in_degree = []
    for item in all_nodes:
        all_nodes_out_degree.append(graph.out_degree()[item])
        all_nodes_in_degree.append(graph.in_degree()[item])

    # left side
    left_side_nodes = partitions[1][0]
    left_side_nodes_out_degree = []
    left_side_nodes_in_degree = []
    for item in left_side_nodes:
        left_side_nodes_out_degree.append(graph.out_degree()[item])
        left_side_nodes_in_degree.append(graph.in_degree()[item])

    # right side
    right_side_nodes = partitions[1][1]
    right_side_nodes_out_degree = []
    right_side_nodes_in_degree = []
    for item in right_side_nodes:
        right_side_nodes_out_degree.append(graph.out_degree()[item])
        right_side_nodes_in_degree.append(graph.in_degree()[item])

    # list of high degree nodes
    sorted_degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    high_degree_nodes = []
    for item in sorted_degrees[0:int(0.02 * len(sorted_degrees))]:
        high_degree_nodes.append(item[0])

    # list of low degree nodes
    low_degree_nodes = [x for x in all_nodes if x not in high_degree_nodes]

    # RWC
    non_saparate = 0
    separate = 0
    for i in range(iterations):
        # randomly choose a node
        initial_node = random.choice(low_degree_nodes)
        node = initial_node
        # node_neighbor_list = [n for n in graph.successors(node)]
        while node not in high_degree_nodes:
            index = all_nodes.index(node)
            neighbor_index = roulette_wheel_selection(list(modified_adj_matrix[:, index]))
            node = all_nodes[neighbor_index]
            if node in high_degree_nodes:
                high_degree_node = node
        if (initial_node in left_side_nodes) and (high_degree_node in left_side_nodes):
            separate += 1
        if (initial_node in right_side_nodes) and (high_degree_node in right_side_nodes):
            separate += 1
        if (initial_node in right_side_nodes) and (high_degree_node in left_side_nodes):
            non_saparate += 1
        if (initial_node in left_side_nodes) and (high_degree_node in right_side_nodes):
            non_saparate += 1

    rwc_score = separate / iterations

    return rwc_score
