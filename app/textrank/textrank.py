#!/usr/bin/env python3

import sys
from itertools import combinations
from collections import defaultdict
from .app.textrank.graph import Graph
from node import Node
import nltk
import math
#from . import *

def extract_sentences(text):
    tokens = tokenizeSentence(text)
    sentenceNodes = _consolidate_tokens(tokens)
    sentenceNodes = rankSentences(text, sentenceNodes)
    return sorted(sentenceNodes, key=lambda n: n.score, reverse=True)

def extract_keywords(text):
    tokens = list(tokenizeKeywords(text))
    text_nodes = _consolidate_tokens(tokens)
    # Rank the keywords with TextRank word ranking
    text_nodes = rankWords(text, text_nodes)
    return sorted(text_nodes, key=lambda n: n.score, reverse=True)


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

def tokenizeKeywords(text):
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
    for node in graph.get_nodes():
        scoreNode(graph, node)
    return graph.get_nodes()

def rankSentences(sentence_nodes):
    graph = Graph(sentence_nodes)
    connectNodeSentences(graph)

    for node in graph.get_nodes():
        scoreSentenceNode(graph,node)

    return graph.get_nodes()


def scoreSentenceNode(graph, node, iterations=2):
    if iterations <= 0:
        return 0

    score = node.score
    for nodesConnected in graph.get_connected_to(node):

        outNodeWeight = 0

        for outNodes in graph.get_connected_from(nodesConnected)
            outNodeWeight += outnodes.score

        successiveScore = scoreSentenceNode(graph,nodesConnected,iterations-1)

        weightNodeB = nodesConnected.score * successiveScore
        score += weightNodeB / outNodeWeight

        df = 0.85
        node.score = (1-df) + df * score
    return node.score

def scoreNode(graph, node):
    totalVariationScore = node.get_averaged_score()
    node.score += totalVariationScore
    return node.score




def connectNodeSentences(graph):
    for a in graph.get_nodes():
        for b in graph.get_nodes():
            if a==b:
                continue
            similaritySentences = sentSim(a,b)
            if similaritySentences > 0.5:
                graph.add_edge(a,b)

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




def sentSim(s1,s2):
    wordsS1 = s1.split()
    wordss2 = s2.split()

    common_word_count = len(set(wordsS1) & set(wordss2))


    log_s1 = _log10(len(wordsS1))
    log_s2 = _log10(len(wordss2))

    if log_s1 + log_s2 == 0:
        return 0
    return common_word_count / (log_s1 + log_s2)
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

def get_variations(p, text):
    '''Get the base words of every word in the given text.'''

    stemmer = SnowballStemmer('english')
    variations = {}
    for token, tag in pos_tag_text(text, clean=False):
        base = token
        if token not in [wn.data for wn in variations[base]]:
            variations[base].append(Node(token, pos=tag))
    return variations
file = sys.argv[1]
with open(sys.argv[1]) as f:
    file = f.read()
    #print(textrank(file))
    print(coocurrence(file))
    c = coocurrence(file)
