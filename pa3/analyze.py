"""
Analyze module
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

def create_entities_lst(tweets, entity_desc):
    '''
    Creates a list of entities based on the entity_desc parameter

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
    
    Returns: a list of entities
    '''
    entities = []
    key, subkey, is_case_sensitive = entity_desc

    for tweet in tweets:
        for entities_dictionary in tweet["entities"][key]:
            if is_case_sensitive:
                entities.append(entities_dictionary[subkey])
            else:
                entities.append(entities_dictionary[subkey].lower())
    
    return entities


def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        k: integer

    Returns: list of entities
    '''
    return find_top_k(create_entities_lst(tweets, entity_desc), k)


def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        min_count: integer

    Returns: set of entities
    '''
    return find_min_count(create_entities_lst(tweets, entity_desc), min_count)

############## Part 3 ##############

def preprocess_tweet(tweet, case_sensitive, is_remove_stop_words=True):
    '''
    Preprocesses a tweet by extracting qualifying words from tweet

    Inputs:
        tweet: a tweet (dictionary)
        case_sensitive: boolean
        is_remove_stop_words: boolean
    
    Returns: a list of qualifying words
    '''
    qualifying_words = []

    for word in tweet['abridged_text'].split():
        word = word.strip(PUNCTUATION)
        if not case_sensitive:
            word = word.lower()
        if is_remove_stop_words:
            if word != "" and word not in STOP_WORDS and not word.startswith(STOP_PREFIXES):
                qualifying_words.append(word)
        else:
            if word != "" and not word.startswith(STOP_PREFIXES):
                qualifying_words.append(word)
    
    return qualifying_words


def create_n_grams(tweet, case_sensitive, n, is_remove_stop_words):
    '''
    Creates a list of n-grams for a tweet

    Inputs:
        tweet: a tweet
        case_sensitive: boolean
        n: an integer
        remove_stop_words: boolean
    
    Returns: a list of n-grams for a tweet
    '''
    n_grams_lst = []

    qualifying_words = preprocess_tweet(tweet, case_sensitive, is_remove_stop_words)

    for index, __ in enumerate(qualifying_words):
        if index + n <= len(qualifying_words):
            n_grams_lst.append(tuple(qualifying_words[index: index + n]))

    return n_grams_lst


def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''
    n_grams_lst = []

    for tweet in tweets:
        n_grams_lst.extend(create_n_grams(tweet, case_sensitive, n, True))
    
    return find_top_k(n_grams_lst, k)


def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''
    n_grams_lst = []

    for tweet in tweets:
        n_grams_lst.extend(create_n_grams(tweet, case_sensitive, n, True))
    
    return find_min_count(n_grams_lst, min_count)


def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''
    n_grams_lst = []

    for tweet in tweets:
        n_grams_lst.append(create_n_grams(tweet, case_sensitive, n, False))
    
    return find_salient(n_grams_lst, threshold)