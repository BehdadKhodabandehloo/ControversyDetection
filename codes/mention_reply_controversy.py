from controversy_measures.controversy_measures import *
from utils.data_loader import Dataloader
from utils.utils import *
from utils.network_building import *
import nxmetis

if __name__ == '__main__':
        for file in ['germanwings_data', 'indiana_data', 'indiasdaughter_data', 'leadersdebate_data', 'mothersday_data',
                     'baltimore_data', 'beefban_data']:
            print('load dataset : %s' % file)
            dataloader = Dataloader('/root/tweets_dataset')
            dataset = dataloader.load_files(file)

            # mention graph analysis
            mention_graph = static_mention_graph(dataset)
            partitions = nxmetis.partition(mention_graph, 2)
            bt_con = betweenness_centrality_controversy(mention_graph, partitions)
            # RWW_con = random_walk_conteroversy(mention_graph, partitions, 1000)
            print("mention graph controversy measures")
            print("Betweennes Measure = %s" % bt_con)
            # print("RWW Measure = %s" % RWW_con)

            # reply graph analysis
            reply_graph = static_reply_graph(dataset)
            partitions = nxmetis.partition(reply_graph, 2)
            bt_con = betweenness_centrality_controversy(reply_graph, partitions)
            # RWW_con = random_walk_conteroversy(reply_graph, partitions, 1000)
            print("reply graph controversy measures")
            print("Betweennes Measure = %s" % bt_con)
            # print("RWW Measure = %s" % RWW_con)
