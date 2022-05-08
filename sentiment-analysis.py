import pandas as pd
import boto3


def get_sentiment(text):
    text_sent = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = text_sent['Sentiment']
    pos_score = text_sent['SentimentScore']['Positive']
    neg_score = text_sent['SentimentScore']['Negative']
    neutral_score = text_sent['SentimentScore']['Neutral']
    mixed_score = text_sent['SentimentScore']['Mixed']
    return [sentiment, pos_score, neg_score, neutral_score, mixed_score]

if __name__ == '__main__':
    # Getting the various json files into a single df
    kd_tweets = pd.read_json('data\kd_tweets_en_master.json', orient='index')
    lebron_tweets = pd.read_json('data\lebron_tweets_en_master.json', orient='index')
    steph_tweets = pd.read_json('data\steph_tweets_en_master.json', orient='index')
    others_tweets = pd.read_json('data\other_tweets_en_master.json', orient='index')

    all_tweets = kd_tweets.append(lebron_tweets)
    all_tweets = all_tweets.append(steph_tweets)
    all_tweets = all_tweets.append(others_tweets)

    # connect to aws copmrehend
    # need access key and private key - currently as environment variables
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')

    # Running the sentiment analysis and adding columns in the df with the results
    all_tweets['sentiment'], all_tweets['pos_score'], all_tweets['neg_score'],\
        all_tweets['neutral_score'], all_tweets['mixed_score'] = \
            zip(*all_tweets['Text'].map(get_sentiment))

    all_tweets.to_json('all_tweets.json', orient='records')
    print(all_tweets.shape)
    print(all_tweets.head())