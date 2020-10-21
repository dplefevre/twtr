import json
import random

from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

from twitter_utilities import remove_noise
from plotting import create_plot
"""
This script will load the file of tweets which was downloaded by search_analyze.py, and perform sentiment
analysis on them.

It prints out the list of tweets, categorized as "positive" or "negative", 
and also visualizes the result in a pie chart
"""

DOWNLOADED_TWEETS = "/Users/daniellefevre/PycharmProjects/untitled2/new_tweets_AAPL.json"


def get_all_words(cleaned_tokens_list):
    for tkns in cleaned_tokens_list:
        for token in tkns:
            yield token


def get_tweets_for_models(cleaned_tokens_list):
    for twt_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in twt_tokens)


def load_real_tweets():
    with open(DOWNLOADED_TWEETS, "r") as f:
        downloaded_tweets = json.load(f)
    return downloaded_tweets


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
p_n_array = []
for tweet, rt in zip(cleaned_tweets, real_tweets):
    pos_neg = classifier.classify(dict([token, True] for token in tweet))
    p_n_array.append(pos_neg)
    print(f"{pos_neg}, {rt}")
create_plot(p_n_array)
