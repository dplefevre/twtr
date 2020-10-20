from nltk.corpus import twitter_samples
import re
import string

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

import random
import json

"""
This script will load the file of tweets which was downloaded by main.py, and perform sentiment analysis on them.

It prints out the list of tweets, categorized as "positive" or "negative"
"""

DOWNLOADED_TWEETS = "/Users/daniellefevre/PycharmProjects/untitled2/example_data_new.json"


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_models(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def load_real_tweets():
    with open(DOWNLOADED_TWEETS, "r") as f:
        real_tweets = json.load(f)
    return real_tweets



positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
test = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]
stop_words = stopwords.words('english')

positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

positive_tokens_for_model = get_tweets_for_models(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_models(negative_cleaned_tokens_list)

positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:7000]
test_data = dataset[7000:]

classifier = NaiveBayesClassifier.train(train_data)

real_tweets = load_real_tweets()
cleaned_tweets = [remove_noise(word_tokenize(tweet)) for tweet in real_tweets]
for tweet, rt in zip(cleaned_tweets, real_tweets):
    print(f"{classifier.classify(dict([token, True] for token in tweet))}, {rt}")
