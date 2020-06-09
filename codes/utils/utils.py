import datetime
import time
import ktrain


def datetime_to_timestamp(t):
    timestamp = datetime.datetime.strptime(t.replace(' +0000', ''), '%a %b %d %H:%M:%S %Y')
    return time.mktime(timestamp.timetuple())


def load_model_sentiment(model_path):
    return ktrain.load_predictor(model_path)


def sentiment(text_list, model, prob=False):
    if prob:
        return model.predict_proba(text_list)
    else:
        return model.predict(text_list)


if __name__ == '__main__':
    file = 'baltimore_data'
    from data_loader import Dataloader
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file)
    import random
    samples = random.sample(dataset, 10)
    model = load_model_sentiment('/root/Sentiment-analysis/sentiment_module.model')
    for item in samples:
        print('Text:')
        print(item['full_text'])
        print('Sentiment: %s' % sentiment([item['full_text']], model, prob=True))
        print('Sentiment: %s' % sentiment([item['full_text']], model))