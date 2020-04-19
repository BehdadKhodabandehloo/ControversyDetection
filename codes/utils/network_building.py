import networkx as nx
from utils import *
from data_loader import Dataloader


def static_retweet_graph(data):
    Original_Username = [] # username of who tweet
    Retweeting_Username = [] # user name of who retweet
    
    for i in range(len(data)):
        if 'retweeted_status' in data[i]:
            if type(data[i]['retweeted_status']) == dict:
                Original_Username.append(data[i]['retweeted_status']['user']['screen_name'])
                Retweeting_Username.append(data[i]['user']['screen_name'])
            
    edges_to_add = []   
    for j in range(len(Original_Username)):
        edges_to_add.append((Retweeting_Username[j], Original_Username[j]))
            
    # Remove Duplicate Elements
    edges_list = list(set(edges_to_add))
        
    Graph = nx.Graph()
    
    # Adding Weights to Graph
    for i in range(len(edges_list)):
        Graph.add_edges_from([edges_list[i]], weight=edges_to_add.count(edges_list[i]))
        
    return Graph


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
    for key, graph_list in dygraph.items():
        dygraph[key] = static_retweet_graph(graph_list)
    return dygraph


if __name__ == '__main__':
    file = 'baltimore_data'
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file)
    print('size of dataset = %s' % len(dataset))
    dygraphs = dynamic_retweet_graph(dataset)
    print(dygraphs.keys())
    count = 1
    for key, graph in dygraphs.items():
        print('%s. graph (%s) --> nodes = %s, edges = %s' % (count, key, len(graph.nodes), len(graph.edges)))
        count += 1

# 1. graph (1430020362_1430023962) --> nodes = 11, edges = 9
# 2. graph (1430023962_1430027562) --> nodes = 7, edges = 4
# 3. graph (1430027562_1430031162) --> nodes = 105, edges = 100
# 4. graph (1430031162_1430034762) --> nodes = 107, edges = 99
# 5. graph (1430034762_1430038362) --> nodes = 36, edges = 29
# 6. graph (1430038362_1430041962) --> nodes = 73, edges = 71
# 7. graph (1430041962_1430045562) --> nodes = 48, edges = 39
# 8. graph (1430045562_1430049162) --> nodes = 18, edges = 13
# 9. graph (1430049162_1430052762) --> nodes = 18, edges = 13
# 10. graph (1430052762_1430056362) --> nodes = 14, edges = 9
# 11. graph (1430056362_1430059962) --> nodes = 30, edges = 23
# 12. graph (1430059962_1430063562) --> nodes = 32, edges = 22
# 13. graph (1430063562_1430067162) --> nodes = 64, edges = 54
# 14. graph (1430067162_1430070762) --> nodes = 97, edges = 86
# 15. graph (1430070762_1430074362) --> nodes = 76, edges = 62
# 16. graph (1430074362_1430077962) --> nodes = 70, edges = 56
# 17. graph (1430077962_1430081562) --> nodes = 72, edges = 60
# 18. graph (1430081562_1430085162) --> nodes = 77, edges = 61
# 19. graph (1430085162_1430088762) --> nodes = 76, edges = 56
# 20. graph (1430088762_1430092362) --> nodes = 52, edges = 41
# 21. graph (1430092362_1430095962) --> nodes = 62, edges = 51
# 22. graph (1430095962_1430099562) --> nodes = 45, edges = 33
# 23. graph (1430099562_1430103162) --> nodes = 68, edges = 48
# 24. graph (1430103162_1430106762) --> nodes = 69, edges = 47
# 25. graph (1430106762_1430110362) --> nodes = 72, edges = 56
# 26. graph (1430110362_1430113962) --> nodes = 57, edges = 39
# 27. graph (1430113962_1430117562) --> nodes = 55, edges = 33
# 28. graph (1430117562_1430121162) --> nodes = 87, edges = 70
# 29. graph (1430121162_1430124762) --> nodes = 48, edges = 33
# 30. graph (1430124762_1430128362) --> nodes = 20, edges = 15
# 31. graph (1430128362_1430131962) --> nodes = 20, edges = 11
# 32. graph (1430131962_1430135562) --> nodes = 6, edges = 3
# 33. graph (1430135562_1430139162) --> nodes = 4, edges = 2
# 34. graph (1430139162_1430142762) --> nodes = 13, edges = 7
# 35. graph (1430142762_1430146362) --> nodes = 16, edges = 9
# 36. graph (1430146362_1430149962) --> nodes = 35, edges = 28
# 37. graph (1430149962_1430153562) --> nodes = 49, edges = 43
# 38. graph (1430153562_1430157162) --> nodes = 73, edges = 57
# 39. graph (1430157162_1430160762) --> nodes = 55, edges = 39
# 40. graph (1430160762_1430164362) --> nodes = 55, edges = 43
# 41. graph (1430164362_1430167962) --> nodes = 80, edges = 63
# 42. graph (1430167962_1430171562) --> nodes = 92, edges = 73
# 43. graph (1430171562_1430175162) --> nodes = 56, edges = 39
# 44. graph (1430175162_1430178762) --> nodes = 256, edges = 231
# 45. graph (1430178762_1430182362) --> nodes = 1754, edges = 1797
# 46. graph (1430182362_1430185962) --> nodes = 10633, edges = 13403
# 47. graph (1430185962_1430189562) --> nodes = 16182, edges = 19452
# 48. graph (1430189562_1430193162) --> nodes = 24434, edges = 30025
# 49. graph (1430193162_1430196762) --> nodes = 1020, edges = 796

