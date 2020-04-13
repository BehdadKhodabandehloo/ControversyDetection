
"""
@author: Behdad Khodabandehloo
"""
import networkx as nx
import pandas as pd

def Static_Retweet_graph_Building(Data):
    
    Original_Username = [] # username of who tweet
    Retweeting_Username = [] # user name of who retweet
    
    for i in range(len(baltimore_data)):
        if type(baltimore_data['retweeted_status'][i]) == dict:
            Original_Username.append(baltimore_data['retweeted_status'][i]['user']['screen_name'])
            Retweeting_Username.append(baltimore_data['user'][i]['screen_name'])
            
    edges_to_add = []   
    for j in range(len(Original_Username)):
        edges_to_add.append((Retweeting_Username[j],Original_Username[j]))
            
    # Remove Duplicate Elements
    edges_list = list(set(edges_to_add))
        
    Graph = nx.Graph()
    
    # Adding Weights to Graph
    for i in range(len(edges_list)):
        Graph.add_edges_from([edges_list[i]], weight=edges_to_add.count(edges_list[i]))
        
    return Graph
