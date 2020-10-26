import configparser
import datetime
import tweepy
import json
import logging
import sys

from twitter_utilities import cleanup_query, filter_tweets, get_api_keys, get_search_queries


def write_json_to_file(json_data, fname):
    """Save Twitter data to a file, to avoid calling API more than needed"""
    with open(fname, "w") as f:
        json.dump(json_data, f)


def cursor_search(keys, search_query):
    auth = tweepy.AppAuthHandler(keys["API key"], keys["Secret key"])
    api = tweepy.API(auth)
    language = "en"
    tweets_to_get = 50
    new_tweets = tweepy.Cursor(api.search, q=search_query, lang=language)
    tweet_list = [status.text for status in new_tweets.items(tweets_to_get)]
    return tweet_list


def cleanup_tweets(list_of_tweets):
    """remove twitter link and whitespace"""
    new_list = []
    for tweet in list_of_tweets:
        tweet = tweet.split("https://")[0]
        tweet = tweet.replace("\n", " ")
        new_list.append(tweet)
    return new_list


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
        fh = logging.FileHandler(f"{log_dir}/download_tweets.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        root.addHandler(fh)

    root.info(f"download_tweets.py is now starting at {datetime.datetime.now()}")
    runtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Load api keys
    twitter_keys = configs["twitter_keys"]
    api_keys = get_api_keys(twitter_keys)

    # Download Twitter data
    query_file = configs["search_queries"]
    queries = get_search_queries(query_file)
    for query in queries:
        # Search for tweets
        tweets = cursor_search(api_keys, query)
        # Remove noise from tweets
        cleaned_tweets = cleanup_tweets(tweets)
        # Filter out useless tweets
        filtered_tweets = filter_tweets(cleaned_tweets)
        # Save data to file
        filename = \
            f"/Users/daniellefevre/PycharmProjects/tweet_analyzer/new_tweets_{cleanup_query(query)}_{runtime}.json"
        write_json_to_file(tweets, filename)

    root.info(f"download_tweets.py is now completing at {datetime.datetime.now()}")
