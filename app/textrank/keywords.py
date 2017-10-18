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

    tags = ['NN', 'JJ']     # NN = Noun JJ = Adjective NNP = Pronoun
    tagged = pos_tag_tokens(text_words)
    text_words = [t[0] for t in tagged if t[1] in tags]

    # Textrank Algorithm
    graph = Graph()
    seen_words = []
    _connect_nodes(graph, seen_words, title_words, multiplier=TITLE_MULTIPLIER)
    print(seen_words)
    _connect_nodes(graph, seen_words, text_words)
    print(seen_words)

    for node in graph.get_nodes():
        _score_node(graph, node)

    #no = list(graph.get_nodes())
    return sorted(graph.get_nodes(), key=lambda n: n.score, reverse=True)


def _connect_nodes(graph, seen_words , words, multiplier=1.0):
    """
    :param graph (Graph)
    :param words (list of str)
    Uses coocurrence in a window of WINDOW_SIZE to create nodes
    and create edges between nodes
    target_node is a Node of the current word
    context_node.data is a word within WINDOW_SIZE of the target_node.data
    """

    # Less words than required
    if (len(words) < WINDOW_SIZE):
        return 

    data_index = 0
    # So we can do some fancy optimisations later
    buffer = collections.deque(maxlen=WINDOW_SIZE)

    # First window
    for i in range(WINDOW_SIZE):
        buffer.append(words[i])
        data_index = (data_index + 1) % len(words)

    for i in range(len(words)):
        target_index = WINDOW_SIZE // 2 
        target_word = buffer[target_index]

        for j in range(WINDOW_SIZE):
            if j == target_index:
                continue

            if target_word not in seen_words:
                seen_words.append(target_word)
                target_node = Node(target_word)
                target_node.multiplier = multiplier

            context_word = buffer[j]
            if context_word not in seen_words:
                seen_words.append(context_word)
                context_node = Node(context_word)
                context_node.multiplier = multiplier 

            graph.add_edge(target_node, context_node)
            graph.add_edge(context_node, target_node)

        # Slide window one word over
        buffer.append(words[data_index])
        data_index = (data_index + 1) % len(words)


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
