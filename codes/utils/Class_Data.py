
# =============================================================================
# Libraries
# =============================================================================
import pandas as pd

# =============================================================================
# Data
# =============================================================================
dataset = pd.read_json('path/data.json')



# =============================================================================
# Class Data
# =============================================================================
class Data(object):
    def __init__(self, data):
        self.data = data
    
    def Retweet_Graph_Building(self):
        created_at = [] # time of creating retweet
        Original_Username = [] # username of who tweet
        Retweeting_Username = [] # user name of who retweet
        for i in range(len(self.data)):
            if type(self.data['retweeted_status'][i]) == dict:
                created_at.append(self.data['created_at'][i])
                Original_Username.append(self.data['retweeted_status'][i]['user']['screen_name'])
                Retweeting_Username.append(self.data['user'][i]['screen_name'])
        
        Graph = {'Creation_time': created_at,
                'Source':Retweeting_Username,
                'Destination': Original_Username
        }
        Graph = pd.DataFrame(Graph)
        return Graph
        
