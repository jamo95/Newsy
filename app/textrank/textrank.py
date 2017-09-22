#!/usr/bin/env python3

import sys
from itertools import combinations
from collections import defaultdict
from app.textrank.graph import Graph
from node import Node
import nltk
import math
#from . import *
def extract_sentences(text):

def extract_keywords(text):
    tokens = list(tokenize(text))
    text_nodes = _consolidate_tokens(tokens)

    for node in text_nodes:
        if node.data in [n.data for n in title_nodes]:
            node.in_title = True
            node.score *= 1.1

    # Rank the keywords with TextRank word ranking
    text_nodes = rankWords(text, text_nodes)
    return sorted(text_nodes, key=lambda n: n.score, reverse=True)

def coocurrence (common_entities):
    com = defaultdict(lambda : defaultdict(lambda: {'weight':0}))
    # Build co-occurrence matrix
    for w1, w2 in combinations(sorted(common_entities), 2):
        if w1 != w2:
            com[w1][w2]['weight'] += 1
    return com

def pos_tag_text(text, clean=True):
    '''POS tag a list of tokens.'''

    tokens = tokenizeWords(text)
    tagged = nltk.pos_tag(tokens)
    unclean_words = nltk.corpus.stopwords.words('english')
    unclean_words += string.punctuation

    if clean:
        # Remove unclean words.
        tokens = list(
            filter(lambda tag: tag[0] not in _unclean_words(), tagged)
        )
    return tagged

def tokenize(text):
    tokens = {}
    for token, tag in pos_tag_text(text):
        # Skip duplicate tokens.
        if token in tokens:
            continue
        # Skip short tokens.
        if len(token) < 3:
            continue

        tokens[token] = Node(token, tag, score=1)

    return tokens.values()

def rankWords(text, text_nodes):
    graph = Graph(text_nodes)
    sentences = nltk.sent_tokenize(text)
    connectNodesWords(graph, sentences)
    for node in graph.nodes:
        scoreNode(graph, node)
    return graph.nodes

def rankSentences(sentence_nodes):
    graph = Graph(sentence_nodes)


def scoreNode(graph, node):
    totalVariationScore = node.get_averaged_score()
    node.score += totalVariationScore
    return node.score

def connectNodeSentences(graph):
    for a in graph.nodes:
        for b in graph nodes:
            if a==b:
                continue
            similaritySentences = sentSim(a,b)
            if similaritySentences > 0.5:
                graph.add_edge(a,b)


def sentSim(s1,s2):
    wordsS1 = s1.split()
    wordss2 = s2.split()

    common_word_count = len(set(wordsS1) & set(wordss2))


    log_s1 = _log10(len(wordsS1))
    log_s2 = _log10(len(wordss2))

    if log_s1 + log_s2 == 0:
        return 0
    return common_word_count / (log_s1 + log_s2)

def connectNodesWords(Graph, sentences):
    for s in sentences:
        words = tokenizeWords(sentences)
        for i in range(len(words) - 2):
            cooccurring = words[i:i + 2]
            for token_a in cooccurring:
                word_a = graph.find(node_variation=token_a)
                if not word_a:
                    continue
                for token_b in cooccurring:
                    word_b = graph.find(node_variation=token_b)
                    if not word_b or word_a == word_b:
                        continue
                    graph.add_edge(word_a, word_b)

def tokenizeWords(text):
    tokens = nltk.word_tokenize(text)
    return tokens
def tokenizeSentence(text):
    tokens = nltk.sent_tokenize(text)
    return tokens


def dirtyWords():
    unclean_words = nltk.corpus.stopwords.words('english')
    unclean_words += string.punctuation
    return word not in unclean_words




def _consolidate_tokens( tokens):
    '''Consolidates all token nodes within a base node.'''
    stemmer = SnowballStemmer('english')
    variations = {}

    for token in tokens:
        base = stemmer.stem(token.data)

        if base not in variations:
            variations[base] = []

        variations[base].append(token)

    consolidated_nodes = []

    for base in variations.keys():
        base_node = Node(base,1)

        variation_score = 0
        for variation_node in variations[base]:
            variation_node.base = base_node
            base_node.variations.append(variation_node)
            variation_score += variation_node.score

        base_node.score = variation_score / float(len(variations[base]))
        consolidated_nodes.append(base_node)

    return consolidated_nodes

file = sys.argv[1]
with open(sys.argv[1]) as f:
    file = f.read()
    #print(textrank(file))
    print(coocurrence(file))
    c = coocurrence(file)
