import re
import string

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


def cleanup_query(search_query):
    for symbol in ["@", "#", "$"]:
        if symbol in search_query:
            clean_query = search_query.replace(symbol, "")
        else:
            clean_query = search_query
    return clean_query


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
    QUERY_FILE = "/Users/daniellefevre/PycharmProjects/untitled2/queries.txt"
    with open(QUERY_FILE, "r") as f:
        query_list = f.readlines()
    query_list = [query.strip() for query in query_list]
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

