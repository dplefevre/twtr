import tweepy
import json

example_trends = "/Users/daniellefevre/PycharmProjects/untitled2/example_data_new.json"
twitter_keys = "/Users/daniellefevre/PycharmProjects/untitled2/twitterkeys.txt"


def get_api_keys(keyfile):
    """Load API keys from local textfile"""
    with open(keyfile, "r") as f:
        file_data = f.readlines()
    keys = {}
    for line in file_data:
        type, value = line.split(": ")
        keys[type] = value.strip()
    return keys


def list_trends(trendfile):
    with open(trendfile) as f:
        trend_data = json.load(f)
    return trend_data


def write_json_to_file(json_data, filename):
    """Save Twitter data to a file, to avoid calling API more than needed"""
    with open(filename, "w") as f:
        json.dump(json_data, f)


def download_twitter_data(keys):
    """Download a set of tweets using the Twitter API"""
    ny_code = "2458833"
    auth = tweepy.AppAuthHandler(keys["API key"], keys["Secret key"])
    api = tweepy.API(auth)
    return api.trends_place(ny_code)[0]


def search_tweets(keys):
    auth = tweepy.AppAuthHandler(keys["API key"], keys["Secret key"])
    api = tweepy.API(auth)
    tweets = api.search("$TSLA", lang="en", count=50)
    return tweets


def cursor_search(keys):
    auth = tweepy.AppAuthHandler(keys["API key"], keys["Secret key"])
    api = tweepy.API(auth)
    query = "$TSLA"
    language = "en"
    tweets_to_get = 50
    new_tweets = tweepy.Cursor(api.search, q=query, lang=language)
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


# Load api keys
api_keys = get_api_keys(twitter_keys)
# Download Twitter data
# data = download_twitter_data(api_keys)
# tweets = search_tweets(api_keys)
tweets = cursor_search(api_keys)
cleaned_tweets = cleanup_tweets(tweets)
print(cleaned_tweets)
# Save data to file
write_json_to_file(tweets, example_trends)

