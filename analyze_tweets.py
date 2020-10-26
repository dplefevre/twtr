import configparser
import datetime
import json
import logging
import os
import random
import sys

from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

from twitter_utilities import cleanup_query, get_latest_tweet_file, get_search_queries, remove_noise
from plotting import create_plot
"""
This script will load the file of tweets which was downloaded by download_tweets.py, and perform sentiment
analysis on them.

It prints out the list of tweets, categorized as "positive" or "negative", 
and also visualizes the result in a pie chart
"""


class NewClassifier:

    def __init__(self):
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

        self.classifier = NaiveBayesClassifier.train(train_data)


def get_all_words(cleaned_tokens_list):
    for tkns in cleaned_tokens_list:
        for token in tkns:
            yield token


def get_tweets_for_models(cleaned_tokens_list):
    for twt_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in twt_tokens)


def load_real_tweets(data_dir, cleaned_query):
    log = logging.getLogger("root.load_real_tweets")
    tweet_file = get_latest_tweet_file(data_dir, cleaned_query)
    with open(tweet_file, "r") as f:
        downloaded_tweets = json.load(f)
    log.info(f"Loaded tweets from file: {os.path.basename(tweet_file)}")
    return downloaded_tweets


def classify_tweets(data_folder, search_queries):

    print("starting to classify")

    classifier = NewClassifier()

    # Load search query list and perform analysis on each
    queries = get_search_queries(search_queries)
    clean_queries = [cleanup_query(query) for query in queries]

    for query, clean_query in zip(queries, clean_queries):
        logging.info(f"Analyzing query: {query}")
        real_tweets = load_real_tweets(data_folder, clean_query)
        cleaned_tweets = [remove_noise(word_tokenize(tweet)) for tweet in real_tweets]
        p_n_array = []
        for tweet, rt in zip(cleaned_tweets, real_tweets):
            pos_neg = classifier.classifier.classify(dict([token, True] for token in tweet))
            p_n_array.append(pos_neg)
        # create_plot(clean_query, p_n_array)
        logging.info(f"Classified {query}")
        logging.info(f"Result: {(p_n_array.count('Positive')/p_n_array.count('Negative'))} Positive/Negative")


if __name__ == "__main__":
    # Read config file
    config = configparser.ConfigParser()
    config.read("/Users/daniellefevre/PycharmProjects/tweet_analyzer/configuration.ini")
    configs = config["configs"]

    # Set up logging
    log_dir = configs["log_dir"]
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        root.addHandler(sh)
        fh = logging.FileHandler(f"{log_dir}/analyze_tweets.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
    root.info(f"analyze_tweets.py is now starting at {datetime.datetime.now()}")
    query_file = configs["search_queries"]
    data_dir = configs["data_dir"]
    classify_tweets(data_dir, query_file)
    root.info(f"analyze_tweets.py is now completing at {datetime.datetime.now()}")
