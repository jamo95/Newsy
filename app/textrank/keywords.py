import math
import collections

from .graph import Graph
from .helpers import tokenize_words,pos_tag_tokens
from .node import Node

D_FACTOR = 0.85
#Must be odd
WINDOW_SIZE = 15
SCORE_ITERATIONS = 2
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

            
# TODO 
# - Make the target label centre of window
# - Do the post processing
# - Test against newspaper version


def rank_words(words):
    # I hope nltk.word_tokenize keeps order
    # Uses coocurrence to connect nodes/words
    # POS TAG DAT BISH!
    # NN = Noun JJ = Verb NNP = Pronoun
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
    

def _connect_nodes(graph, cooccurrence):
    nodes = graph.get_nodes()
    for target_node in nodes:
        print(target_node.data, end='')
        print(" >>> ")
        for ctx_node in nodes:
            if target_node.data == ctx_node.data:
                continue
            for word in cooccurrence[target_node.data]:
                if word == ctx_node.data:
                    print(ctx_node.data, end='')
                    print("|", end='')
                    graph.add_edge(target_node, ctx_node)
        print("\n")

def _get_cooccurrence(words):
    """
    :param words (list)
    Returns dictionary with key,value pair as:
    target_node(Node), adjacent_words(Nodes)
    """
    #FIXME Only does 10 to the right -->
    # Make it take the centre word and slide window across
    adjacent = {}
    data_index = 0
    # So we can do some fancy optimisations later
    buffer = collections.deque(maxlen=WINDOW_SIZE)

    # First window
    for i in range(WINDOW_SIZE):
        buffer.append(words[i])
        data_index = (data_index + 1) % len(words)
    
    for i in range(len(words)):
        sliding_index = 0
        target_index = WINDOW_SIZE//2 + 1
        target = buffer[target_index]

        for j in range(WINDOW_SIZE):
            # Don't want to add self
            if j == target_index:
                continue

            if target not in adjacent:
                adjacent[target] = set()

            adjacent[target].add(words[j])
            print(adjacent[target])
            sliding_index += 1

        # Slide window one word over
        buffer.append(words[data_index])
        print("BUFFER!")
        print(buffer)
        data_index = (data_index + 1) % len(words)


     #   #if target not in adjacent:
     #   #    target_node = (Node(word))
     #   #    graph.add_node(target_node)
     #   #    adjacent[target_node] = set()

     #   for j in range(WINDOW):
     #       if i+j == WINDOW_SIZE//2:
     #           continue

     #       # If at the end
     #       #if i+j >= len(words):
     #       #    return adjacent

     #       #ctx_word = words[i+j % len(words)]

     #       #if target == ctx_word:
     #       #    continue

     #       #if target not in adjacent:
     #       #    adjacent[target] = set()

     #       adjacent[target].add(ctx_word)
    return adjacent

    
def _score_node(graph, node, iterations=SCORE_ITERATIONS):
    if iterations == 0:
        return 0
    #TODO Wtf is node.multiplier?
    score = node.score
    connected_nodes = graph.get_connected_from(node)

    if len(connected_nodes) == 0:
        return 0

    for connected_node in connected_nodes:
        iter_score = _score_node(graph, connected_node, iterations - 1)
        # Make sure this is right
        score += float(iter_score) / float(len(connected_nodes))

    node.score = (1 - D_FACTOR) + D_FACTOR * score

    return node.score


