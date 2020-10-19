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


# Load api keys
api_keys = get_api_keys(twitter_keys)
# Download Twitter data
data = download_twitter_data(api_keys)
# Save data to file
write_json_to_file(data, example_trends)

