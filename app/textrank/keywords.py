import math

from .graph import Graph
from .helpers import tokenize_words
from .node import Node

#BRIN AND PAGE
D_FACTOR = 0.85
WINDOW = 5
SCORE_ITERATIONS = 20
DEFAULT_NODE_SCORE = 1

"""
TextRank Algo
1. Identify text units that best define the task at hand,
and add them as vertices in the graph.
2. Identify relations that connect such text units, and
use these relations to draw edges between vertices
in the graph. Edges can be directed or undirected,
weighted or unweighted.
3. Iterate the graph-based ranking algorithm until convergence.
4. Sort vertices based on their final score. Use the values
attached to each vertex for ranking/selection decisions
"""

def _get_cooccurrence(words):
    adjacent = {}
    for i in range(len(words)):
        for j in range(WINDOW):
            target = words[i]
            ctx_word = words[i+j]
            print(i+j, len(words))

            if target == ctx_word:
                continue

            if target not in adjacent:
                adjacent[target] = set()

            adjacent[target].add(target)

            # If at the end
            if i+j >= len(words)-1:
                return adjacent

    return adjacent
            
#TODO
# - Add preprocessing (POS tagging)
def rank_words(words):
# I hope nltk.word_tokenize keeps order
# Uses coocurrence to connect nodes/words
    graph = Graph()
    cooccurrence = _get_cooccurrence(words)
    for word in cooccurrence:
        graph.add_node(Node(word)) #Default score is 1

    _connect_nodes(graph, cooccurrence)

    for node in graph.get_nodes():
        _score_node(graph, node)

    return list(graph.get_nodes())
    

def _connect_nodes(graph, cooccurrence):
    nodes = graph.get_nodes()
    for word1 in nodes:
        for word2 in nodes:
            if word1 == word2:
                continue
            for word in cooccurrence[word1]:
                if word == word2:
                    graph.add_edge(word1, word2)

    
def _score_node(graph, node, iterations=SCORE_ITERATIONS):

    if iterations <= 0:
        return 0

    score = node.score

    connectedIn = graph.get_connected_from(node)

    if len(connectedIn) == 0:
        return 0

    for connected_node in connectedIn:
        iter_score = _score_node(graph, connected_node, iterations - 1)
        score += float(iter_score) / float(len(connections))

    node.score = (1 - D_FACTOR) + D_FACTOR * score

    return node.score


	


