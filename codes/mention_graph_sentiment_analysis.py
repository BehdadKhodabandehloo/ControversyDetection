if __name__ == '__main__':
    file = 'baltimore_data'
    dataloader = Dataloader('/root/sentiment_module/baltimore')
    dataset = dataloader.load_files(file)
    print(len(dataset))
    print(dataset[0])

model = load_model_sentiment('/root/sentiment_module/sentiment_module.model')

def mention_sentiment(dataset, model):
    retweet_graph = static_retweet_graph(dataset)
    partitions = nxmetis.partition(retweet_graph.to_undirected(), 2)
    mention_graph = static_mention_graph(dataset, sentiment=True)

    # finding cross-edges between two partitions in retweet graph
    left_to_right = list(nx.edge_boundary(retweet_graph, partitions[1][0], partitions[1][1]))
    right_to_left = list(nx.edge_boundary(retweet_graph, partitions[1][1], partitions[1][0]))
    list1 = left_to_right.copy()
    list2 = right_to_left.copy()
    list1.extend(list2)
    cross_edges = list1

    # add sentiment from mention graph to cross-edges
    cross_texts = []
    for item in cross_edges:
        if item in mention_graph.edges():
            print('yes')
            cross_texts.extend(mention_graph.edges[item]['text'])
    cross_sentiment = sentiment(cross_texts, model, prob=True)
    cross_negative = sum(cross_sentiment)[0] / len(cross_texts)
    cross_positive = sum(cross_sentiment)[1] / len(cross_texts)
    print('cross_negative :', cross_negative)
    print('cross_positive :', cross_positive)

    # left side sentiment
    left_partition_edges = retweet_graph.edges(partitions[0])
    left_side_texts = []
    for item in left_partition_edges:
        if item in mention_graph.edges():
            left_side_texts.extend(mention_graph.edges[item]['text'])
    left_partition_sentiment = sentiment(left_side_texts, model, prob=True)
    left_negative = sum(cross_sentiment)[0] / len(left_side_texts)
    left_positive = sum(cross_sentiment)[1] / len(left_side_texts)
    print('left_negative :', left_negative)
    print('left_positive :', left_positive)

    # right side sentiment
    right_partition_edges = retweet_graph.edges(partitions[1])
    right_side_texts = []
    for item in right_partition_edges:
        if item in mention_graph.edges():
            right_side_texts.extend(mention_graph.edges[item]['text'])
    right_partition_sentiment = sentiment(right_side_texts, model, prob=True)
    right_negative = sum(cross_sentiment)[0] / len(right_side_texts)
    right_positive = sum(cross_sentiment)[1] / len(right_side_texts)
    print('right_negative :', right_negative)
    print('right_positive :', right_positive)
