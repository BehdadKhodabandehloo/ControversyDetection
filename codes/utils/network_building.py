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


def static_reply_graph(data, graph=None):
    orginal_usernames = []
    reply_usernames = []

    for item in data:
        if 'in_reply_to_user_id' in item:
            if item['in_reply_to_user_id'] is not None:
                orginal_usernames.append(item['in_reply_to_user_id'])
                reply_usernames.append(item['user']['id'])

    return graph_maker(orginal_usernames, reply_usernames, graph)


def static_retweet_graph(data, graph=None):
    Original_Username = [] # username of who tweet
    Retweeting_Username = [] # user name of who retweet
    
    for i in range(len(data)):
        if 'retweeted_status' in data[i]:
            if type(data[i]['retweeted_status']) == dict:
                Original_Username.append(data[i]['retweeted_status']['user']['screen_name'])
                Retweeting_Username.append(data[i]['user']['screen_name'])
            
    return graph_maker(Original_Username, Retweeting_Username, graph)


def dynamic_retweet_graph(data, discrete_bin=3600):
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
            dygraph[key] = static_retweet_graph(graph_list)
        else:
            temp_graph = copy.deepcopy(dygraph[previous_key])
            dygraph[key] = static_retweet_graph(graph_list, temp_graph)
        previous_key = key
    return dygraph


if __name__ == '__main__':
    file = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file)
    print('size of dataset = %s' % len(dataset))
    graph = static_reply_graph(dataset)
    print('reply graph --> nodes = %s, edges = %s' % (len(graph.nodes), len(graph.edges)))
    # count = 1
    # for key, graph in dygraphs.items():
    #     print('%s. graph (%s) --> nodes = %s, edges = %s' % (count, key, len(graph.nodes), len(graph.edges)))
    #     count += 1

# 1. graph (1430020362_1430023962) --> nodes = 11, edges = 9
# 2. graph (1430023962_1430027562) --> nodes = 15, edges = 13
# 3. graph (1430027562_1430031162) --> nodes = 118, edges = 113
# 4. graph (1430031162_1430034762) --> nodes = 204, edges = 207
# 5. graph (1430034762_1430038362) --> nodes = 230, edges = 235
# 6. graph (1430038362_1430041962) --> nodes = 297, edges = 306
# 7. graph (1430041962_1430045562) --> nodes = 335, edges = 345
# 8. graph (1430045562_1430049162) --> nodes = 349, edges = 358
# 9. graph (1430049162_1430052762) --> nodes = 363, edges = 370
# 10. graph (1430052762_1430056362) --> nodes = 372, edges = 379
# 11. graph (1430056362_1430059962) --> nodes = 393, edges = 402
# 12. graph (1430059962_1430063562) --> nodes = 414, edges = 424
# 13. graph (1430063562_1430067162) --> nodes = 468, edges = 478
# 14. graph (1430067162_1430070762) --> nodes = 554, edges = 564
# 15. graph (1430070762_1430074362) --> nodes = 614, edges = 624
# 16. graph (1430074362_1430077962) --> nodes = 665, edges = 677
# 17. graph (1430077962_1430081562) --> nodes = 722, edges = 736
# 18. graph (1430081562_1430085162) --> nodes = 780, edges = 797
# 19. graph (1430085162_1430088762) --> nodes = 837, edges = 853
# 20. graph (1430088762_1430092362) --> nodes = 872, edges = 894
# 21. graph (1430092362_1430095962) --> nodes = 916, edges = 944
# 22. graph (1430095962_1430099562) --> nodes = 948, edges = 975
# 23. graph (1430099562_1430103162) --> nodes = 997, edges = 1023
# 24. graph (1430103162_1430106762) --> nodes = 1044, edges = 1070
# 25. graph (1430106762_1430110362) --> nodes = 1097, edges = 1126
# 26. graph (1430110362_1430113962) --> nodes = 1137, edges = 1163
# 27. graph (1430113962_1430117562) --> nodes = 1174, edges = 1195
# 28. graph (1430117562_1430121162) --> nodes = 1250, edges = 1265
# 29. graph (1430121162_1430124762) --> nodes = 1279, edges = 1298
# 30. graph (1430124762_1430128362) --> nodes = 1292, edges = 1312
# 31. graph (1430128362_1430131962) --> nodes = 1303, edges = 1323
# 32. graph (1430131962_1430135562) --> nodes = 1305, edges = 1326
# 33. graph (1430135562_1430139162) --> nodes = 1307, edges = 1328
# 34. graph (1430139162_1430142762) --> nodes = 1312, edges = 1334
# 35. graph (1430142762_1430146362) --> nodes = 1320, edges = 1343
# 36. graph (1430146362_1430149962) --> nodes = 1345, edges = 1371
# 37. graph (1430149962_1430153562) --> nodes = 1380, edges = 1409
# 38. graph (1430153562_1430157162) --> nodes = 1433, edges = 1463
# 39. graph (1430157162_1430160762) --> nodes = 1465, edges = 1500
# 40. graph (1430160762_1430164362) --> nodes = 1502, edges = 1540
# 41. graph (1430164362_1430167962) --> nodes = 1559, edges = 1598
# 42. graph (1430167962_1430171562) --> nodes = 1615, edges = 1670
# 43. graph (1430171562_1430175162) --> nodes = 1646, edges = 1708
# 44. graph (1430175162_1430178762) --> nodes = 1850, edges = 1935
# 45. graph (1430178762_1430182362) --> nodes = 3419, edges = 3708
# 46. graph (1430182362_1430185962) --> nodes = 13296, edges = 17029
# 47. graph (1430185962_1430189562) --> nodes = 27128, edges = 36162
# 48. graph (1430189562_1430193162) --> nodes = 47389, edges = 65672
# 49. graph (1430193162_1430196762) --> nodes = 47891, edges = 66431

# reply graph --> nodes = 3843, edges = 3335