from utils.data_loader import Dataloader
from utils.utils import *
from utils.network_building import *
import nxmetis
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from termcolor import colored

if __name__ == '__main__':
    matplotlib.use('Agg')
    threshold = 0.0
    print('load sentiment model')
    model = load_model_sentiment('/root/Sentiment-analysis/sentiment_module.model')
    print('load dataset')
    file = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file)
    print('build retweet and reply dynamic graph')
    ret_graph = static_retweet_graph(dataset)
    print('partition retweet graph')
    partitions = nxmetis.partition(ret_graph, 2)
    op_nodes = partitions[1][0]
    agg_nodes = partitions[1][1]
    for graph_type in ['mention']:
        rep_graphs = dynamic_graph(dataset, graph_type=graph_type, sentiment=True)
        between_scores = {'neg': [], 'pos': []}
        op_scores = {'neg': [], 'pos': []}
        agg_scores = {'neg': [], 'pos': []}
        for key, rep_graph in rep_graphs.items():
            for edge in rep_graph.edges:
                count = 0
                for text in rep_graph[edge[0]][edge[1]]['text']:
                    if 'pos' or 'neg' not in rep_graph[edge[0]][edge[1]]:
                        rep_graph[edge[0]][edge[1]]['pos'] = 0
                        rep_graph[edge[0]][edge[1]]['neg'] = 0
                    sent = sentiment(text, model, prob=True)
                    if sent[0] > threshold or sent[1] > threshold:
                        rep_graph[edge[0]][edge[1]]['neg'] += sent[0]
                        rep_graph[edge[0]][edge[1]]['pos'] += sent[1]
                        count += 1
                if count != 0:
                    rep_graph[edge[0]][edge[1]]['neg'] /= count
                    rep_graph[edge[0]][edge[1]]['pos'] /= count

            between_partitions = {'neg': 0, 'pos': 0, 'count': 0}
            op_partition = {'neg': 0, 'pos': 0, 'count': 0}
            agg_partition = {'neg': 0, 'pos': 0, 'count': 0}
            for edge in rep_graph.edges:
                if (edge[0] in op_nodes and edge[1] in agg_nodes) or (edge[0] in agg_nodes and edge[1] in op_nodes):
                    for sent in ['pos', 'neg']:
                        between_partitions[sent] += rep_graph[edge[0]][edge[1]][sent]
                    between_partitions['count'] += 1
                elif edge[0] in op_nodes and edge[1] in op_nodes:
                    for sent in ['pos', 'neg']:
                        op_partition[sent] += rep_graph[edge[0]][edge[1]][sent]
                    op_partition['count'] += 1
                elif edge[0] in agg_nodes and edge[1] in agg_nodes:
                    for sent in ['pos', 'neg']:
                        agg_partition[sent] += rep_graph[edge[0]][edge[1]][sent]
                    agg_partition['count'] += 1
            for sent in ['pos', 'neg']:
                if between_partitions['count'] != 0:
                    between_partitions['%s_avg' % sent] = between_partitions[sent] / between_partitions['count']
                else:
                    between_partitions['%s_avg' % sent] = 0
                if op_partition['count'] != 0:
                    op_partition['%s_avg' % sent] = op_partition[sent] / op_partition['count']
                else:
                    op_partition['%s_avg' % sent] = 0
                if agg_partition['count'] != 0:
                    agg_partition['%s_avg' % sent] = agg_partition[sent] / agg_partition['count']
                else:
                    agg_partition['%s_avg' % sent] = 0
                between_scores[sent].append(between_partitions['%s_avg' % sent])
                op_scores[sent].append(op_partition['%s_avg' % sent])
                agg_scores[sent].append(agg_partition['%s_avg' % sent])
            print(colored('dynamic graph key: %s' % key, 'green'))
            print('between partitions')
            print(between_partitions)
            print('opposite partition')
            print(op_partition)
            print('agreeing partition')
            print(agg_partition)

        for sent in ['pos', 'neg']:
            x = np.arange(len(rep_graphs))
            plt.plot(x, between_scores[sent], color='red')
            plt.plot(x, op_scores[sent], color='blue')
            plt.plot(x, agg_scores[sent], color='green')

            plt.legend(['Between Group', 'Left Group', 'Right Group'], loc='upper left')

            plt.savefig('../Plots/%s_%s_%s.png' % (file, graph_type, sent))
