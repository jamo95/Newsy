import collections

from .graph import Graph
from .helpers import tokenize_words, pos_tag_tokens
from .node import Node

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

D_FACTOR = 0.85
WINDOW_SIZE = 3 #Must be odd (Includes label word)
TITLE_MULTIPLIER = 1.1

SCORE_ITERATIONS = 2


def rank_words(title, text):
    # Preprocessing 
    title_words = tokenize_words(title)
    text_words = tokenize_words(text)

    # Textrank Algorithm
    graph = Graph()
    seen_words = []
    _connect_nodes(graph, title_words, multiplier=TITLE_MULTIPLIER)
    _connect_nodes(graph, text_words)

    for node in graph.get_nodes():
        _score_node(graph, node)

    return sorted(graph.get_nodes(), key=lambda n: n.score, reverse=True)


def _connect_nodes(graph, words, multiplier=1.0):
    """
    :param graph (Graph)
    :param words (list of words)
    :param multiplier - To boost scores of title or other special word sets
    Uses coocurrence in a window of WINDOW_SIZE to create nodes
    target_node and context_node and create edges between these nodes
    """
    to_connect = _get_cooccurrence_matrix(words)

    for t_word in to_connect:
        t_node = Node(t_word, multiplier=multiplier)
        for c_word in to_connect[t_word]:
            c_node = Node(c_word, multiplier=multiplier)

            graph.add_edge(t_node, c_node)
            graph.add_edge(c_node, t_node)

def _get_cooccurrence_matrix(words):
    """
    :param words (list of words)
    RETURN: a coocurrence matrix with each row representing target: context_words
    """
    to_connect = {}

    # Exit if less words than required
    if (len(words) < WINDOW_SIZE):
        return to_connect

    # So we can do some fancy optimisations later
    buffer = collections.deque(maxlen=WINDOW_SIZE)

    # First window
    data_index = 0
    for i in range(WINDOW_SIZE):
        buffer.append(words[i])
        data_index = (data_index + 1) % len(words)

    for i in range(len(words)):
        target_index = WINDOW_SIZE // 2 
        target_word = buffer[target_index]

        for j in range(WINDOW_SIZE):
            if j == target_index:
                continue

            if target_word not in to_connect:
                to_connect[target_word] = [] 

            context_word = buffer[j]
            if context_word not in to_connect[target_word]:
                to_connect[target_word].append(context_word)

        # Slide window one word over
        buffer.append(words[data_index])
        data_index = (data_index + 1) % len(words)
    return to_connect 


def _score_node(graph, node, iterations=SCORE_ITERATIONS):
    if iterations == 0:
        return 0

    score = node.score * node.multiplier
    connected_nodes = graph.get_connected_from(node)

    if len(connected_nodes) == 0:
        return 0

    for connected_node in connected_nodes:
        iter_score = _score_node(graph, connected_node, iterations - 1)
        # Make sure this is right
        score += float(iter_score) / float(len(connected_nodes))

    node.score = (1 - D_FACTOR) + D_FACTOR * score

    return node.score
