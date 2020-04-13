from math import log2
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
	BCC = 1 - (1/np.exp(kl))
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
