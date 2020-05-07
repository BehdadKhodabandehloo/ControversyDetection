import networkx as nx
from utils import *
from data_loader import Dataloader
import copy


def graph_maker(heads, tails, graph=None):
    # graph initiate
    if graph is None:
        graph = nx.Graph()
    for i in range(len(heads)):
        if graph.has_edge(heads[i], tails[i]):
            graph[heads[i]][tails[i]]['weight'] += 1
        else:
            graph.add_edges_from([[heads[i], tails[i]]], weight=1)
    return graph


def directed_graph_maker_without_Sentiment(heads, tails, graph=None):
    # graph initiate
    if graph is None:
        graph = nx.DiGraph()
    for i in range(len(heads)):
        if graph.has_edge(tails[i], heads[i]):
            graph[tails[i]][heads[i]]['weight'] += 1
        else:
            graph.add_edges_from([[tails[i], heads[i]]], weight=1)
    return graph


def directed_graph_maker_with_sentiment(heads, tails, texts, graph=None):
    # graph initiate
    if graph is None:
        graph = nx.DiGraph()
    for i in range(len(heads)):
        if graph.has_edge(tails[i], heads[i]):
            graph[tails[i]][heads[i]]['weight'] += 1
            graph[tails[i]][heads[i]]['text'].append(texts[i])
        else:
            graph.add_edges_from([[tails[i], heads[i]]], weight=1,text = texts[i])

    return graph
    
def static_reply_graph(data, graph=None):
    orginal_usernames = []
    reply_usernames = []

    for item in data:
        if 'in_reply_to_user_id' in item:
            if item['in_reply_to_user_id'] is not None:
                orginal_usernames.append(item['in_reply_to_user_id'])
                reply_usernames.append(item['user']['id'])

    return graph_maker(orginal_usernames, reply_usernames, graph)


def static_mention_graph(data, graph=None):
    
    original_usernames = []
    mentioned_usernames = []
    
    for item in data:
        if 'retweeted_status' not in item:
                for k in range(len(item['entities']['user_mentions'])):
                    original_usernames.append(item['user']['screen_name'])
                    mentioned_usernames.append(item['entities']['user_mentions'][k]['screen_name'])
                    
    return graph_maker(mentioned_usernames, original_usernames, graph)


def static_mention_graph_with_sentiment(data, graph=None):
    
    original_usernames = [] #tails
    mentioned_usernames = [] #Heads
    texts = []
    
    for item in data:
        if 'retweeted_status' not in item:
            for k in range(len(item['entities']['user_mentions'])):
                original_usernames.append(item['user']['screen_name'])
                mentioned_usernames.append(item['entities']['user_mentions'][k]['screen_name'])
                texts.append([[item['full_text']]])
                         
    return graph_maker_with_sentiment(mentioned_usernames, original_usernames, texts, graph)
    
    
def static_retweet_graph(data, graph=None):
    original_username = [] # heads
    retweeting_username = [] # tails
    
    for item in data:
        if 'retweeted_status' in item:
                original_username.append(item['retweeted_status']['user']['screen_name'])
                retweeting_username.append(item['user']['screen_name'])
            
    return graph_maker(original_username, retweeting_username,  graph)


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
