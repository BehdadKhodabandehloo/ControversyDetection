import networkx as nx
from utils import *
import copy


def graph_maker(heads, tails, texts=None, graph=None):
    # graph initiate
    if graph is None:
        # graph = nx.DiGraph()
        graph = nx.Graph()
    if texts is not None:
        for i in range(len(heads)):
            if graph.has_edge(tails[i], heads[i]):
                graph[tails[i]][heads[i]]['weight'] += 1
                graph[tails[i]][heads[i]]['text'].append(texts[i])
            else:
                graph.add_edges_from([[tails[i], heads[i]]], weight=1, text=texts[i])
    elif texts is None:
        for i in range(len(heads)):
            if graph.has_edge(tails[i], heads[i]):
                graph[tails[i]][heads[i]]['weight'] += 1
            else:
                graph.add_edges_from([[tails[i], heads[i]]], weight=1)

    return graph
    
    
def static_reply_graph(data, sentiment=False, graph=None):
    orginal_usernames = []
    reply_usernames = []
    texts = None
    if sentiment:
        texts = []
    for item in data:
        if 'in_reply_to_user_id' in item:
            if item['in_reply_to_user_id'] is not None:
                orginal_usernames.append(item['in_reply_to_user_id'])
                reply_usernames.append(item['user']['id'])
                if sentiment:
                    texts.append([[item['full_text']]])

    return graph_maker(orginal_usernames, reply_usernames, texts, graph)


def static_mention_graph(data, sentiment=False, graph=None):
    
    tails = [] 
    heads = [] 
    if sentiment:
        texts = []
        for item in data:
            if 'retweeted_status' not in item:
                for k in range(len(item['entities']['user_mentions'])):
                    tails.append(item['user']['screen_name'])
                    heads.append(item['entities']['user_mentions'][k]['screen_name'])
                    texts.append([[item['full_text']]])

    else:
        texts = None
        for item in data:
            if 'retweeted_status' not in item:
                for k in range(len(item['entities']['user_mentions'])):
                    tails.append(item['user']['screen_name'])
                    heads.append(item['entities']['user_mentions'][k]['screen_name'])

    return graph_maker(heads, tails, texts, graph)   
    
    
def static_retweet_graph(data, graph=None):
    heads = []
    tails = []
    texts = None
    
    for item in data:
        if 'retweeted_status' in item:
                heads.append(item['retweeted_status']['user']['id'])
                tails.append(item['user']['id'])
            
    return graph_maker(heads, tails, texts, graph)


def dynamic_graph(data, graph_type='retweet', discrete_bin=3600):
    graph_types = {
        'retweet': static_retweet_graph,
        'reply': static_reply_graph,
        'mention': static_mention_graph,
        'mention_with_sentiment': static_mention_graph_with_sentiment
    }
    tweet_times = []
    for item in data:
        item['created_at'] = int(datetime_to_timestamp(item['created_at']))
        tweet_times.append(item['created_at'])
    first_time = min(tweet_times)
    window_time = first_time
    last_time = max(tweet_times)
    dygraph = {}
    while last_time > window_time:
        window_time += discrete_bin
        dygraph['%s_%s' % (first_time, window_time)] = []
        first_time = window_time
    for item in data:
        for key in dygraph.keys():
            times = key.split('_')
            if int(times[0]) <= item['created_at'] < int(times[1]):
                dygraph[key].append(item)
    previous_key = None
    for key, graph_list in dygraph.items():
        if previous_key is None:
            dygraph[key] = graph_types[graph_type](graph_list)
        else:
            temp_graph = copy.deepcopy(dygraph[previous_key])
            dygraph[key] = graph_types[graph_type](graph_list, temp_graph)
        previous_key = key
    return dygraph


if __name__ == '__main__':
    from data_loader import Dataloader
    file = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file)
    print('size of dataset = %s' % len(dataset))
    graphs = dynamic_graph(dataset, graph_type='mention')
    # print('reply graph --> nodes = %s, edges = %s' % (len(graph.nodes), len(graph.edges)))
    count = 1
    for key, graph in graphs.items():
        print('%s. graph (%s) --> nodes = %s, edges = %s' % (count, key, len(graph.nodes), len(graph.edges)))
        count += 1
