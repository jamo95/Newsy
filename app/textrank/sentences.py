import math

from .graph import Graph
from .helpers import tokenize_words

D_FACTOR = 0.85     # Dampening factor.
SCORE_ITERATIONS = 2
MIN_SENTENCE_SIMILARITY = 0.5
DEFAULT_NODE_SCORE = 0.5

# TODO: Improvements.
#   - Ignore really short sentences.
#   - When calculating similarity ignore words with bad POS tags.
#   - Use the multiplier on sentence nodes if they contain keywords.


def rank(text_nodes):
    '''Rank sentences.'''

    graph = Graph()

    for node in text_nodes:
        graph.add_node(node)

    _connect_nodes(graph)
    for node in graph.get_nodes():
        _score_node(graph, node)

    return list(graph.get_nodes())


def _connect_nodes(graph):
    '''Connects sentence nodes in the graph based on similarity.'''

    for sentence_a in graph.get_nodes():
        for sentence_b in graph.get_nodes():
            if sentence_a == sentence_b:
                continue

            similarity = _sentence_similarity(sentence_a, sentence_b)
            if similarity > MIN_SENTENCE_SIMILARITY:
                graph.add_edge(sentence_a, sentence_b)


def _sentence_similarity(node_a, node_b):
    '''Calculates the similarity between two node based on content overlap.'''

    node_a_words = tokenize_words(node_a.data)
    node_b_words = tokenize_words(node_b.data)

    # Count the common base words between the sentences.
    common_words = len(list(filter(
        lambda w: w in node_b_words, node_a_words)))

    log_length = math.log(len(node_a_words)) + math.log(len(node_b_words))

    if log_length == 0:
        return 0.0

    return common_words / log_length


def _score_node(graph, node, iterations=SCORE_ITERATIONS):
    '''Score a node in the graph.'''

    if iterations <= 0:
        return 0

    score = node.score * node.multiplier
    connections = graph.get_connected_from(node)

    if len(connections) == 0:
        return 0.0

    for connected_node in connections:
        iter_score = _score_node(graph, connected_node, iterations - 1)
        score += float(iter_score) / float(len(connections))

    node.score = (1 - D_FACTOR) + D_FACTOR * score
    return node.score
