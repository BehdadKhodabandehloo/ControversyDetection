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
        count =0
        for text in rep_graph[edge[0]][edge[1]]['text']:
            if 'pos' or 'neg' not in rep_graph[edge[0]][edge[1]]:
                rep_graph[edge[0]][edge[1]]['pos'] = 0
                rep_graph[edge[0]][edge[1]]['neg'] = 0
            sent = sentiment(text, model, prob=True)
            print(sent)
            rep_graph[edge[0]][edge[1]]['neg'] += sent[1]
            rep_graph[edge[0]][edge[1]]['pos'] += sent[0]
            count += 1
        rep_graph[edge[0]][edge[1]]['neg'] /= count
        rep_graph[edge[0]][edge[1]]['pos'] /= count

    between_partitions = {'neg': 0, 'pos': 0, 'count': 0}
    op_partition = {'neg': 0, 'pos': 0, 'count': 0}
    agg_partition = {'neg': 0, 'pos': 0, 'count':0}
    for edge in rep_graph.edges:
        if edge[0] in op_nodes and edge[1] in agg_nodes:
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
        between_partitions['%s_avg' % sent] = between_partitions[sent]/between_partitions['count']
        op_partition['%s_avg' % sent] = op_partition[sent]/op_partition['count']
        agg_partition['%s_avg' % sent] = agg_partition[sent]/agg_partition['count']
    print('between partitions')
    print(between_partitions)
    print('opposite partition')
    print(op_partition)
    print('agreeing partition')
    print(agg_partition)
