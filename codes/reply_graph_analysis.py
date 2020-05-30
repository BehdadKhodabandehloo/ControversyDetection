import networkx as nx
from utils.data_loader import Dataloader
from utils.utils import *
from utils.network_building import *
import nxmetis

if __name__ == '__main__':
    print('load dataset')
    file = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file)
    print('build retweet graph')
    ret_graph = static_retweet_graph(dataset)
    print('partition retweet graph')
    partitions = nxmetis.partition(ret_graph, 2)
    op_nodes = partitions[1][0]
    agg_nodes = partitions[1][1]
    print('build reply graph')
    rep_graph = static_reply_graph(dataset, sentiment=True)
    print('load sentiment model')
    model = load_model_sentiment('/root/Sentiment-analysis/sentiment_module.model')
    for edge in rep_graph.edges:
        for text in rep_graph[edge[0]][edge[1]]['text']:
            if 'sentiments' not in rep_graph[edge[0]][edge[1]]:
                rep_graph[edge[0]][edge[1]]['sentiment'] = []
            sent = sentiment(text, model)[0]
            if 'neg' in sent:
                rep_graph[edge[0]][edge[1]]['sentiment'].append('neg')
            else:
                rep_graph[edge[0]][edge[1]]['sentiment'].append('pos')
    between_partitions = {'neg': 0, 'pos': 0}
    op_partition = {'neg': 0, 'pos': 0}
    agg_partition = {'neg': 0, 'pos': 0}
    for edge in rep_graph.edges:
        for sent in rep_graph[edge[0]][edge[1]]['sentiment']:
            if edge[0] in op_nodes and edge[1] in agg_nodes:
                between_partitions[sent] += 1
            elif edge[0] in op_nodes and edge[1] in op_nodes:
                op_partition[sent] += 1
            elif edge[0] in agg_nodes and edge[1] in agg_nodes:
                agg_partition[sent] += 1
    print('between partitions')
    print(between_partitions)
    print('opposite partition')
    print(op_partition)
    print('agreeing partition')
    print(agg_partition)
