import math

from .graph import Graph
from .helpers import tokenize_words,pos_tag_tokens
from .node import Node

#BRIN AND PAGE
D_FACTOR = 0.85
WINDOW = 15
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

            
#TODO
# - Add preprocessing (POS tagging)
def rank_words(words):
    # I hope nltk.word_tokenize keeps order
    # Uses coocurrence to connect nodes/words
    # POS TAG DAT BISH!
    tags = ['NN', 'JJ', 'NNP']
    tagged = pos_tag_tokens(words)
    words = [t[0] for t in tagged if t[1] in tags]

    graph = Graph()
    cooccurrence = _get_cooccurrence(words)
    for word in cooccurrence:
        graph.add_node(Node(word)) #Default score is 1

    _connect_nodes(graph, cooccurrence)

    for node in graph.get_nodes():
        _score_node(graph, node)

    return list(graph.get_nodes())
    

def _get_cooccurrence(words):
    adjacent = {}
    for i in range(len(words)):
        for j in range(WINDOW):
            # If at the end
            if i+j >= len(words):
                return adjacent

            target = words[i]
            ctx_word = words[i+j]

            if target == ctx_word:
                continue

            if target not in adjacent:
                adjacent[target] = set()

            adjacent[target].add(target)
    return adjacent

def _connect_nodes(graph, cooccurrence):
    nodes = graph.get_nodes()
    for target_node in nodes:
        for ctx_node in nodes:
            if target_node.data == ctx_node.data:
                continue
            for word in cooccurrence[target_node.data]:
                if word == ctx_node.data:
                    graph.add_edge(target_node, ctx_node)

    
def _score_node(graph, node, iterations=SCORE_ITERATIONS):

    if iterations == 0:
        return 0

    score = node.score

    connected_nodes = graph.get_connected_from(node)

    if len(connected_nodes) == 0:
        return 0

    for connected_node in connectedIn:
        iter_score = _score_node(graph, connected_node, iterations - 1)
        score += float(iter_score) / float(len(connections))

    node.score = (1 - D_FACTOR) + D_FACTOR * score

    return node.score


	


