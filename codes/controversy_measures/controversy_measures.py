from math import log2
import networkx as nx
import nxmetis
from scipy import stats
import random
import numpy as np


#seperate edge
def betweenness_centrality_controversy(graph, seprated_graph):
	betweeness_edges = nx.algorithms.centrality.edge_betweenness_centrality(graph)
	cut_edges, rest_edges = seprate_graph_with_betweenness(seprated_graph, betweeness_edges)
	pdf_cut_edges = stats.norm.pdf(list(cut_edges.values()))
	pdf_rest_edges = stats.norm.pdf(list(betweeness_edges.values()))
	rsamples_pdf_cut_edges = random.choices(pdf_cut_edges, k=10000)
	rsamples_pdf_rest_edges = random.choices(pdf_rest_edges, k=10000)
	kl = kl_divergence(rsamples_pdf_cut_edges, rsamples_pdf_rest_edges)
	kl = stats.entropy(rsamples_pdf_cut_edges, rsamples_pdf_rest_edges)
	print(kl)
	print(1/(np.exp(kl)))
	BCC = 1 - (1/np.exp(kl))
	print(BCC)

#calculate kl divergence
def kl_divergence(p, q):
	return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p)))


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

if __name__ == '__main__':
	graph = nx.karate_club_graph()
	seprated_graph = nxmetis.partition(graph, 2)
	betweenness_centrality_controversy(graph, seprated_graph)