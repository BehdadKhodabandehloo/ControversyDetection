if __name__ == '__main__':
    file = 'baltimore_data'
    dataloader = Dataloader('/root/sentiment_module/baltimore')
    dataset = dataloader.load_files(file)
    
model = load_model_sentiment('/root/sentiment_module/sentiment_module.model')

def group_sentiment(mention_graph, edges, group_side):
    texts = []
    for item in edges:
        if item in mention_graph.edges():
            texts.extend(mention_graph.edges[item]['text'])
    group_sentiment = sentiment(texts, model, prob=True)
    group_negative = sum(group_sentiment)[0] / len(texts)
    group_positive = sum(group_sentiment)[1] / len(texts)
    print(group_side + 'negative :', group_negative)
    print(group_side + 'positive :', group_positive)

            
def mention_sentiment(dataset, model):
    retweet_graph = static_retweet_graph(dataset)
    partitions = nxmetis.partition(retweet_graph.to_undirected(), 2)
    mention_graph = static_mention_graph(dataset, sentiment=True)

    # mention sentiment between left and right partitions
    left_to_right = list(nx.edge_boundary(mention_graph, partitions[1][0], partitions[1][1]))
    right_to_left = list(nx.edge_boundary(mention_graph, partitions[1][1], partitions[1][0]))
    list1 = left_to_right.copy()
    list2 = right_to_left.copy()
    list1.extend(list2)
    cross_edges = list1
    group_sentiment(mention_graph,  cross_edges, 'cross')
    
    # mention sentiment inside left partition
    left_partition_edges = retweet_graph.edges(partitions[1][0])
    group_sentiment(mention_graph, left_partition_edges, 'left')
    
    # mention sentiment inside right partition
    right_partition_edges = retweet_graph.edges(partitions[1][1])
    group_sentiment(mention_graph, right_partition_edges, 'right')

#crossnegative : 0.5683458626988422
#crosspositive : 0.4316540453807417
#leftnegative : 0.7373288869857788
#leftpositive : 0.26267117261886597
#rightnegative : 0.5709779479286887
#rightpositive : 0.4290220520713113
