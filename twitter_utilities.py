import inspect
import logging
import re
import string
import sys

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


log = logging.getLogger("twitter_utilities")
log.setLevel(logging.INFO)
# handler = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# log.addHandler(handler)

def cleanup_query(search_query):
    for symbol in ["@", "#", "$"]:
        if symbol in search_query:
            clean_query = search_query.replace(symbol, "")
        else:
            clean_query = search_query
    return clean_query


def filter_tweets(tweet_list):
    """This function takes a list of tweets and attempts to
    remove those that contain scams, sales pitches, or otherwise
    useless content"""
    filtered_tweets = []
    stop_content = ["link in bio", "giveaway", "tutorial", "chat", "we help you"]
    for tweet in tweet_list:
        intersection = [content for content in stop_content if content in tweet.lower()]
        if len(intersection) == 0:
            filtered_tweets.append(tweet)
        else:
            continue
    log.info(f"Removed {len(tweet_list) - len(filtered_tweets)} junk tweets!")
    return filtered_tweets


def get_api_keys(keyfile):
    """Load API keys from local textfile"""
    with open(keyfile, "r") as f:
        file_data = f.readlines()
    keys = {}
    for line in file_data:
        key_type, value = line.split(": ")
        keys[key_type] = value.strip()
    return keys


def get_search_queries():
    log = logging.getLogger("twitter_utilities.get_search_queries")
    QUERY_FILE = "/Users/daniellefevre/PycharmProjects/untitled2/queries.txt"
    with open(QUERY_FILE, "r") as f:
        query_list = f.readlines()
    query_list = [query.strip() for query in query_list]
    log.info(f"Search queries: {query_list}")
    return query_list


def remove_noise(tweet_tokens, stop_words=()):

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

