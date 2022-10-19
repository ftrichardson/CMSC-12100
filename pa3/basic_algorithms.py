"""
CS121: Analyzing Election Tweets (Solutions)

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

Functions to implement:

- count_tokens
- find_top_k
- find_min_count
- find_most_salient

You may add helper functions.
"""

import math
from util import sort_count_pairs


def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''
    token_cnts = {}

    for token in tokens:
        token_cnts[token] = token_cnts.get(token, 0) + 1
    
    return token_cnts


def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''
    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    return [token for (token, __) in sort_count_pairs(list(count_tokens(tokens).items()))[:k]]


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''
    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    return {token for (token, cnt) in sort_count_pairs(list(count_tokens(tokens).items())) if cnt >= min_count}


def tf_score(term, doc):
    ''' 
    Computes the tf score for a term in a document

    Inputs:
        term: a word (string)
        doc: a document (list of strings)
    
    Returns: tf score (float)
    '''
    term_counts = count_tokens(doc)
    return 0.5 + 0.5 * (term_counts[term] / max(term_counts.values()))


def idf_score(term, docs):
    '''
    Computes the idf score for a term in a collection of documents

    Inputs:
        term: a word (a string)
        docs: a collection of documents (list of lists of strings)
    
    Returns: idf score (float)
    '''
    term_appearances = 0

    for doc in docs:
        if term in doc:
            term_appearances += 1
    
    return math.log(len(docs) / term_appearances)


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    salient_words = []

    for doc in docs:
        salient_set = set()
        for term in doc:
            tf_idf_score = tf_score(term, doc) * idf_score(term, docs)
            if tf_idf_score > threshold:
                salient_set.add(term)
        salient_words.append(salient_set)
    
    return salient_words
