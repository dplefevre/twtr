from nltk.corpus import twitter_samples
import re, string

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus import stopwords
from nltk import FreqDist, classify, NaiveBayesClassifier

from nltk.tokenize import word_tokenize

import random

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
test = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]
stop_words = stopwords.words('english')