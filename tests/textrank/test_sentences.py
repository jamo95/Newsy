from app.textrank import sentences
from app.textrank.node import Node


def test_rank():
    sentence_list = sorted([
        'This is a sentence.', 'A quick brown fox.', 'Jumped over the lazy dog.'
    ])

    sentence_nodes = sentences.rank([
        Node(s, score=sentences.DEFAULT_NODE_SCORE) for s in sentence_list])
    sentence_nodes = sorted(sentence_nodes, key=lambda n: n.data)

    # Here we expect that each sentence node will have the same score. This is
    # because the 'clean' (non-stop) words in each sentence have no similarity
    # with any other sentence.
    for i in range(len(sentence_list)):
        assert sentence_nodes[i].data == sentence_list[i]
        assert sentence_nodes[i].score == sentences.DEFAULT_NODE_SCORE
