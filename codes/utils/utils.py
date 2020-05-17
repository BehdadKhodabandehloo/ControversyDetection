import datetime
import time
import ktrain
from data_loader import Dataloader


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
    dataloader = Dataloader('/root/tweets_dataset')
    dataset = dataloader.load_files(file, 5)
    model = load_model_sentiment('/root/Sentiment-analysis/sentiment_module.model')
    for item in dataset:
        print(item['full_text'])
        print(sentiment([item['full_text']], model))