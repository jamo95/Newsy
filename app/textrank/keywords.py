import collections

from .graph import Graph
from .helpers import pos_tag_tokens
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
# WINDOW_SIZE Must be odd and include the target word
WINDOW_SIZE = 3
SCORE_ITERATIONS = 2

# TODO
# - Do the post processing
# - Test against newspaper version


def rank_words(words):
    # POS TAG DAT BISH!
    # Using NN and JJ as per paper
    # NN = Noun JJ = Adjective NNP = Pronoun

    tags = ['NN', 'JJ']
    tagged = pos_tag_tokens(words)
    words = [t[0] for t in tagged if t[1] in tags]

    graph = Graph()
    cooccurrence = _connect_nodes(graph, words)

    for node in graph.get_nodes():
        _score_node(graph, node)

    return list(graph.get_nodes())


def _connect_nodes(graph, words):
    """
    :param graph (Graph)
    :param words (list of str)
    Uses coocurrence in a window of WINDOW_SIZE to create nodes
    and create edges between nodes
    target_node is a Node of the current word
    context_node.data is a word within WINDOW_SIZE of the target_node.data
    """
    seen_nodes = []
    data_index = 0
    # So we can do some fancy optimisations later
    buffer = collections.deque(maxlen=WINDOW_SIZE)

    # First window
    for i in range(WINDOW_SIZE):
        # In case of super small article
        if (len(words) == i):
            break
        buffer.append(words[i])
        data_index = (data_index + 1) % len(words)

    for i in range(len(words)):
        target_index = WINDOW_SIZE // 2 + 1
        target = buffer[target_index]

        for j in range(WINDOW_SIZE):
            if j == target_index:
                continue

            target_node = Node(target)
            if target_node not in seen_nodes:
                seen_nodes.append(target_node)

            context_node = Node(buffer[j])
            if context_node not in seen_nodes:
                seen_nodes.append(context_node)

            graph.add_edge(target_node, context_node)
            graph.add_edge(context_node, target_node)

        # Slide window one word over
        buffer.append(words[data_index])
        data_index = (data_index + 1) % len(words)


def _score_node(graph, node, iterations=SCORE_ITERATIONS):
    if iterations == 0:
        return 0

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
