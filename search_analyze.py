import tweepy
import json
import argparse

example_trends = "/Users/daniellefevre/PycharmProjects/untitled2/example_data_new.json"
twitter_keys = "/Users/daniellefevre/PycharmProjects/untitled2/twitterkeys.txt"

arg = argparse.ArgumentParser()
arg.add_argument("query")
args = arg.parse_args()
query = args.query


def get_api_keys(keyfile):
    """Load API keys from local textfile"""
    with open(keyfile, "r") as f:
        file_data = f.readlines()
    keys = {}
    for line in file_data:
        key_type, value = line.split(": ")
        keys[key_type] = value.strip()
    return keys


def list_trends(trendfile):
    with open(trendfile) as f:
        trend_data = json.load(f)
    return trend_data


def write_json_to_file(json_data, fname):
    """Save Twitter data to a file, to avoid calling API more than needed"""
    with open(fname, "w") as f:
        json.dump(json_data, f)


def download_twitter_data(keys):
    """Download a set of tweets using the Twitter API"""
    ny_code = "2458833"
    auth = tweepy.AppAuthHandler(keys["API key"], keys["Secret key"])
    api = tweepy.API(auth)
    return api.trends_place(ny_code)[0]


def search_tweets(keys, search_query):
    auth = tweepy.AppAuthHandler(keys["API key"], keys["Secret key"])
    api = tweepy.API(auth)
    tweets = api.search(search_query, lang="en", count=50)
    return tweets


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


def cleanup_query(search_query):
    for symbol in ["@", "#", "$"]:
        if symbol in search_query:
            clean_query = search_query.replace(symbol, "")
        else:
            clean_query = search_query
    return clean_query


# Load api keys
api_keys = get_api_keys(twitter_keys)
# Download Twitter data
# data = download_twitter_data(api_keys)
# tweets = search_tweets(api_keys)
tweets = cursor_search(api_keys, query)
cleaned_tweets = cleanup_tweets(tweets)
print(cleaned_tweets)
# Save data to file
filename = f"/Users/daniellefevre/PycharmProjects/untitled2/new_tweets_{cleanup_query(query)}.json"
write_json_to_file(tweets, filename)

